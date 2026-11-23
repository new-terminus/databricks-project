# Databricks notebook source
# MAGIC %md
# MAGIC # Transformación Silver
# MAGIC
# MAGIC Se normalizan las marcas de tiempo a UTC. Las velas de Binance se conservan por minuto y se resumen por día antes de unirlas con el índice de sentimiento.

# COMMAND ----------

dbutils.widgets.text("catalog", "catalog_smartdata", "Catalog")
dbutils.widgets.text("bronze_schema", "bitcoin_bronze", "Bronze schema")
dbutils.widgets.text("silver_schema", "bitcoin_silver", "Silver schema")

# COMMAND ----------

from pyspark.sql import functions as F

catalog = dbutils.widgets.get("catalog")
bronze_schema = dbutils.widgets.get("bronze_schema")
silver_schema = dbutils.widgets.get("silver_schema")

spark.conf.set("spark.sql.session.timeZone", "UTC")

prices = spark.table(f"{catalog}.{bronze_schema}.binance_prices")
sentiment = spark.table(f"{catalog}.{bronze_schema}.fear_greed_index")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Velas por minuto
# MAGIC
# MAGIC Los tiempos de Binance están en milisegundos hasta 2024 y en microsegundos desde enero de 2025.

# COMMAND ----------

uses_microseconds = F.col("open_time") >= 1_000_000_000_000_000
open_timestamp = F.when(uses_microseconds, F.timestamp_micros("open_time")).otherwise(
    F.timestamp_millis("open_time")
)
close_timestamp = F.when(uses_microseconds, F.timestamp_micros("close_time")).otherwise(
    F.timestamp_millis("close_time")
)

minutes = (
    prices
    .withColumn("open_timestamp", open_timestamp)
    .withColumn("close_timestamp", close_timestamp)
    .withColumn("trade_date", F.to_date("open_timestamp"))
    .filter(F.col("open_timestamp").isNotNull())
    .dropDuplicates(["open_timestamp"])
)

minutes_table = f"{catalog}.{silver_schema}.binance_minutes"
minutes.write.format("delta").mode("overwrite").saveAsTable(minutes_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Mercado y sentimiento por día
# MAGIC
# MAGIC La apertura y el cierre salen de la primera y última vela de cada día, respectivamente. El cruce conserva los días de mercado que no tienen un valor de sentimiento.

# COMMAND ----------

market_daily = spark.table(minutes_table).groupBy("trade_date").agg(
    F.min_by("open", "open_timestamp").alias("daily_open"),
    F.max("high").alias("daily_high"),
    F.min("low").alias("daily_low"),
    F.max_by("close", "open_timestamp").alias("daily_close"),
    F.sum("volume").alias("daily_volume"),
    F.sum("number_of_trades").alias("daily_trade_count"),
    F.count("*").alias("minute_count"),
)

sentiment_daily = sentiment.select(
    F.to_date(F.timestamp_seconds("timestamp")).alias("trade_date"),
    F.col("value").alias("sentiment_score"),
    F.col("value_classification").alias("sentiment_category"),
).dropDuplicates(["trade_date"])

bitcoin_daily = market_daily.join(sentiment_daily, "trade_date", "left")

daily_table = f"{catalog}.{silver_schema}.bitcoin_daily"
bitcoin_daily.write.format("delta").mode("overwrite").saveAsTable(daily_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revisión de resultados
# MAGIC
# MAGIC Se muestran los días con una cantidad de velas distinta de 1.440 o con el sentimiento vacío.

# COMMAND ----------

silver_daily = spark.table(daily_table)
display(silver_daily.orderBy("trade_date").limit(5))
display(
    silver_daily
    .filter((F.col("minute_count") != 1440) | F.col("sentiment_score").isNull())
    .orderBy("trade_date")
)

print(f"{minutes_table}: {spark.table(minutes_table).count():,} rows")
print(f"{daily_table}: {silver_daily.count():,} rows")

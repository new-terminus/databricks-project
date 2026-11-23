# Databricks notebook source
# MAGIC %md
# MAGIC # Carga Gold
# MAGIC
# MAGIC Se calculan las métricas diarias de Bitcoin y se resumen los resultados por categoría de sentimiento.

# COMMAND ----------

dbutils.widgets.text("catalog", "catalog_smartdata", "Catalog")
dbutils.widgets.text("silver_schema", "bitcoin_silver", "Silver schema")
dbutils.widgets.text("gold_schema", "bitcoin_gold", "Gold schema")

# COMMAND ----------

from pyspark.sql import Window
from pyspark.sql import functions as F

catalog = dbutils.widgets.get("catalog")
silver_schema = dbutils.widgets.get("silver_schema")
gold_schema = dbutils.widgets.get("gold_schema")

bitcoin_daily = spark.table(f"{catalog}.{silver_schema}.bitcoin_daily")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Métricas diarias
# MAGIC
# MAGIC La variación compara el cierre con el cierre anterior. El rango intradía mide la diferencia entre el máximo y el mínimo como porcentaje de la apertura. La primera fecha queda sin variación.

# COMMAND ----------

by_date = Window.orderBy("trade_date")
daily_metrics = (
    bitcoin_daily
    .withColumn("previous_close", F.lag("daily_close").over(by_date))
    .withColumn(
        "daily_return_pct",
        (F.col("daily_close") / F.col("previous_close") - 1) * 100,
    )
    .withColumn(
        "intraday_range_pct",
        (F.col("daily_high") - F.col("daily_low")) / F.col("daily_open") * 100,
    )
    .withColumn("is_complete_day", F.col("minute_count") == 1440)
)

daily_table = f"{catalog}.{gold_schema}.bitcoin_daily_metrics"
daily_metrics.write.format("delta").mode("overwrite").saveAsTable(daily_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumen por sentimiento
# MAGIC
# MAGIC El resumen agrupa los días con sentimiento registrado. Las medianas de rango intradía y volumen se calculan con días de 1.440 velas.

# COMMAND ----------

gold_daily = spark.table(daily_table)
complete_day = F.col("is_complete_day")
daily_return = F.col("daily_return_pct")

sentiment_summary = (
    gold_daily
    .filter(F.col("sentiment_category").isNotNull())
    .groupBy("sentiment_category")
    .agg(
        F.count("*").alias("day_count"),
        F.count("daily_return_pct").alias("return_day_count"),
        F.count(F.when(complete_day, 1)).alias("full_day_count"),
        F.median("daily_return_pct").alias("median_daily_return_pct"),
        F.median(F.when(complete_day, F.col("intraday_range_pct"))).alias("median_intraday_range_pct"),
        F.median(F.when(complete_day, F.col("daily_volume"))).alias("median_daily_volume"),
        F.count(F.when(daily_return > 0, 1)).alias("up_days"),
        F.count(F.when(daily_return < 0, 1)).alias("down_days"),
    )
)

summary_table = f"{catalog}.{gold_schema}.sentiment_summary"
sentiment_summary.write.format("delta").mode("overwrite").saveAsTable(summary_table)

# COMMAND ----------

gold_summary = spark.table(summary_table)
display(gold_daily.orderBy("trade_date").limit(5))
display(gold_summary.orderBy("sentiment_category"))

print(f"{daily_table}: {gold_daily.count():,} rows")
print(f"{summary_table}: {gold_summary.count():,} rows")

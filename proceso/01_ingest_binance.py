# Databricks notebook source
# MAGIC %md
# MAGIC # Ingesta Bronze de Binance
# MAGIC
# MAGIC Se cargan las velas de BTC/USDT y se conserva la unidad original de sus marcas de tiempo.

# COMMAND ----------

dbutils.widgets.text("catalog", "catalog_smartdata", "Catalog")
dbutils.widgets.text("schema", "bitcoin_bronze", "Schema")
dbutils.widgets.text("raw_path", "abfss://delta-lake@adlsmartdata0811.dfs.core.windows.net/raw/bitcoin", "Raw path")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.types import DoubleType, IntegerType, LongType, StructField, StructType

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
raw_path = dbutils.widgets.get("raw_path").rstrip("/")

# COMMAND ----------

prices_schema = StructType([
    StructField("open_time", LongType()),
    StructField("open", DoubleType()),
    StructField("high", DoubleType()),
    StructField("low", DoubleType()),
    StructField("close", DoubleType()),
    StructField("volume", DoubleType()),
    StructField("close_time", LongType()),
    StructField("quote_asset_volume", DoubleType()),
    StructField("number_of_trades", LongType()),
    StructField("taker_buy_base_asset_volume", DoubleType()),
    StructField("taker_buy_quote_asset_volume", DoubleType()),
    StructField("ignore", IntegerType()),
])

# COMMAND ----------

file_name = "btcusdt_1m_2022_2025.csv"
prices = (
    spark.read
    .option("header", True)
    .schema(prices_schema)
    .csv(f"{raw_path}/binance/{file_name}")
)
prices = prices.withColumn("ingestion_date", current_timestamp())
prices = prices.withColumn("source_file", lit(file_name))

# COMMAND ----------

table_name = f"{catalog}.{schema}.binance_prices"
prices.write.format("delta").mode("overwrite").saveAsTable(table_name)

bronze_prices = spark.table(table_name)
display(bronze_prices.limit(5))
print(f"{table_name}: {bronze_prices.count():,} rows")

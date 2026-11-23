# Databricks notebook source
# MAGIC %md
# MAGIC # Ingesta Bronze de Fear & Greed
# MAGIC
# MAGIC Se carga el índice diario de Alternative.me con su puntuación y categoría originales.

# COMMAND ----------

dbutils.widgets.text("catalog", "catalog_smartdata", "Catalog")
dbutils.widgets.text("schema", "bitcoin_bronze", "Schema")
dbutils.widgets.text("raw_path", "abfss://delta-lake@adlsmartdata0811.dfs.core.windows.net/raw/bitcoin", "Raw path")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.types import IntegerType, LongType, StringType, StructField, StructType

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
raw_path = dbutils.widgets.get("raw_path").rstrip("/")

# COMMAND ----------

sentiment_schema = StructType([
    StructField("timestamp", LongType()),
    StructField("value", IntegerType()),
    StructField("value_classification", StringType()),
])

# COMMAND ----------

file_name = "fear_greed_2022_2025.csv"
sentiment = (
    spark.read
    .option("header", True)
    .schema(sentiment_schema)
    .csv(f"{raw_path}/alternative-me/{file_name}")
)
sentiment = sentiment.withColumn("ingestion_date", current_timestamp())
sentiment = sentiment.withColumn("source_file", lit(file_name))

# COMMAND ----------

table_name = f"{catalog}.{schema}.fear_greed_index"
sentiment.write.format("delta").mode("overwrite").saveAsTable(table_name)

bronze_sentiment = spark.table(table_name)
display(bronze_sentiment.limit(5))
print(f"{table_name}: {bronze_sentiment.count():,} rows")

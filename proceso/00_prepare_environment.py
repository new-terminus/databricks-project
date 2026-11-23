# Databricks notebook source
# MAGIC %md
# MAGIC # Preparación del ambiente
# MAGIC
# MAGIC Se comprueba la lectura de los dos CSV en Raw y se crean los esquemas del proyecto en Unity Catalog. El parámetro `raw_path` apunta a la carpeta `raw/bitcoin` del contenedor `delta-lake`, accesible con identidad administrada.

# COMMAND ----------

dbutils.widgets.text("catalog", "catalog_smartdata", "Catalog")
dbutils.widgets.text("raw_path", "abfss://delta-lake@adlsmartdata0811.dfs.core.windows.net/raw/bitcoin", "Raw path")

# COMMAND ----------

raw_path = dbutils.widgets.get("raw_path").strip().rstrip("/")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lectura de los archivos Raw
# MAGIC
# MAGIC Cada consulta muestra cinco filas del CSV de origen.

# COMMAND ----------

binance_path = f"{raw_path}/binance/btcusdt_1m_2022_2025.csv"
prices = spark.read.option("header", True).csv(binance_path)
display(prices.limit(5))

# COMMAND ----------

sentiment_path = f"{raw_path}/alternative-me/fear_greed_2022_2025.csv"
sentiment = spark.read.option("header", True).csv(sentiment_path)
display(sentiment.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Esquemas del proyecto
# MAGIC
# MAGIC Los esquemas se crean dentro del catálogo indicado. Las capas Bronze, Silver y Gold se cargan en sus respectivos notebooks.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG IDENTIFIER(:catalog);
# MAGIC CREATE SCHEMA IF NOT EXISTS bitcoin_bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS bitcoin_silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS bitcoin_gold;
# MAGIC
# MAGIC SHOW SCHEMAS LIKE 'bitcoin_*';

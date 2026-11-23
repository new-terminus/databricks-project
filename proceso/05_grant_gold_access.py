# Databricks notebook source
# MAGIC %md
# MAGIC # Permisos de lectura de Gold
# MAGIC
# MAGIC Se concede acceso de lectura al grupo `bitcoin_readers` sobre las dos tablas de Gold.

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT USE CATALOG ON CATALOG catalog_smartdata TO `bitcoin_readers`;
# MAGIC GRANT USE SCHEMA ON SCHEMA catalog_smartdata.bitcoin_gold TO `bitcoin_readers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE catalog_smartdata.bitcoin_gold.bitcoin_daily_metrics TO `bitcoin_readers`;
# MAGIC GRANT SELECT ON TABLE catalog_smartdata.bitcoin_gold.sentiment_summary TO `bitcoin_readers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANTS ON TABLE catalog_smartdata.bitcoin_gold.bitcoin_daily_metrics;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW GRANTS ON TABLE catalog_smartdata.bitcoin_gold.sentiment_summary;

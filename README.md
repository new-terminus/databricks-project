# Bitcoin y sentimiento del mercado

Proyecto de ingeniería de datos sobre BTC/USDT entre 2022 y 2025. Azure Databricks procesa las velas de Binance Vision y las cruza por fecha con el índice Fear & Greed de Alternative.me. El resultado se consulta en Power BI.

El alcance actual comprende la preparación del ambiente, el ETL de Raw a Gold y el [informe de Power BI](dashboard/README.md).

## ¿Qué preguntas responde?

- ¿Cómo cambió el cierre de Bitcoin en el periodo seleccionado?
- ¿Qué categorías de sentimiento coinciden con mayor rango intradía?
- ¿Cuántos días respaldan cada comparación y cómo se distribuyen por año?

## Arquitectura

```text
Binance Vision (velas por minuto) + Alternative.me (índice diario)
    → Raw en Azure Data Lake Storage Gen2
    → Bronze en Delta Lake
    → Silver en Delta Lake
    → Gold en Delta Lake
    → Power BI Desktop
```

Azure Databricks lee Raw mediante una ubicación externa de Unity Catalog. La credencial de almacenamiento usa la identidad administrada de un Access Connector. Las tablas se registran en el catálogo `catalog_smartdata`.

| Capa | Tablas | Qué se hace |
| --- | --- | --- |
| Bronze | `bitcoin_bronze.binance_prices`, `bitcoin_bronze.fear_greed_index` | Se cargan los dos CSV y se conservan los valores de origen. |
| Silver | `bitcoin_silver.binance_minutes`, `bitcoin_silver.bitcoin_daily` | Se unifican las marcas de tiempo en UTC, se quitan duplicados y se unen el mercado y el sentimiento por fecha. |
| Gold | `bitcoin_gold.bitcoin_daily_metrics`, `bitcoin_gold.sentiment_summary` | Se calculan el retorno diario y el rango intradía. Se resumen las métricas en cinco categorías de sentimiento. |

## Datos y resultados

| Dato | Cobertura |
| --- | --- |
| Velas BTC/USDT de Binance | 2.103.760 registros de un minuto en 48 archivos mensuales. |
| Fear & Greed de Alternative.me | 1.460 valores diarios. |
| Métricas diarias de Gold | 1.461 fechas de mercado. El cruce conserva una fecha sin sentimiento. |
| Resumen de sentimiento de Gold | Cinco categorías. El rango intradía mediano usa los días con 1.440 velas. |

El [directorio de datasets](datasets/README.md) detalla las fuentes, archivos incluidos y rutas de carga en ADLS.

## Ejecución en Azure Databricks

1. Se cargan los dos CSV completos en `delta-lake/raw/bitcoin/`, en las subcarpetas de cada fuente. La ubicación externa debe tener acceso a esta ruta con la identidad administrada.
2. En la carpeta Git de Azure Databricks se selecciona un clúster con acceso a Unity Catalog y se ejecutan los notebooks en este orden. Los widgets incluyen los valores del ambiente del proyecto.

   | Orden | Notebook | Resultado |
   | --- | --- | --- |
   | 1 | [00_prepare_environment.ipynb](proceso/00_prepare_environment.ipynb) | Comprueba los CSV en Raw y crea los esquemas. |
   | 2 | [01_ingest_binance.ipynb](proceso/01_ingest_binance.ipynb) | Carga las velas en Bronze. |
   | 3 | [02_ingest_fear_greed.ipynb](proceso/02_ingest_fear_greed.ipynb) | Carga el índice de sentimiento en Bronze. |
   | 4 | [03_transform_silver.ipynb](proceso/03_transform_silver.ipynb) | Obtiene las velas normalizadas y la serie diaria. Muestra las fechas con datos incompletos. |
   | 5 | [04_load_gold.ipynb](proceso/04_load_gold.ipynb) | Crea las dos tablas para el análisis. |

3. Se abre [bitcoin_sentimiento.pbix](dashboard/bitcoin_sentimiento.pbix) en Power BI Desktop. El archivo incluye una copia importada de las tablas Gold. Para actualizarla, Power BI requiere acceso al entorno de Azure Databricks.

## Power BI

- **Mercado** muestra el cierre diario, las cifras del periodo y la evolución de Fear & Greed. [Vista de Mercado](dashboard/bitcoin_mercado.png)
- **Sentimiento** compara el rango intradía y el retorno diario con filtros de año y categoría. [Vista de Sentimiento](dashboard/bitcoin_sentimiento.png)

El [detalle del informe](dashboard/README.md) describe los filtros y cómo se calculan las métricas.

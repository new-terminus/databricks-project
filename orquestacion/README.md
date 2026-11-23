# Job de Bitcoin

[wf_bitcoin.json](wf_bitcoin.json) adapta al proyecto las tareas y dependencias de `wf_structure.txt`, de la sesión 13. En clase, `script3.yml` crea y ejecuta el Job mediante la API de Databricks. Los pasos de esta guía sirven para comprobar el Job `bitcoin_etl` desde la interfaz antes de automatizarlo.

| Tarea | Notebook | Depende de |
| --- | --- | --- |
| `prepare_environment` | [00_prepare_environment](../prep-amb/00_prepare_environment.ipynb) | — |
| `ingest_binance` | [01_ingest_binance](../proceso/01_ingest_binance.ipynb) | `prepare_environment` |
| `ingest_fear_greed` | [02_ingest_fear_greed](../proceso/02_ingest_fear_greed.ipynb) | `prepare_environment` |
| `transform_silver` | [03_transform_silver](../proceso/03_transform_silver.ipynb) | `ingest_binance`, `ingest_fear_greed` |
| `load_gold` | [04_load_gold](../proceso/04_load_gold.ipynb) | `transform_silver` |

## Primera ejecución

1. Se sincroniza la carpeta Git de `databricks-project` en Databricks.
2. En **Jobs & Pipelines** se crea el Job `bitcoin_etl`. Se agrega cada tarea como **Notebook**, se elige la fuente **Workspace** y se selecciona el notebook en la carpeta Git. El cómputo de las cinco tareas es `ClusterSD`.
3. Se configuran las dependencias según la tabla. Los widgets de los notebooks ya incluyen el catálogo, los esquemas y la ruta de Raw.
4. Se ejecuta con **Run now**. En **Runs** se comprueba que las cinco tareas terminen correctamente. La salida de `load_gold` debe mostrar 1.461 filas diarias y 5 categorías de sentimiento.

Si se crea el Job desde el JSON, se completan `<CLUSTER_ID>` y `<WORKSPACE_REPO_PATH>` con el ID del cómputo y la ruta real de la carpeta Git. En la interfaz ambos valores se seleccionan directamente.

La captura `bitcoin_etl_run.png` debe mostrar el gráfico de las tareas y el estado de la ejecución.

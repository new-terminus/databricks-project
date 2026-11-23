# Preparación del ambiente

El proyecto lee los CSV de Raw en Azure Data Lake Storage Gen2. Unity Catalog usa una ubicación externa y una credencial de almacenamiento vinculada a la identidad administrada del Access Connector de Azure Databricks.

| Recurso | Configuración del proyecto |
| --- | --- |
| Contenedor y carpeta de Raw | `delta-lake/raw/bitcoin/` |
| Ruta de Raw | `abfss://delta-lake@adlsmartdata0811.dfs.core.windows.net/raw/bitcoin` |
| Catálogo | `catalog_smartdata` |
| Esquemas | `bitcoin_bronze`, `bitcoin_silver` y `bitcoin_gold` |

## Configuración y prueba

1. En Azure se configura el Access Connector con identidad administrada y se asigna a esa identidad el rol `Storage Blob Data Contributor` para el almacenamiento de Raw.
2. En Unity Catalog se crea una credencial de tipo **Azure Managed Identity** con el ID del Access Connector. La ubicación externa usa esa credencial y cubre la ruta de Raw. El usuario que ejecuta la ingesta necesita `READ FILES` en la ubicación.
3. Se cargan los [CSV completos](../datasets/README.md#capa-raw) en sus respectivas subcarpetas de Raw. Se ejecuta [00_prepare_environment.ipynb](00_prepare_environment.ipynb) en un clúster con acceso a Unity Catalog para leer cinco filas de cada fuente y crear los esquemas. El catálogo y la ruta ya están definidos en los widgets.
4. Se comprueba que aparezcan las filas de ambos CSV y los tres esquemas.

La [hoja de aprovisionamiento](../certificaciones/03-databricks-aprovisionamiento.pdf) contiene el detalle de la configuración con identidad administrada.

# Permisos de lectura de Gold

El grupo de cuenta `bitcoin_readers` ya está asignado al workspace. [Captura del grupo](../evidencias/bitcoin_readers_group.png)

1. En la carpeta Git `databricks-project` de Databricks se sincroniza la rama `main`.
2. Se abre [grant_gold_access.ipynb](grant_gold_access.ipynb) en `seguridad/`, se selecciona `ClusterSD` y se pulsa **Run all**.
3. En las dos últimas celdas se revisa que `bitcoin_readers` tenga `SELECT` sobre `bitcoin_daily_metrics` y `sentiment_summary`. Se captura la salida de `SHOW GRANTS` de cada tabla.

El notebook usa las celdas SQL de permisos y comprobación del ejercicio `4. Grants-Medallion` de la sesión 11 con los nombres del proyecto.

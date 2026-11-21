# Datasets

Los datos del proyecto cubren 2022–2025. El repositorio incluye una muestra de las velas de Bitcoin y el índice de sentimiento completo del periodo.

Los 48 ZIP mensuales de Binance y sus archivos de comprobación están en [binance/historical/](binance/historical/).

| Fuente | CSV en el repositorio | Periodo | Filas |
| --- | --- | --- | ---: |
| Binance Vision | [Muestra BTC/USDT por minuto](binance/btcusdt_sample.csv) | Enero a marzo de 2025 | 129.600 |
| Alternative.me | [Fear & Greed 2022–2025](alternative-me/fear_greed_2022_2025.csv) | Enero de 2022 a diciembre de 2025 | 1.460 |

## Fuentes de descarga

- **Binance Vision** · Archivos mensuales de BTC/USDT a un minuto. <https://data.binance.vision/?prefix=data/spot/monthly/klines/BTCUSDT/1m/>
- **Alternative.me** · Historial del índice Fear & Greed en JSON. <https://api.alternative.me/fng/?limit=0>

## Capa Raw

Los dos CSV completos están en `datasets/raw/upload/`. En Azure Portal se abre el contenedor `delta-lake` y se carga cada archivo en su carpeta dentro de `raw/bitcoin/`.

| Archivo local | Registros | Ruta en ADLS |
| --- | ---: | --- |
| `datasets/raw/upload/binance/btcusdt_1m_2022_2025.csv` | 2.103.760 velas por minuto | `delta-lake/raw/bitcoin/binance/btcusdt_1m_2022_2025.csv` |
| `datasets/raw/upload/alternative-me/fear_greed_2022_2025.csv` | 1.460 valores diarios | `delta-lake/raw/bitcoin/alternative-me/fear_greed_2022_2025.csv` |


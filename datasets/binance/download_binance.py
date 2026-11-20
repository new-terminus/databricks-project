"""Descarga y verifica el histórico de BTC/USDT por minuto."""

import hashlib
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


SOURCE_URL = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / ".resources" / "binance"


def download(url):
    with urlopen(url, timeout=30) as response:
        return response.read()


def download_month(year, month):
    file_name = f"BTCUSDT-1m-{year}-{month:02d}"
    archive_url = f"{SOURCE_URL}/{file_name}.zip"
    checksum = download(f"{archive_url}.CHECKSUM").decode("ascii").split()[0].lower()
    archive_bytes = download(archive_url)
    if hashlib.sha256(archive_bytes).hexdigest() != checksum:
        raise ValueError(f"SHA-256 mismatch for {file_name}.zip.")

    csv_name = f"{file_name}.csv"
    destination = OUTPUT_DIR / csv_name
    temporary_file = destination.with_suffix(".tmp")
    with ZipFile(BytesIO(archive_bytes)) as archive:
        temporary_file.write_bytes(archive.read(csv_name))
    temporary_file.replace(destination)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for year in range(2022, 2026):
        for month in range(1, 13):
            download_month(year, month)
    print(f"Saved 48 verified CSV files to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()

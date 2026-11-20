"""Descarga el índice Fear & Greed para el periodo del proyecto."""

import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import urlopen


SOURCE_URL = "https://api.alternative.me/fng/?limit=0"
START_DATE = date(2022, 1, 1)
END_DATE = date(2026, 1, 1)
OUTPUT_DIR = Path(__file__).resolve().parents[2] / ".resources" / "alternative-me"


def main():
    with urlopen(SOURCE_URL, timeout=30) as response:
        payload = json.load(response)
    if payload["metadata"]["error"]:
        raise ValueError(f"Alternative.me API error: {payload['metadata']['error']}")

    records_by_date = {}
    for record in payload["data"]:
        record_date = datetime.fromtimestamp(int(record["timestamp"]), timezone.utc).date()
        if START_DATE <= record_date < END_DATE:
            if record_date in records_by_date:
                raise ValueError(f"Alternative.me returned duplicate records for {record_date}.")
            records_by_date[record_date] = record
    if not records_by_date:
        raise ValueError("Alternative.me returned no records for the selected period.")

    records = [records_by_date[day] for day in sorted(records_by_date)]
    snapshot = {"name": payload["name"], "data": records}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / "fear_greed_2022-2025.json"
    temporary_file = destination.with_suffix(".tmp")
    temporary_file.write_bytes((json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    temporary_file.replace(destination)
    print(f"Saved {len(records):,} records to {destination}.")


if __name__ == "__main__":
    main()

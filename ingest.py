import os
import json
import psycopg2
from glob import glob
from datetime import datetime


# DB config
DB_CONFIG = {
    "dbname": "katapay",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": 5432
}

# Create table query
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw_transactions (
    event_id    TEXT PRIMARY KEY,
    event_type  TEXT,
    timestamp   TIMESTAMP,
    user_id     TEXT,
    provider_id TEXT,
    amount      NUMERIC,
    currency    TEXT
);
"""

# Insert query with deduplication
INSERT_SQL = """
INSERT INTO raw_transactions (
    event_id, event_type, timestamp, user_id, provider_id, amount, currency
) VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (event_id) DO NOTHING;
"""


def parse_event(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        events = data if isinstance(data, list) else [data]

        rows = []
        for event in events:
            rows.append((
                event.get("event_id"),
                event.get("event_type"),
                event.get("timestamp"),
                event.get("user_id"),
                event.get("provider_id"),
                event.get("amount"),
                event.get("currency"),
            ))
        return rows


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    all_files = glob("data/events/*.json")

    inserted = 0
    for file in all_files:
        rows = parse_event(file)
        for row in rows:
            try:
                cur.execute(INSERT_SQL, row)
                inserted += 1
            except Exception as e:
                print(f"Error in {file}: {e}")

    conn.commit()
    print(f"[✓] Ingest complete. Rows inserted (excluding duplicates): {inserted}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()


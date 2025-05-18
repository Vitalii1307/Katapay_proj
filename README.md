# Katapay: Event-Based Transaction Analytics

This project processes and analyzes JSON-based payment events (authorization and settlement) using:

- PostgreSQL (Docker)
- Python (`ingest.py`)
- dbt (Data Build Tool)
- Metabase (BI Dashboard)

---

## 1. Launch the stack (PostgreSQL + Metabase)

Start the services using Docker Compose:

```bash
docker compose up -d
```

This will:

* Start **PostgreSQL** at `localhost:5432` with:

  * **user:** `admin`
  * **password:** `admin`
  * **database:** `katapay`
* Start **Metabase** at: [http://localhost:3000](http://localhost:3000)

Initial database is created from `init.sql`.

## 2. How to run ingestion (`python ingest.py`)

### 🔧 Requirements

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> `requirements.txt` should include:

```txt
psycopg2-binary
```

### ▶️ Run ingestion:

```bash
python ingest.py
```

This script:

* Reads all `*.json` files from `data/events/`
* Loads them into table `raw_transactions` in `katapay` database
* Skips duplicates via `event_id` primary key

---

## 📊 3. How to run dbt (`dbt run`, `dbt test`, `dbt docs serve`)

### 📁 Move into dbt project:

```bash
cd katapay_dbt
```

### ▶️ Run dbt:

```bash
dbt run         # Builds fact_transactions and dim_time
dbt test        # Runs tests on event_id, timestamp, event_type
dbt docs generate
dbt docs serve  # Opens docs in browser at http://localhost:8000
```

---

## 📈 4. How to view the dashboard in Metabase

### 🔌 First-time Metabase setup

1. Visit [http://localhost:3000](http://localhost:3000)
2. Create admin account
3. When prompted to **add a database**, use:

```
Database type: PostgreSQL
Name: katapay
Host: host.docker.internal      (or use container IP () on Linux)
Port: 5432
Database name: katapay
Username: admin
Password: admin
```

> If on Linux and `host.docker.internal` doesn't work, run:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' katapay-db
```

Use that IP as host.

---

### 📊 Building a chart

1. Go to **Browse data** → `katapay` → `fact_transactions`
2. Click **+ New → Simple Question**
3. Summarize:

   * `Count of rows` (filtered where `event_type = authorization`)
   * `Count of rows` (filtered where `event_type = settlement`)
4. Group by: `timestamp` (by Day)
5. Visualize → Choose **Line chart**
6. (Optional) Add custom column:

   ```text
   [settlements] / [authorizations]
   ```
7. Save chart to a dashboard

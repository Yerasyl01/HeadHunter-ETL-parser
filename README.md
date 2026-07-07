# HH ETL

A Python Bronze/Silver ETL pipeline for extracting vacancy data from the HeadHunter (HH) API, storing raw vacancy documents in MongoDB (Bronze), and transforming them into an analytical Parquet dataset (Silver) using Polars.

The project follows a modular architecture with concurrent ingestion, Redis-backed work queues, and a recursive search planner that overcomes the HH API's 2,000-result search limitation.

---

## Features

* Recursive search planning for large result sets
* Concurrent producer/consumer ingestion pipeline
* Redis-backed vacancy queue
* Bronze layer stored in MongoDB
* Silver analytical dataset stored as Parquet
* Batch-based transformation with Polars
* Duplicate detection using MongoDB unique indexes
* Structured logging
* Docker and Docker Compose support
* Interface-based architecture for easy extension

---

## Technology Stack

| Component        | Technology                     |
| ---------------- | ------------------------------ |
| Language         | Python 3.13                    |
| Data Processing  | Polars                         |
| Source           | HeadHunter (HH) API            |
| Bronze Storage   | MongoDB                        |
| Queue            | Redis                          |
| Silver Storage   | Apache Parquet                 |
| Containerization | Docker & Docker Compose        |
| Concurrency      | `ThreadPoolExecutor`           |
| Configuration    | Environment variables (`.env`) |
| Logging          | Python `logging`               |

---

## Architecture

```text
                  HH API
                     │
                     ▼
             SearchPlanner
                     │
                     ▼
            VacancyProducer
                     │
                     ▼
               Redis Queue
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    VacancyConsumer      VacancyConsumer
          │                     │
          └──────────┬──────────┘
                     ▼
          Bronze Transformer
                     │
                     ▼
           MongoDB (Bronze)
                     │
                     ▼
            Silver Pipeline
                     │
                     ▼
          Silver Transformer
                     │
                     ▼
        Parquet Dataset (Silver)
```

---

## Data Layers

### Bronze

* Raw vacancy documents returned by the HH API
* Stored in MongoDB
* Preserves the original API structure
* Serves as the source of truth for downstream processing

### Silver

* Flattened analytical dataset
* Stored as partitioned Parquet files
* Optimized for analytics with Polars, DuckDB, Pandas and BI tools
* Schema documented in `silver/SCHEMA.md`

---

## Project Structure

```text
hh-etl
├── api/              # HH API client
├── bronze/           # Bronze pipeline
├── contracts/        # ETL interfaces
├── data/             # Generated Parquet dataset
├── db/               # MongoDB and Redis managers
├── exceptions/       # Custom exceptions
├── loaders/          # Data loaders
├── models/           # Shared models and types
├── producer/         # Search planning and extraction
├── queues/           # Queue implementations
├── silver/           # Silver pipeline and schema
├── utils/            # Logging, retry, timer
├── workers/          # Queue consumers
├── compose.yaml
├── Dockerfile
├── config.py
├── main.py           # Pipeline orchestrator
└── requirements.txt
```

---

## Requirements

* Python 3.13+
* MongoDB
* Redis

or simply Docker and Docker Compose.

---

## Configuration

Create a `.env` file from `.env.example`.

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=hh_etl

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_QUEUE_NAME=hh:vacancies
WORKER_COUNT=5

# HH
HH_BASE_URL=https://almaty.hh.kz
HH_SEARCH_PATH=/search/vacancy
REQUEST_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOGS_TO_KEEP=10

# Browser User-Agent
USER_AGENT=
```

`USER_AGENT` should contain a modern browser User-Agent string.

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start MongoDB and Redis, then run:

```bash
python main.py
```

The pipeline will:

1. Extract vacancies from the HH API.
2. Store raw documents in MongoDB (Bronze).
3. Read Bronze data in batches.
4. Transform the data into the Silver schema.
5. Write the analytical dataset as Parquet files under `data/vacancies/`.

---

## Running with Docker

Build and start the services:

```bash
docker compose up --build
```

---

## Pipeline

### Bronze Stage

1. The SearchPlanner recursively partitions large searches until each request contains at most 2,000 vacancies.
2. The VacancyProducer downloads every page for each planned search.
3. Vacancies are pushed into a Redis queue.
4. Multiple worker threads consume vacancies concurrently.
5. Each vacancy is transformed into the Bronze schema.
6. Raw vacancy documents are stored in MongoDB.

### Silver Stage

1. Bronze documents are read from MongoDB in batches.
2. Relevant fields are flattened into an analytical schema.
3. Nested structures are normalized.
4. Data types are converted where necessary.
5. The resulting dataset is written as partitioned Parquet files.

---

## Duplicate Handling

Search partitions may overlap, causing the same vacancy to be encountered multiple times during extraction.

MongoDB uses a unique index on the vacancy ID, allowing duplicate documents to be skipped automatically while preserving a complete extraction process.

---

## Logging

The application produces structured logs including:

* Search planning
* Page downloads
* Worker activity
* Duplicate statistics
* ETL summary

Example:

```text
Queued 72064 vacancies

Worker 1: 14450 loaded (1526 duplicates)
Worker 2: 14402 loaded (1578 duplicates)
Worker 3: 14395 loaded (1572 duplicates)
Worker 4: 14397 loaded (1543 duplicates)
Worker 5: 14415 loaded (1580 duplicates)

ETLStats(
    extracted=72059,
    transformed=72059,
    loaded=72059,
    duplicates=7799,
    failed=0
)
```

---

## Future Work

Planned improvements include:

* Incremental Bronze → Silver synchronization
* Partitioned Parquet datasets
* Gold analytical layer
* Workflow orchestration
* Data quality validation
* Monitoring and metrics
* Power BI dashboards

---

## License

This project is provided for educational and research purposes.

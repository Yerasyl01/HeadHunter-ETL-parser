# HH ETL Pipeline

A production-oriented ETL pipeline that extracts vacancy data from the HeadHunter (HH) API, transforms it into a normalized format, and loads it into MongoDB using a concurrent worker architecture backed by Redis.

## Features

* Extracts vacancies from the HH API
* Producer–consumer architecture
* Redis-backed work queue
* Concurrent workers using `ThreadPoolExecutor`
* MongoDB storage with indexes
* Configurable through environment variables
* Docker Compose support
* Modular and extensible design
* Structured logging
* Automatic retry handling for transient failures

---

## Architecture

```
          HH API
             │
             ▼
      HHClient (Producer)
             │
             ▼
      Redis Vacancy Queue
             │
   ┌─────────┴─────────┐
   │         │         │
Worker 1  Worker 2  Worker N
   │         │         │
   ▼         ▼         ▼
Transformer → Loader → MongoDB
```

Pipeline stages:

1. **Extract**

   * Downloads vacancy pages from the HH API.
   * Pushes raw vacancies into a Redis queue.

2. **Transform**

   * Converts raw HH vacancy objects into normalized documents.

3. **Load**

   * Inserts transformed documents into MongoDB.
   * Duplicate documents are ignored.

---

## Project Structure

```
hh-etl
├── api/                 # HH API client
├── contracts/           # Interfaces (ports)
├── db/                  # MongoDB and Redis clients
├── exceptions/          # Custom exceptions
├── loaders/             # Data loaders
├── models/              # Data models
├── producer/            # Vacancy producer
├── queues/              # Queue implementations
├── transformers/        # Data transformers
├── utils/               # Logging, retry, timing
├── workers/             # Consumer workers
├── compose.yaml
├── Dockerfile
├── config.py
├── main.py
└── requirements.txt
```

---

## Technologies

* Python 3
* MongoDB
* Redis
* Docker
* Docker Compose

---

## Configuration

Create a `.env` file from `.env.example`.

Example:

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=hh_etl

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_QUEUE_NAME=hh:vacancies
WORKER_COUNT=5

# HH API
HH_BASE_URL=https://almaty.hh.kz
HH_SEARCH_PATH=/search/vacancy
REQUEST_TIMEOUT=30

# Logging
LOG_LEVEL=INFO

# User Agent
USER_AGENT=
```

### Environment variables

| Variable           | Description                         |
| ------------------ | ----------------------------------- |
| `MONGO_URI`        | MongoDB connection string           |
| `MONGO_DATABASE`   | Database name                       |
| `REDIS_URL`        | Redis connection string             |
| `REDIS_QUEUE_NAME` | Queue used by producer and workers  |
| `WORKER_COUNT`     | Number of concurrent worker threads |
| `HH_BASE_URL`      | HH API base URL                     |
| `HH_SEARCH_PATH`   | Vacancy search endpoint             |
| `REQUEST_TIMEOUT`  | HTTP request timeout (seconds)      |
| `LOG_LEVEL`        | Logging level                       |
| `USER_AGENT`       | Optional custom User-Agent          |

---

## Running with Docker

Build and start the infrastructure:

```bash
docker compose up --build
```

Run the ETL:

```bash
docker compose run --rm app
```

---

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start MongoDB and Redis.

Run:

```bash
python main.py
```

---

## How It Works

When the application starts it:

1. Connects to MongoDB.
2. Connects to Redis.
3. Clears the Redis queue.
4. Starts worker threads.
5. Downloads vacancies from the HH API.
6. Pushes each vacancy into Redis.
7. Workers continuously:

   * read vacancies,
   * transform them,
   * load them into MongoDB.
8. After all vacancies have been queued, the producer sends termination signals.
9. Workers finish processing remaining items and exit.
10. The application prints ETL statistics.

---

## Main Components

### HHClient

Responsible for communicating with the HH API.

### VacancyProducer

Downloads vacancies and pushes them into Redis.

### RedisVacancyQueue

Implements the producer–consumer queue.

### VacancyConsumer

Consumes vacancies from Redis and performs transformation and loading.

### HHVacancyTransformer

Converts raw HH vacancy objects into normalized MongoDB documents.

### MongoVacancyLoader

Stores transformed documents in MongoDB.

---

## Concurrency Model

The application uses a producer–consumer architecture.

* One producer downloads vacancies.
* Multiple consumers process vacancies concurrently.
* Redis provides a shared queue between producer and workers.
* `ThreadPoolExecutor` manages worker threads.

The number of workers is configured via:

```env
WORKER_COUNT=5
```

---

## Logging

The application reports:

* database connections
* queue activity
* worker progress
* duplicate documents
* ETL summary
* unexpected failures

Example:

```
Queued 897231 vacancies

Worker 1: 179501 loaded (821 duplicates)
Worker 2: 179486 loaded (803 duplicates)
Worker 3: 179420 loaded (815 duplicates)
Worker 4: 179378 loaded (799 duplicates)
Worker 5: 179402 loaded (808 duplicates)

ETLStats(
    loaded=897187,
    duplicates=4046
)
```

---

## Future Improvements

Possible extensions include:

* Scheduled execution (cron or scheduler)
* Incremental synchronization
* Celery workers
* Data enrichment
* Additional data sources
* Metrics and monitoring
* Power BI dashboards
* Automated tests

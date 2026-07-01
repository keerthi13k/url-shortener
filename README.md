🔗 URL Shortener — Production-Grade Cross-Domain System

```bash
cat > /Users/keerthi/url-shortener/README.md << 'EOF'
# 🔗 URL Shortener — Production-Grade Cross-Domain System

> A full-stack URL shortener built with **SDE + Data Engineering + DevOps** layers — designed to demonstrate production-level thinking across three engineering domains.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green) ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-7.4.0-black) ![PySpark](https://img.shields.io/badge/PySpark-3.5.0-orange) ![dbt](https://img.shields.io/badge/dbt-1.11-red) ![Airflow](https://img.shields.io/badge/Airflow-2.10.4-blue) ![Docker](https://img.shields.io/badge/Docker-Compose-blue)

---

## 🏗️ Architecture Overview

```
User clicks short URL
        │
        ▼
┌─────────────────┐
│   FastAPI App   │  ← REST API + WebSocket live feed
│  PostgreSQL DB  │  ← stores URLs + click events
│   Redis Cache   │  ← sub-millisecond redirects
└────────┬────────┘
         │ Kafka Producer
         ▼
┌─────────────────┐
│  Apache Kafka   │  ← real-time event stream (url-clicks topic)
└────────┬────────┘
         │ PySpark Consumer
         ▼
┌─────────────────┐
│ PySpark Pipeline│  ← batch analytics processing
│   dbt Models    │  ← SQL transformations + tests
│ Apache Airflow  │  ← hourly pipeline orchestration
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  url_analytics  │  ← aggregated analytics table in PostgreSQL
│  (PostgreSQL)   │
└─────────────────┘
```

---

## 🧱 Tech Stack

### Phase 1 — SDE Core
| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | REST endpoints + WebSocket |
| Database | PostgreSQL 16 | URL + click event storage |
| Cache | Redis | Fast redirects, rate limiting |
| Message Queue | Apache Kafka | Real-time click event streaming |
| Live Feed | WebSockets | Live analytics dashboard |

### Phase 2 — Data Engineering
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Stream Processing | PySpark 3.5.0 | Batch analytics from Kafka events |
| Transformations | dbt | SQL models + data tests |
| Orchestration | Apache Airflow 2.10.4 | Hourly pipeline scheduling |

### Phase 3 — DevOps
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker + Docker Compose | Full stack in one command |
| CI/CD | GitHub Actions | Auto-deploy on push _(coming soon)_ |
| Monitoring | Grafana + Prometheus | Observability _(coming soon)_ |

---

## 📁 Project Structure

```
url-shortener/
├── app/                        # FastAPI application
│   ├── main.py                 # App entry point
│   ├── routes.py               # API endpoints
│   ├── models.py               # PostgreSQL models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # DB connection
│   ├── cache.py                # Redis caching
│   ├── kafka_producer.py       # Kafka event publisher
│   └── websocket_manager.py    # WebSocket live feed
│
├── pipeline/
│   ├── spark/
│   │   ├── kafka_consumer.py       # Consumes click events from Kafka
│   │   └── analytics_processor.py  # PySpark aggregations → PostgreSQL
│   └── dbt/
│       └── url_analytics/
│           └── models/analytics/
│               ├── url_click_summary.sql   # dbt transformation model
│               ├── schema.yml              # column tests
│               └── sources.yml             # source definitions
│
├── airflow/
│   └── dags/
│       └── url_analytics_pipeline.py  # Hourly Airflow DAG
│
├── docker-compose.yml          # Kafka + Zookeeper setup
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12
- PostgreSQL 16
- Redis
- Docker + Docker Compose
- Java 22 (for PySpark)

### 1. Clone the repo
```bash
git clone https://github.com/keerthi13k/url-shortener.git
cd url-shortener
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start services
```bash
# Start PostgreSQL + Redis
brew services start postgresql@16
brew services start redis

# Start Kafka + Zookeeper
docker-compose up -d
```

### 4. Start the API
```bash
uvicorn app.main:app --reload
```

API will be live at: **http://localhost:8000**
Swagger docs at: **http://localhost:8000/docs**

### 5. Start the Data Pipeline
```bash
# Terminal 1 — Kafka consumer
python pipeline/spark/kafka_consumer.py

# Terminal 2 — Analytics processor
python pipeline/spark/analytics_processor.py
```

### 6. Start Airflow
```bash
export AIRFLOW_HOME=/Users/keerthi/url-shortener/airflow ```set AIRFLOW_HOME to your project's airflow directory```
airflow webserver --port 8080 &
airflow scheduler &
```

Airflow UI at: **http://localhost:8080** (admin / admin123)

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shorten` | Create a short URL |
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/analytics/{short_code}` | Get click analytics |
| `WS` | `/ws/analytics` | Live click feed via WebSocket |

---

## 📊 Data Pipeline Flow

```
Kafka Topic: url-clicks
        ↓
kafka_consumer.py     → writes raw events to PostgreSQL (click_events table)
        ↓
analytics_processor.py → PySpark aggregations → url_analytics table
        ↓
dbt run               → url_click_summary model → tests + transformations
        ↓
Airflow DAG           → schedules all above every hour (@hourly)
```

---

## 🎯 Key Design Decisions

**Why Redis over in-memory cache?**
Redis survives app restarts and works across multiple instances — critical for production horizontal scaling.

**Why Kafka over direct DB writes for click events?**
Decouples the redirect (latency-critical) from analytics (batch-ok). A slow analytics write never delays a user redirect.

**Why PySpark over pandas?**
Built to scale — the same analytics_processor.py works on 100 rows or 100 million rows without code changes.

**Why dbt over raw SQL scripts?**
dbt gives version-controlled, testable, documented SQL. Schema tests run automatically and catch data quality issues before they reach dashboards.

**Why Airflow over a cron job?**
Airflow gives retry logic, dependency management, and a UI to monitor pipeline health — a cron job gives none of that.

---

## 👩‍💻 Author

**Keerthi K**
[GitHub](https://github.com/keerthi13k) • [LinkedIn](https://www.linkedin.com/in/keerthiperiyasamy/)

---

## 📌 Roadmap

- [x] Phase 1 — FastAPI + PostgreSQL + Redis + Kafka + WebSockets
- [x] Phase 2 — PySpark + dbt + Airflow
- [x] Phase 3 — Docker Compose
- [ ] Phase 3 — Kubernetes (HPA + rolling deployments)
- [ ] Phase 3 — GitHub Actions CI/CD
- [ ] Phase 3 — Grafana + Prometheus monitoring
- [ ] Phase 4 — Live deployment + documentation
EOF
```

Then push it:

```bash
git add README.md
git commit -m "Add detailed README with architecture, setup guide, and design decisions"
git push origin main
```


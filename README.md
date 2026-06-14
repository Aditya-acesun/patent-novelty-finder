# 🔬 Patent Novelty & Research Gap Finder

AI-powered system for patent novelty scoring, research gap analysis, and innovation suggestions — built with a full-stack RAG pipeline.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 18 + TypeScript + Tailwind + ShadCN + React Query |
| Backend | Node.js + Express + JWT + RBAC + Swagger |
| AI Service | FastAPI + Celery + Sentence Transformers + XGBoost + HDBSCAN + Prophet |
| Vector DB | Qdrant |
| Task Queue | Celery + Redis |
| Database | MongoDB Atlas |

## Quick Start

### Prerequisites
- Docker + Docker Compose
- Node.js 20+
- Python 3.11+

### 1. Clone & configure
```bash
git clone <repo-url>
cd patent-novelty-finder
make setup        # creates .env from .env.example
# → Edit .env and fill in MONGODB_URI, JWT_SECRET, ANTHROPIC_API_KEY
```

### 2. Start all services
```bash
make up           # starts everything in background
make logs         # tail all logs
```

### 3. Access
| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:4000/api |
| Swagger Docs | http://localhost:4000/api/docs |
| AI Service | http://localhost:8000 |
| AI Docs | http://localhost:8000/docs |
| Qdrant UI | http://localhost:6333/dashboard |

## Build Phases

| Phase | What gets built |
|---|---|
| 0 ✅ | Folder scaffold, Docker, env, Makefile |
| 1 | Qdrant + Redis infra validation |
| 2 | Node backend: JWT auth, RBAC, MongoDB models, Swagger |
| 3 | React frontend: Auth UI, dashboard shell, React Query |
| 4 | PDF ingestion: PyMuPDF → OCR → embed → Qdrant |
| 5 | Hybrid search: BM25 + dense + BGE reranker |
| 6 | Novelty scoring: XGBoost + SciBERT + PatentSBERTa |
| 7 | Topic clusters (HDBSCAN) + trend forecast (Prophet) |
| 8 | RAG pipeline → Gap + Novelty + Innovation reports |
| 9 | Polish, Nginx, production deploy |

## Useful Commands
```bash
make up              # start everything
make down            # stop everything
make logs s=backend  # logs for a specific service
make restart s=ai-service
make clean           # wipe all volumes (⚠️ deletes data)
make swagger         # open Swagger UI in browser
make qdrant-ui       # open Qdrant dashboard
```

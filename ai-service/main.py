from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────
    print("🚀 AI Service starting up...")
    try:
        from app.core.qdrant_client import ensure_collections
        ensure_collections()
        print("✅ Qdrant collections ready")
    except Exception as e:
        print(f"⚠️  Qdrant init failed (will retry on first request): {e}")
    yield
    # ── Shutdown ─────────────────────────────────────────────────
    print("👋 AI Service shutting down...")


app = FastAPI(
    title="Patent Novelty AI Service",
    description="ML/NLP/RAG engine for patent novelty & research gap analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "patent-novelty-ai"}


@app.get("/infra/status")
async def infra_status():
    """Phase 1: Check all infra connections."""
    status = {}

    # Qdrant
    try:
        from app.core.qdrant_client import get_qdrant_client
        client = get_qdrant_client()
        collections = [c.name for c in client.get_collections().collections]
        status["qdrant"] = {"status": "ok", "collections": collections}
    except Exception as e:
        status["qdrant"] = {"status": "error", "detail": str(e)}

    # Redis
    try:
        import redis, os
        r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
        r.ping()
        status["redis"] = {"status": "ok"}
    except Exception as e:
        status["redis"] = {"status": "error", "detail": str(e)}

    all_ok = all(v["status"] == "ok" for v in status.values())
    return {"overall": "ok" if all_ok else "degraded", "services": status}


# Routers added per phase:
# Phase 4: from app.api import embed, doc_processing
# Phase 5: from app.api import search
# Phase 6: from app.api import novelty
# Phase 7: from app.api import cluster, trend
# Phase 8: from app.api import rag

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

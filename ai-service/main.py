from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Patent Novelty AI Service",
    description="ML/NLP/RAG engine for patent novelty & research gap analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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

# Routers will be added per phase:
# Phase 4: from app.api import embed, doc_processing
# Phase 5: from app.api import search
# Phase 6: from app.api import novelty
# Phase 7: from app.api import cluster, trend
# Phase 8: from app.api import rag

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

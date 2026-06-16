"""
Phase 1: Qdrant client wrapper
Shared across all AI service modules.
"""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "patents")
VECTOR_SIZE = 1024  # bge-large-en-v1.5

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    return _client


def ensure_collections():
    """Create collections if they don't exist. Called at startup."""
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]

    for name in [COLLECTION_NAME, "research_papers"]:
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            # Payload indexes for filtering
            for field, schema in [
                ("domain", PayloadSchemaType.KEYWORD),
                ("year", PayloadSchemaType.INTEGER),
                ("novelty_score", PayloadSchemaType.FLOAT),
            ]:
                client.create_payload_index(
                    collection_name=name,
                    field_name=field,
                    field_schema=schema,
                )
            print(f"✅ Qdrant: created collection '{name}'")
        else:
            print(f"ℹ️  Qdrant: collection '{name}' already exists")

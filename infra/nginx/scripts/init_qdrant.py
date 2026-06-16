"""
Phase 1: Qdrant Collection Initializer
Run once to create the patents vector collection.
Usage: python scripts/init_qdrant.py
"""

import os
import sys
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
)

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "patents")

# bge-large-en-v1.5 produces 1024-dim vectors
# all-mpnet-base-v2 produces 768-dim vectors
# We use 1024 (bge-large) as primary
VECTOR_SIZE = 1024


def init_collections(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]

    # ── patents collection (primary) ──────────────────────────────
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        print(f"✅ Created collection: '{COLLECTION_NAME}' (dim={VECTOR_SIZE}, cosine)")
    else:
        print(f"ℹ️  Collection '{COLLECTION_NAME}' already exists — skipping")

    # ── research_papers collection ────────────────────────────────
    if "research_papers" not in existing:
        client.create_collection(
            collection_name="research_papers",
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        print("✅ Created collection: 'research_papers'")
    else:
        print("ℹ️  Collection 'research_papers' already exists — skipping")

    # ── Create payload indexes for fast filtering ─────────────────
    for collection in [COLLECTION_NAME, "research_papers"]:
        client.create_payload_index(
            collection_name=collection,
            field_name="domain",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        client.create_payload_index(
            collection_name=collection,
            field_name="year",
            field_schema=PayloadSchemaType.INTEGER,
        )
        client.create_payload_index(
            collection_name=collection,
            field_name="novelty_score",
            field_schema=PayloadSchemaType.FLOAT,
        )
        print(f"✅ Payload indexes created for '{collection}'")


def main():
    print(f"\n🔌 Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        info = client.get_collections()
        print(f"✅ Connected — {len(info.collections)} existing collections")
    except Exception as e:
        print(f"❌ Cannot connect to Qdrant: {e}")
        sys.exit(1)

    print("\n📦 Initializing collections...")
    init_collections(client)

    print("\n📊 Final state:")
    for col in client.get_collections().collections:
        info = client.get_collection(col.name)
        print(f"   • {col.name}: {info.vectors_count} vectors, dim={info.config.params.vectors.size}")

    print("\n✅ Qdrant init complete — ready for Phase 4 (document ingestion)\n")


if __name__ == "__main__":
    main()

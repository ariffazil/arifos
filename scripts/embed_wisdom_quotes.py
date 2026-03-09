#!/usr/bin/env python3
"""
Embed 99 Wisdom Quotes — arifOS Vector Memory
Unified embedding script for the 99-quote wisdom corpus.

Usage:
    python scripts/embed_wisdom_quotes.py
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "arifos_wisdom_quotes"
EMBEDDING_MODEL = "BAAI/bge-m3"
QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")
QUOTES_PATH = Path(__file__).parent.parent / "data" / "wisdom_quotes.json"


def main():
    print("=" * 60)
    print("ARIFOS 99 WISDOM QUOTES EMBEDDER")
    print("=" * 60)

    print("\n[1/5] Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    dim = model.get_sentence_embedding_dimension()
    print(f"      Model: {EMBEDDING_MODEL}")
    print(f"      Dimensions: {dim}")

    print("\n[2/5] Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL)

    try:
        client.get_collection(COLLECTION_NAME)
        print(f"      Collection '{COLLECTION_NAME}' exists - recreating...")
        client.delete_collection(COLLECTION_NAME)
    except UnexpectedResponse:
        print(f"      Creating collection '{COLLECTION_NAME}'...")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
    )

    print("\n[3/5] Loading 99 wisdom quotes...")
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    quotes = data["quotes"]
    print(f"      Loaded {len(quotes)} quotes")

    categories = {}
    for q in quotes:
        cat = q["category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"        - {cat}: {count}")

    print("\n[4/5] Generating embeddings...")
    embedding_texts = [
        f"Quote: {q['text']}\nAuthor: {q['author']}\nCategory: {q['category']}\nSource: {q['source']}\nHuman Cost: {q['human_cost']}"
        for q in quotes
    ]
    embeddings = model.encode(embedding_texts, normalize_embeddings=True, show_progress_bar=True)

    print("\n[5/5] Uploading to Qdrant...")
    points = []
    for i, (quote, embedding) in enumerate(zip(quotes, embeddings)):
        points.append(
            PointStruct(
                id=quote["id"],
                vector=embedding.tolist(),
                payload={
                    "id": quote["id"],
                    "category": quote["category"],
                    "author": quote["author"],
                    "text": quote["text"],
                    "source": quote["source"],
                    "human_cost": quote["human_cost"],
                    "embedding_model": EMBEDDING_MODEL,
                },
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"      Uploaded {len(points)} quotes")

    print("\n" + "=" * 60)
    print("EMBEDDING COMPLETE")
    print("=" * 60)
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Quotes:     {len(quotes)}")
    print(f"  Model:      {EMBEDDING_MODEL}")
    print()

    print("Test queries:")
    for query in ["I am suffering", "I need courage", "The paradox of life", "I feel broken"]:
        print(f"\n  '{query}'")
        query_embedding = model.encode(query, normalize_embeddings=True)
        results = client.search(COLLECTION_NAME, query_embedding.tolist(), limit=2)
        for r in results:
            print(f'    [{r.score:.3f}] {r.payload["author"]}: "{r.payload["text"][:50]}..."')


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate embeddings for wiki pages using multilingual MiniLM."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.venv-neo4j/lib/python*/site-packages"))
import numpy as np
from fastembed import TextEmbedding

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading embedding model (first time)...", file=sys.stderr)
        _model = TextEmbedding(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    return _model

def embed_text(text: str) -> list:
    """Generate embedding vector for a single text."""
    model = get_model()
    emb = list(model.embed([text[:8000]]))[0]
    return [float(v) for v in emb]

def embed_batch(texts: list) -> list:
    """Generate embeddings for a batch of texts."""
    model = get_model()
    texts = [t[:8000] for t in texts]
    return [[float(v) for v in emb] for emb in model.embed(texts)]

def cosine_similarity(a: list, b: list) -> float:
    """Cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

if __name__ == "__main__":
    # Quick test
    t1 = "PER 분석 방법 — 적정 PER 산정"
    t2 = "궤도 밸류에이션 — 적정 PER + PBR"
    e1 = embed_text(t1)
    e2 = embed_text(t2)
    print(f"Dim: {len(e1)}")
    print(f"Similarity: {cosine_similarity(e1, e2):.4f}")
    print("OK")

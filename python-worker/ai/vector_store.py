import faiss
import numpy as np

index = faiss.IndexFlatIP(512)

def add_vector(embedding: list) -> int:
    vector = np.array(embedding).astype("float32").reshape(1, 512)
    index.add(vector)
    return index.ntotal - 1

def search_vector(embedding: list, k: int = 5) -> list:
    vector = np.array(embedding).astype("float32").reshape(1, 512)
    scores, indices = index.search(vector, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "index": int(idx),
            "score": float(score)
        })
    return results
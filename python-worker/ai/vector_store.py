import faiss
import numpy as np

index = faiss.IndexFlatIP(512)
id_map = {}

def add_vector(embedding: list, identity_id: str) -> int:
    vector = np.array(embedding).astype("float32").reshape(1, 512)
    index.add(vector)
    faiss_id = index.ntotal - 1
    id_map[faiss_id] = identity_id
    return faiss_id

def search_vector(embedding: list, k: int = 5) -> list:
    vector = np.array(embedding).astype("float32").reshape(1, 512)
    scores, indices = index.search(vector, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "identity_id": id_map.get(int(idx)),
            "index": int(idx),
            "score": float(score)
        })
    return results
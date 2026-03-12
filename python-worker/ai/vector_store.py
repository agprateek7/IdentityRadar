import faiss
import numpy as np
import json
import os

INDEX_PATH = "faiss_index.bin"
ID_MAP_PATH = "faiss_id_map.json"

# On startup: load from disk if files exist, otherwise create fresh
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatIP(512)

if os.path.exists(ID_MAP_PATH):
    with open(ID_MAP_PATH, "r") as f:
        id_map = {int(k): v for k, v in json.load(f).items()}
else:
    id_map = {}

def _save():
    faiss.write_index(index, INDEX_PATH)
    with open(ID_MAP_PATH, "w") as f:
        json.dump(id_map, f)

def add_vector(embedding: list, identity_id: str) -> int:
    vector = np.array(embedding).astype("float32").reshape(1, 512)
    index.add(vector)
    faiss_id = index.ntotal - 1
    id_map[faiss_id] = identity_id
    _save()  # persist to disk so restarts don't reset the index
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
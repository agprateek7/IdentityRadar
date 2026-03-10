from fastapi import FastAPI
from pydantic import BaseModel
from ai.face_embedding import generate_embedding
from ai.vector_store import add_vector
from ai.vector_store import search_vector

app = FastAPI()

class EmbedRequest(BaseModel):
    identity_id: str
    image_url: str

class SearchRequest(BaseModel):
    image_url: str

@app.get('/health')
async def health():
    return {"status": 'ok'}

@app.post('/embed')
async def embed(req: EmbedRequest):
    vector = generate_embedding(req.image_url)
    faiss_id = add_vector(vector)
    return {"faiss_id": faiss_id}

@app.post('/search')
async def search(req: SearchRequest):
    vector = generate_embedding(req.image_url)
    results = search_vector(vector)
    return results
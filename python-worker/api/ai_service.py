from fastapi import FastAPI, HTTPException
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
    try:
        vector = generate_embedding(req.image_url)
        faiss_id = add_vector(vector, req.identity_id)
        return {"faiss_id": faiss_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/search')
async def search(req: SearchRequest):
    vector = generate_embedding(req.image_url)
    results = search_vector(vector)
    return results
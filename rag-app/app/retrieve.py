from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from .database import SessionLocal
from .models import Document

router = APIRouter()
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@router.get("/search/")
def search_documents(query: str, db: Session = Depends(get_db)):
    query_embedding = model.encode(query)

    documents = db.query(Document).all()
    results = []
    
    for doc in documents:
        doc_embedding = np.array(json.loads(doc.embedding))
        similarity = cosine_similarity(query_embedding, doc_embedding)
        results.append((doc, similarity))

    results.sort(key=lambda x: x[1], reverse=True)

    top_results = [{"id": doc.id, "name": doc.name, "content": doc.content} for doc, _ in results[:3]]
    return {"results": top_results}

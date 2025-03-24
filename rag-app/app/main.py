from fastapi import FastAPI
from .ingest import router as ingest_router
from .retrieve import router as retrieve_router
from .qa import router as qa_router

app = FastAPI()

app.include_router(ingest_router, prefix="/documents")
app.include_router(retrieve_router, prefix="/retrieve")
app.include_router(qa_router, prefix="/qa")

@app.get("/")
def read_root():
    return {"message": "RAG API is running!"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import openai
from .database import SessionLocal
from .retrieve import search_documents

router = APIRouter()
openai.api_key = "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" 

@router.get("/ask/")
def ask_question(query: str, db: Session = Depends(SessionLocal)):
    relevant_docs = search_documents(query, db)["results"]
    
    if not relevant_docs:
        return {"answer": "No relevant documents found."}

    context = "\n".join([doc["content"] for doc in relevant_docs])
    
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:"
    
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=100
    )

    return {"answer": response["choices"][0]["text"].strip()}

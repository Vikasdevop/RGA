from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import openai
from .database import SessionLocal
from .retrieve import search_documents

router = APIRouter()
# replace with your openai-api-key
openai.api_key = "your-openai-api-key" 

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

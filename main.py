"""
main.py
--------
FastAPI application exposing the AI Document Q&A Assistant as a REST API.

Endpoints:
    POST /upload  -> upload a PDF, it gets processed and added to the knowledge base
    POST /ask     -> ask a question, get an AI-generated answer grounded in your documents
    GET  /health  -> simple health check

Run with:
    uvicorn main:app --reload
"""

import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from document_processor import load_and_split_pdf
from rag_pipeline import build_or_update_vectorstore, answer_question

app = FastAPI(
    title="AI Document Q&A Assistant",
    description="RAG-based API that answers questions from uploaded PDF documents.",
    version="1.0.0",
)

DOCUMENTS_FOLDER = os.getenv("DOCUMENTS_FOLDER", "documents")
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Document Q&A Assistant is running"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, process it into chunks, and add it to the vector store."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported right now.")

    file_path = os.path.join(DOCUMENTS_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks = load_and_split_pdf(file_path)
        build_or_update_vectorstore(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

    return {
        "filename": file.filename,
        "chunks_added": len(chunks),
        "message": "Document processed and added to knowledge base successfully.",
    }


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer grounded in the uploaded documents."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = answer_question(request.question)
    return result

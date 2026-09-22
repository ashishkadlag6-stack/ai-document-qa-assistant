# AI Document Q&A Assistant (RAG + REST API)

An AI-powered assistant that answers natural-language questions from your own PDF
documents, using Retrieval-Augmented Generation (RAG). Built with FastAPI, FAISS,
HuggingFace embeddings, and the Groq LLM API.

## Why this project

This project was built to demonstrate core AI Engineering skills:
- **AI/LLM integration** — RAG pipeline using an LLM API (Groq)
- **REST API development** — FastAPI endpoints for upload and Q&A
- **Automation** — a folder watcher that auto-processes new documents
- **Data processing** — PDF parsing, text chunking, and embeddings

## Architecture

```
PDF Upload --> Text Extraction --> Chunking --> Embeddings --> FAISS Vector Store
                                                                      |
User Question -----------------------------------------------> Retrieve top-k chunks
                                                                      |
                                                              Groq LLM + context
                                                                      |
                                                                 Final Answer
```

## Setup

1. Clone this repo and move into it:
   ```bash
   git clone <your-repo-url>
   cd ai-doc-qa
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Get a **free** Groq API key from https://console.groq.com/keys and add it:
   ```bash
   cp .env.example .env
   # then edit .env and paste your GROQ_API_KEY
   ```

4. Run the API locally:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be live at `http://127.0.0.1:8000` — interactive docs at
   `http://127.0.0.1:8000/docs`

## Run with Docker Compose

Docker Compose runs the FastAPI backend and Streamlit frontend as separate services. The frontend talks to the backend using the Compose service name `backend`, while the browser uses the published ports.

1. Create the local environment file and add your Groq key:
   ```bash
   cp .env.example .env
   # edit .env and set GROQ_API_KEY
   ```

2. Build the images:
   ```bash
   docker compose build
   ```

3. Start both services:
   ```bash
   docker compose up
   ```

   Or run in the background:
   ```bash
   docker compose up -d
   ```

4. Open:
   - FastAPI docs: http://localhost:8000/docs
   - Streamlit frontend: http://localhost:8501

5. Check or stop the stack:
   ```bash
   docker compose ps
   docker compose logs backend
   docker compose logs frontend
   docker compose down
   ```

Uploaded PDFs and the FAISS index are bind-mounted from `documents/` and `vectorstore/`, so container restarts do not remove them.

5. (Optional) Run the automation watcher in a separate terminal:
   ```bash
   python watcher.py
   ```
   Now just drop a PDF into the `documents/` folder and it gets processed automatically.

## API Usage

**Upload a document:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@your_document.pdf"
```

**Ask a question:**
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

Response:
```json
{
  "answer": "This document discusses...",
  "sources": ["your_document.pdf"]
}
```

## Tech Stack

| Component        | Tool                                   |
|-------------------|-----------------------------------------|
| API Framework      | FastAPI                                |
| LLM                | Groq (llama-3.1-8b-instant, free tier) |
| Embeddings         | HuggingFace (all-MiniLM-L6-v2, local)  |
| Vector Store       | FAISS                                  |
| Document Parsing   | PyPDF                                  |
| Automation         | Watchdog (folder monitoring)           |

## Possible Extensions

- Add support for `.docx` and `.txt` files
- Add a simple frontend (Streamlit) for a chat-style UI
- Deploy to a free cloud tier (Render / Railway) to also demonstrate cloud exposure
- Add conversation memory for follow-up questions

# 🤖 AI Document Q&A Assistant

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://ashish-ai-document-55.streamlit.app) [![Backend](https://img.shields.io/badge/API-Render-46E3B7?logo=render&logoColor=white)](https://ashish-ai-document-qa-api.onrender.com) [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

An end-to-end **Retrieval-Augmented Generation (RAG)** application for asking natural-language questions over uploaded PDF documents.

The system combines **PDF processing, semantic chunking, local embeddings, FAISS vector search, Groq LLM inference, FastAPI, Streamlit, and Docker** into a practical AI engineering workflow.

## 🚀 Live Demo

| Component | URL |
|---|---|
| Streamlit Frontend | https://ashish-ai-document-55.streamlit.app |
| FastAPI Backend | https://ashish-ai-document-qa-api.onrender.com |
| Health Check | https://ashish-ai-document-qa-api.onrender.com/health |
| GitHub | https://github.com/ashishkadlag6-stack/ai-document-qa-assistant |

> The hosted application uses Streamlit for the interface and FastAPI for document processing and RAG inference.

## ✨ Key Features

- 📄 PDF upload and processing
- ✂️ Recursive chunking with overlap
- 🧠 Local Sentence Transformers embeddings
- 🔎 FAISS semantic similarity retrieval
- 🤖 Groq LLM answer generation
- 📚 **Page-level source citations**
- 🛡️ Context-grounded responses
- ⚡ FastAPI REST API
- 💬 Streamlit research interface
- 🐳 Docker and Docker Compose support
- 🔐 Environment-based secret management
- 👀 Watchdog document monitoring
- ☁️ Public frontend and backend deployment

## 🏗️ Architecture

```text
PDF Upload
    │
    ▼
PyPDFLoader
    │
    ▼
Text Chunking
    │
    ▼
Sentence Transformer Embeddings
    │
    ▼
FAISS Vector Store
    │
    │        User Question
    │              │
    │              ▼
    │        Query Embedding
    │              │
    └──────► Similarity Search
                   │
                   ▼
             Top-K Retrieval
                   │
                   ▼
           Retrieved Context
                   │
                   ▼
                Groq LLM
                   │
                   ▼
           Grounded Answer
                   │
                   ▼
        Answer + Source Pages
```

### Hosted architecture

```text
Streamlit Community Cloud
            │
            │ HTTP
            ▼
         Render
     FastAPI Backend
            │
     ┌──────┴──────┐
     ▼             ▼
 PDF/RAG       Groq LLM
 Processing    Generation
```

## 🧠 RAG Pipeline

### Document ingestion

1. Upload a PDF through the Streamlit UI.
2. Extract text and page metadata with `PyPDFLoader`.
3. Split content with `RecursiveCharacterTextSplitter`.
4. Generate local embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
5. Store embeddings and metadata in FAISS.

### Question answering

1. Accept a natural-language question.
2. Embed the query with the same embedding model.
3. Retrieve the most relevant chunks from FAISS.
4. Pass retrieved context to the Groq LLM.
5. Generate an answer grounded in the retrieved context.
6. Return source filename and page information.

The embedding model is **lazy-loaded** so the FastAPI process does not load the model during application startup.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| RAG | LangChain |
| LLM | Groq |
| Embeddings | Hugging Face Sentence Transformers |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| PDF Processing | PyPDF |
| Backend | FastAPI |
| Frontend | Streamlit |
| HTTP Client | Requests |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Monitoring | Watchdog |
| Version Control | Git / GitHub |
| Frontend Hosting | Streamlit Community Cloud |
| Backend Hosting | Render |

## 📁 Project Structure

```text
a i-document-qa-assistant/
│
├── backend/
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── styles.py
│   ├── ui_components.py
│   ├── requirements.txt
│   └── Dockerfile
├── documents/
│   └── .gitkeep
├── vectorstore/
│   └── .gitkeep
├── main.py
├── document_processor.py
├── rag_pipeline.py
├── watcher.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

## 🔌 REST API

### Health Check

```http
GET /health
```

### Upload PDF

```http
POST /upload
```

Multipart field: `file=<your_pdf>`

### Ask a Question

```http
POST /ask
```

Request:

```json
{
  "question": "What is Retrieval-Augmented Generation?"
}
```

Example response:

```json
{
  "answer": "Retrieval-Augmented Generation (RAG) ...",
  "sources": [
    "sample_ai_document.pdf — Page 1"
  ]
}
```

Interactive Swagger documentation is available locally at `http://127.0.0.1:8000/docs`.

## 📚 Source Citations

Retrieved source metadata is returned with page numbers:

```text
📚 Sources

• sample_ai_document.pdf — Page 1
```

This makes retrieved evidence easier to inspect and demonstrates page-aware RAG retrieval.

## 🧪 Example Queries

```text
What is Retrieval-Augmented Generation?
How does a RAG system work?
What are the benefits of using RAG?
What information does this document contain?
```

### Grounding test

Ask for information that is not present in the document:

```text
What is the population of India according to this document?
```

For the sample document, the application returns a response indicating that the requested information is unavailable instead of fabricating a document-based answer.

## 💻 Run Locally

### Clone

```bash
git clone https://github.com/ashishkadlag6-stack/ai-document-qa-assistant.git
cd ai-document-qa-assistant
```

### Create a virtual environment

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

```bash
cp .env.example .env
```

Add:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit `.env` or real API keys.

### Start FastAPI

```bash
uvicorn main:app --reload
```

### Start Streamlit

Open a second terminal:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Local URLs:

- Streamlit: http://localhost:8501
- FastAPI: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## 🐳 Docker Compose

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

Stop:

```bash
docker compose down
```

Local services:

- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000
- Swagger: http://localhost:8000/docs

## 🔐 Environment Variables

Local backend:

```env
GROQ_API_KEY=your_api_key_here
```

Hosted Streamlit frontend:

```text
API_BASE_URL=https://ashish-ai-document-qa-api.onrender.com
GROQ_API_KEY=your_api_key_here
```

Store production credentials in deployment secrets and keep them out of source control.

## 🎯 AI Engineering Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- LLM application development
- Semantic search
- Text chunking and preprocessing
- Vector embeddings
- FAISS similarity search
- Context grounding
- Source attribution and page citations
- REST API development
- Frontend/backend integration
- Docker containerization
- Secret management
- Cloud deployment
- CPU-based model serving

## 🔍 Engineering Design Decisions

### RAG instead of fine-tuning
RAG retrieves relevant information from an external knowledge base before generation, so changing documents does not require retraining the language model.

### Local embeddings
A local Sentence Transformers model avoids a separate embedding API and demonstrates the embedding pipeline directly.

### FAISS
FAISS provides a lightweight local vector index suitable for this application.

### FastAPI + Streamlit
FastAPI separates the AI pipeline from the interface, while Streamlit provides a lightweight Python-based UI.

### Docker
Docker packages application dependencies into reproducible containers and simplifies local deployment.

## 📈 Current Scope

The current implementation focuses on **PDF question answering with FAISS retrieval, Groq generation, and page-level source citations**.

## 🔮 Future Improvements

- Multi-document management
- Document deletion and re-indexing
- Metadata filtering
- Hybrid keyword + vector retrieval
- Retrieval reranking
- Conversation memory
- RAG evaluation datasets and metrics
- Authentication and user management
- Persistent managed vector storage
- Rate limiting and observability
- CI/CD automation

## 👨‍💻 Author

**Ashish Kadlag**  
Data Science & AI Engineering

- GitHub: https://github.com/ashishkadlag6-stack
- LinkedIn: https://www.linkedin.com/in/ashish-kadlag-5bba382b5/

## ⭐ Project Objective

Build and demonstrate an end-to-end AI application connecting:

**document processing → embeddings → vector retrieval → LLM generation → REST API → web UI → containerized deployment**

This project is intended as a practical portfolio project for **AI Engineering, Generative AI, and applied Machine Learning roles**.

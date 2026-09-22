# 🤖 AI Document Q&A Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask natural-language questions based on their content.

The system combines **document processing, semantic search, vector embeddings, FAISS, Groq LLMs, FastAPI, Streamlit, and Docker** to provide grounded answers from uploaded documents.

---

## 🚀 Features

* 📄 Upload and process PDF documents
* ✂️ Intelligent document chunking
* 🧠 Local sentence-transformer embeddings
* 🔎 Semantic similarity search using FAISS
* 🤖 Groq LLM-powered answer generation
* 📚 Source-aware responses
* 🛡️ Reduces hallucination by answering from retrieved document context
* ⚡ FastAPI REST API
* 💬 Streamlit chat interface
* 👀 Automatic document processing with folder monitoring
* 🐳 Docker and Docker Compose support
* 🔐 Environment-based API key configuration

---

## 🏗️ Architecture

```text
                  ┌─────────────────────┐
                  │     PDF Document    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   PDF Text Extract  │
                  │       (PyPDF)       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Text Chunking     │
                  │ Recursive Splitter  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Embeddings       │
                  │ SentenceTransformers│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   FAISS Vector DB   │
                  └──────────┬──────────┘
                             │
                  User Question
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Semantic Retrieval  │
                  │    Top-K Chunks     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Groq LLM        │
                  │ Context + Question  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Grounded Answer    │
                  │   + Source Info     │
                  └─────────────────────┘
```

---

## 🧠 How RAG Works

The application follows a Retrieval-Augmented Generation pipeline:

1. User uploads a PDF.
2. Text is extracted from the document.
3. Large text is divided into smaller chunks.
4. Each chunk is converted into a vector embedding.
5. Embeddings are stored in a FAISS vector index.
6. User submits a question.
7. The system converts the question into an embedding.
8. FAISS retrieves the most relevant document chunks.
9. Retrieved context is passed to the Groq LLM.
10. The LLM generates an answer based on the retrieved context.
11. Relevant source information is returned with the answer.

This approach helps the application answer questions using the uploaded document rather than relying only on the LLM's general knowledge.

---

## 🛠️ Tech Stack

| Category             | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python                         |
| LLM                  | Groq                           |
| RAG                  | Retrieval-Augmented Generation |
| Embeddings           | Sentence Transformers          |
| Vector Database      | FAISS                          |
| PDF Processing       | PyPDF                          |
| Backend API          | FastAPI                        |
| Frontend             | Streamlit                      |
| Containerization     | Docker                         |
| Orchestration        | Docker Compose                 |
| Automation           | Watchdog                       |
| Version Control      | Git & GitHub                   |

---

## 📁 Project Structure

```text
ai-document-qa-assistant/
│
├── backend/
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── styles.py
│   ├── ui_components.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── documents/
│   └── .gitkeep
│
├── vectorstore/
│   └── .gitkeep
│
├── document_processor.py
├── rag_pipeline.py
├── watcher.py
├── main.py
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

---

## ⚙️ API Endpoints

### Health Check

```http
GET /health
```

### Upload Document

```http
POST /upload
```

Multipart form field:

```text
file=<your_pdf>
```

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "question": "What is this document about?"
}
```

Example response:

```json
{
  "answer": "This document discusses...",
  "sources": [
    "sample.pdf"
  ]
}
```

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ashishkadlag6-stack/ai-document-qa-assistant.git
cd ai-document-qa-assistant
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:

```text
GROQ_API_KEY=your_api_key_here
```

Never commit the `.env` file to GitHub.

### 5. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🐳 Run with Docker

Make sure Docker Desktop is running.

### Build containers

```bash
docker compose build
```

### Start application

```bash
docker compose up -d
```

### Check containers

```bash
docker compose ps
```

### Application URLs

Frontend:

```text
http://localhost:8501
```

FastAPI:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Stop application

```bash
docker compose down
```

---

## 🔐 Environment Variables

Create `.env` from `.env.example`.

```text
GROQ_API_KEY=your_api_key_here
```

The actual `.env` file is intentionally excluded from Git using `.gitignore`.

---

## 🧪 Example Workflow

```text
Upload PDF
    ↓
Document Processing
    ↓
Text Chunking
    ↓
Generate Embeddings
    ↓
Store in FAISS
    ↓
Ask Question
    ↓
Retrieve Relevant Chunks
    ↓
Send Context to Groq LLM
    ↓
Generate Grounded Answer
    ↓
Display Answer + Sources
```

---

## 🎯 AI Engineering Concepts Demonstrated

This project demonstrates practical AI Engineering concepts including:

* Retrieval-Augmented Generation (RAG)
* Large Language Model integration
* Prompt-based context grounding
* Semantic search
* Vector embeddings
* Vector similarity search
* Document ingestion pipelines
* REST API development
* AI application architecture
* Docker containerization
* Frontend/backend integration
* Environment and secret management
* Automated document processing

---

## 🔮 Future Improvements

* Support for DOCX and TXT documents
* Conversation memory
* Multi-document collections
* Metadata filtering
* Improved retrieval strategies
* Reranking retrieved documents
* Authentication and user management
* Cloud deployment
* CI/CD pipeline
* Evaluation metrics for RAG quality

---

## 👨‍💻 Author

**Ashish Kadlag**

Data Science / AI Engineering Enthusiast

GitHub:
https://github.com/ashishkadlag6-stack

LinkedIn:
https://www.linkedin.com/in/ashish-kadlag-5bba382b5/

---

## ⭐ Project Goal

The goal of this project is to demonstrate how modern AI applications can combine **LLMs, RAG, vector search, APIs, data processing, and containerization** into a practical end-to-end system.


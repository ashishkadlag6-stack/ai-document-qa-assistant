# AI Document Q&A Assistant Frontend

This is a separate Streamlit client for the existing FastAPI backend. It does not read or modify the backend's documents or FAISS vectorstore directly.

## Run locally on macOS

Start the backend from the repository root in Terminal 1:

```bash
cd ai-doc-qa
source .venv/bin/activate
uvicorn main:app --reload
```

Install and start the frontend in Terminal 2:

```bash
cd ai-doc-qa/frontend
python -m venv .venv  # only needed once
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The frontend uses `http://127.0.0.1:8000` by default. To point it elsewhere, set `API_BASE_URL` in an environment file or shell before starting Streamlit.

The frontend session tracks only documents uploaded through the current browser session; it does not represent permanent database storage.
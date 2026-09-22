"""
rag_pipeline.py
----------------
The core AI logic:
- Converts text chunks into embeddings and stores them in a FAISS vector store
- Given a question, retrieves the most relevant chunks
- Sends those chunks + the question to the Groq LLM to generate a grounded answer
"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()

VECTORSTORE_FOLDER = os.getenv("VECTORSTORE_FOLDER", "vectorstore")

# Free, local embedding model (no API cost, runs on CPU)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

_vectorstore = None  # cached in memory once loaded


def build_or_update_vectorstore(chunks):
    """
    Adds new document chunks to the FAISS vector store.
    Creates a new store if one doesn't exist yet, otherwise merges into the existing one.
    """
    global _vectorstore

    if os.path.exists(os.path.join(VECTORSTORE_FOLDER, "index.faiss")):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_FOLDER, embedding_model, allow_dangerous_deserialization=True
        )
        new_store = FAISS.from_documents(chunks, embedding_model)
        _vectorstore.merge_from(new_store)
    else:
        _vectorstore = FAISS.from_documents(chunks, embedding_model)

    _vectorstore.save_local(VECTORSTORE_FOLDER)
    print(f"[rag_pipeline] Vector store updated and saved to '{VECTORSTORE_FOLDER}'")
    return _vectorstore


def load_vectorstore():
    """Loads the FAISS vector store from disk into memory (used at API startup)."""
    global _vectorstore
    if _vectorstore is None and os.path.exists(os.path.join(VECTORSTORE_FOLDER, "index.faiss")):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_FOLDER, embedding_model, allow_dangerous_deserialization=True
        )
    return _vectorstore


def answer_question(question: str, top_k: int = 3):
    """
    Runs the full RAG flow: retrieve relevant chunks -> ask the LLM -> return answer + sources.
    """
    vectorstore = load_vectorstore()
    if vectorstore is None:
        return {"answer": "No documents have been uploaded yet. Please upload a PDF first.", "sources": []}

    llm = ChatGroq(
        model="openai/gpt-oss-20b",  # available chat model on the configured Groq account
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": top_k}),
        return_source_documents=True,
    )

    result = qa_chain.invoke({"query": question})

    sources = list({doc.metadata.get("source_file", "unknown") for doc in result["source_documents"]})

    return {"answer": result["result"], "sources": sources}

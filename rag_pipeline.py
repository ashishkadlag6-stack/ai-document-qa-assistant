"""
rag_pipeline.py
----------------
Core RAG logic:
- Converts document chunks into embeddings
- Stores embeddings in FAISS
- Retrieves relevant chunks
- Uses Groq LLM to generate grounded answers
"""

import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

load_dotenv()

VECTORSTORE_FOLDER = os.getenv("VECTORSTORE_FOLDER", "vectorstore")

# Lazy-loaded embedding model.
# This prevents the model from loading during FastAPI startup.
_embedding_model = None

_vectorstore = None


def get_embedding_model():
    """
    Loads the embedding model only when it is actually needed.
    Keeps the model cached after the first load.
    """
    global _embedding_model

    if _embedding_model is None:
        print("[rag_pipeline] Loading embedding model...")

        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        print("[rag_pipeline] Embedding model loaded.")

    return _embedding_model


def build_or_update_vectorstore(chunks):
    """
    Adds new document chunks to the FAISS vector store.
    Creates a new store if one doesn't exist.
    """
    global _vectorstore

    embedding_model = get_embedding_model()

    if os.path.exists(os.path.join(VECTORSTORE_FOLDER, "index.faiss")):
        _vectorstore = FAISS.load_local(
            VECTORSTORE_FOLDER,
            embedding_model,
            allow_dangerous_deserialization=True,
        )

        new_store = FAISS.from_documents(
            chunks,
            embedding_model,
        )

        _vectorstore.merge_from(new_store)

    else:
        _vectorstore = FAISS.from_documents(
            chunks,
            embedding_model,
        )

    _vectorstore.save_local(VECTORSTORE_FOLDER)

    print(
        f"[rag_pipeline] Vector store updated and saved to "
        f"'{VECTORSTORE_FOLDER}'"
    )

    return _vectorstore


def load_vectorstore():
    """
    Loads the FAISS vector store only when needed.
    """
    global _vectorstore

    if _vectorstore is None and os.path.exists(
        os.path.join(VECTORSTORE_FOLDER, "index.faiss")
    ):
        embedding_model = get_embedding_model()

        _vectorstore = FAISS.load_local(
            VECTORSTORE_FOLDER,
            embedding_model,
            allow_dangerous_deserialization=True,
        )

    return _vectorstore


def answer_question(question: str, top_k: int = 3):
    """
    Runs the complete RAG flow:
    retrieve relevant chunks -> send to Groq -> return answer + sources.
    """

    vectorstore = load_vectorstore()

    if vectorstore is None:
        return {
            "answer": "No documents have been uploaded yet. Please upload a PDF first.",
            "sources": [],
        }

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        ),
        return_source_documents=True,
    )

    result = qa_chain.invoke(
        {"query": question}
    )

    # Build unique source citations with page numbers.
    sources = []
    seen_sources = set()

    for doc in result["source_documents"]:
        source_file = doc.metadata.get("source_file", "unknown")
        page_number = doc.metadata.get("page_number")

        if page_number is not None:
            source = f"{source_file} — Page {page_number}"
        else:
            source = source_file

        if source not in seen_sources:
            seen_sources.add(source)
            sources.append(source)

    return {
        "answer": result["result"],
        "sources": sources,
    }
"""Streamlit frontend for the AI Document Q&A Assistant."""

from typing import Any

import streamlit as st

from api_client import APIClientError, ask_question, check_health, upload_document
from styles import load_css
from ui_components import render_api_status, render_brand, render_chat_message, render_metric


st.set_page_config(
    page_title="AI Document Q&A Assistant | Ashish Kadlag",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()


def initialize_state() -> None:
    defaults: dict[str, Any] = {
        "chat_history": [],
        "uploaded_documents": [],
        "upload_results": [],
        "selected_question": "",
        "api_online": False,
        "total_chunks": 0,
        "uploader_reset": 0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def refresh_health() -> None:
    try:
        check_health()
        st.session_state.api_online = True
    except APIClientError:
        st.session_state.api_online = False


def clear_chat() -> None:
    st.session_state.chat_history = []


def render_sidebar() -> None:
    with st.sidebar:
        render_brand()
        if st.button("＋  New chat", use_container_width=True, type="primary"):
            clear_chat()
            st.rerun()

        st.markdown('<div class="section-label">Add a document</div>', unsafe_allow_html=True)
        uploader_key = f"pdf_uploader_{st.session_state.uploader_reset}"
        uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"], key=uploader_key, label_visibility="collapsed")
        if uploaded_file:
            st.caption(f"{uploaded_file.name} · {uploaded_file.size / 1024:.1f} KB")
            upload_column, clear_column = st.columns([3, 2])
            with upload_column:
                upload_clicked = st.button("Upload to knowledge base", use_container_width=True)
            with clear_column:
                clear_file_clicked = st.button("Clear file", use_container_width=True)
            if clear_file_clicked:
                st.session_state.uploader_reset += 1
                st.rerun()
            if upload_clicked:
                with st.spinner("Processing PDF and building embeddings..."):
                    try:
                        result = upload_document(uploaded_file)
                    except APIClientError as error:
                        st.error(str(error))
                    else:
                        filename = str(result.get("filename") or uploaded_file.name)
                        chunks = result.get("chunks_added")
                        if filename not in st.session_state.uploaded_documents:
                            st.session_state.uploaded_documents.append(filename)
                        if isinstance(chunks, int):
                            st.session_state.total_chunks += chunks
                        st.session_state.upload_results.append(result)
                        st.success(result.get("message", "Document uploaded successfully."))
                        st.caption(f"Filename: {filename} · Chunks added: {chunks if chunks is not None else 'Not provided'}")

        st.markdown('<div class="section-label">Connection</div>', unsafe_allow_html=True)
        render_api_status(st.session_state.api_online)

        st.markdown('<div class="section-label">Session documents</div>', unsafe_allow_html=True)
        if st.session_state.uploaded_documents:
            for filename in st.session_state.uploaded_documents:
                st.markdown(f'<div class="file-row">📄 {filename}</div>', unsafe_allow_html=True)
        else:
            st.caption("No PDFs uploaded in this session.")

        st.markdown('<div class="section-label">Workspace</div>', unsafe_allow_html=True)
        if st.button("Clear chat", use_container_width=True):
            clear_chat()
            st.rerun()

        with st.expander("About this project"):
            st.caption("A Streamlit research workspace for asking grounded questions over your PDF knowledge base.")
            st.caption("Frontend: Python · Streamlit · Requests")


def render_dashboard() -> None:
    st.markdown('<div class="eyebrow">AI research workspace</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">AI Document Q&amp;A Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-copy">Your intelligent document research assistant powered by retrieval-augmented generation.</p>', unsafe_allow_html=True)

    first_column, second_column, third_column = st.columns(3)
    with first_column:
        document_label = "No document" if not st.session_state.uploaded_documents else "Ready to query"
        render_metric("Current document status", document_label)
    with second_column:
        render_metric("Uploaded this session", str(len(st.session_state.uploaded_documents)))
    with third_column:
        chunks = str(st.session_state.total_chunks) if st.session_state.total_chunks else "Not available"
        render_metric("Chunks added", chunks)

    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            render_chat_message(message["role"], message["content"], message.get("sources"))
    else:
        st.markdown(
            '<div class="empty-state"><div class="empty-icon">⌁</div><div class="empty-title">Ask questions about your documents</div><div class="empty-copy">Upload a PDF and ask questions using retrieval-augmented generation.</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-label">Suggested questions</div>', unsafe_allow_html=True)
        suggestions = [
            "What is this document about?",
            "What are the key points?",
            "What is Retrieval-Augmented Generation?",
            "What are the benefits of RAG?",
            "Explain the main concepts in this document.",
        ]
        suggestion_columns = st.columns(2)
        for index, suggestion in enumerate(suggestions):
            with suggestion_columns[index % 2]:
                if st.button(suggestion, key=f"suggestion_{index}", use_container_width=True):
                    st.session_state.selected_question = suggestion
                    st.rerun()

    if st.session_state.selected_question:
        st.info(f"Selected question: {st.session_state.selected_question}")
        if st.button("Ask selected question", type="primary"):
            submit_question(st.session_state.selected_question)
            st.session_state.selected_question = ""
            st.rerun()

    question = st.chat_input("Ask a question about your uploaded PDFs...")
    if question:
        submit_question(question.strip())
        st.rerun()

    st.markdown('<div class="footer">Python · FastAPI · RAG · FAISS · HuggingFace Embeddings · Groq</div>', unsafe_allow_html=True)


def submit_question(question: str) -> None:
    if not question:
        return
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("Searching your documents..."):
        try:
            result = ask_question(question)
            answer = result.get("answer")
            if not isinstance(answer, str) or not answer.strip():
                raise APIClientError("The API returned no answer for this question.")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer, "sources": result.get("sources")}
            )
        except APIClientError as error:
            st.session_state.chat_history.append({"role": "assistant", "content": f"I couldn't complete that request: {error}"})


initialize_state()
refresh_health()
render_sidebar()
render_dashboard()
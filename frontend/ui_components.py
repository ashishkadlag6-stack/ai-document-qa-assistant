"""Reusable presentation helpers for the Streamlit app."""

from typing import Any

import streamlit as st


def render_brand() -> None:
    st.markdown(
        '<div class="brand"><div class="brand-mark">✦</div><div><div class="brand-name">AI Document Q&amp;A</div><div class="brand-caption">Research workspace</div></div></div>',
        unsafe_allow_html=True,
    )


def render_api_status(is_online: bool) -> None:
    label = "API Online" if is_online else "API Offline"
    class_name = "status-dot online" if is_online else "status-dot"
    st.markdown(f'<div class="status-pill"><span class="{class_name}"></span>{label}</div>', unsafe_allow_html=True)


def render_metric(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def render_sources(sources: Any) -> None:
    if not sources:
        return
    with st.expander("📚 Sources"):
        if isinstance(sources, list):
            for source in sources:
                if isinstance(source, dict):
                    name = source.get("filename") or source.get("source") or source.get("name") or "Source"
                    metadata = {key: value for key, value in source.items() if key not in {"filename", "source", "name"}}
                    st.markdown(f"**{name}**")
                    if metadata:
                        st.caption(" · ".join(f"{key}: {value}" for key, value in metadata.items()))
                else:
                    st.markdown(f"- {source}")
        else:
            st.write(sources)


def render_chat_message(role: str, content: str, sources: Any = None) -> None:
    with st.chat_message(role):
        st.markdown(content)
        if role == "assistant":
            render_sources(sources)
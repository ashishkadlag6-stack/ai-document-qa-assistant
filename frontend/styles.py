"""Visual system for the Streamlit frontend."""

import streamlit as st


def load_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --accent: #2f6fed;
            --accent-soft: rgba(47, 111, 237, 0.12);
            --border: rgba(127, 139, 164, 0.24);
            --muted: #7c879c;
        }
        .stApp { background: radial-gradient(circle at 85% 0%, rgba(47,111,237,.08), transparent 30%), var(--background-color); }
        [data-testid="stSidebar"] { border-right: 1px solid var(--border); }
        [data-testid="stSidebarContent"] { padding: 1.35rem 1.15rem; }
        .brand { display: flex; gap: .7rem; align-items: center; margin-bottom: 1.7rem; }
        .brand-mark { display: grid; place-items: center; width: 2.25rem; height: 2.25rem; border-radius: .7rem; background: var(--accent); color: white; font-weight: 800; box-shadow: 0 8px 24px rgba(47,111,237,.24); }
        .brand-name { font-weight: 700; line-height: 1.1; }
        .brand-caption, .muted { color: var(--muted); font-size: .8rem; }
        .eyebrow { color: var(--accent); font-size: .74rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin-bottom: .5rem; }
        .hero-title { font-size: clamp(2rem, 4vw, 3.3rem); line-height: 1.05; letter-spacing: -.03em; margin: 0; font-weight: 800; }
        .hero-copy { max-width: 650px; color: var(--muted); font-size: 1.02rem; margin-top: .85rem; }
        .section-label { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 1.6rem 0 .7rem; }
        .metric-card, .empty-state, .info-panel { border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.1rem; background: rgba(127,139,164,.045); }
        .metric-label { color: var(--muted); font-size: .78rem; }
        .metric-value { font-size: 1.5rem; font-weight: 750; margin-top: .25rem; }
        .empty-state { text-align: center; padding: 3rem 1.2rem; margin: 1.4rem 0; }
        .empty-icon { font-size: 2rem; margin-bottom: .7rem; }
        .empty-title { font-size: 1.15rem; font-weight: 700; }
        .empty-copy { color: var(--muted); margin: .35rem auto 0; max-width: 520px; }
        .status-pill { display: inline-flex; align-items: center; gap: .4rem; border: 1px solid var(--border); border-radius: 999px; padding: .3rem .65rem; font-size: .78rem; }
        .status-dot { width: .48rem; height: .48rem; border-radius: 50%; background: #e05454; }
        .status-dot.online { background: #25a269; box-shadow: 0 0 0 3px rgba(37,162,105,.13); }
        .file-row { border: 1px solid var(--border); border-radius: 10px; padding: .7rem .8rem; margin: .45rem 0; }
        .footer { border-top: 1px solid var(--border); margin-top: 3rem; padding: 1.2rem 0 2rem; color: var(--muted); font-size: .78rem; text-align: center; }
        div[data-testid="stChatMessage"] { border: 1px solid var(--border); border-radius: 12px; padding: .8rem 1rem; }
        .stButton > button { border-radius: 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
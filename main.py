#-----------------------3rd One with UI Changes One----------------------------

from typing import Any, Dict, List
import streamlit as st
from backend.core import run_llm


def _format_sources(context_docs: List[Any]) -> List[str]:
    return [
        str((meta.get("source") or "Unknown"))
        for doc in (context_docs or [])
        if (meta := (getattr(doc, "metadata", None) or {})) is not None
    ]


st.set_page_config(
    page_title="DocuMind — AI Documentation Assistant",
    page_icon="🧠",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F8F9FC; }

    /* Title styling */
    h1 { color: #1A1A2E !important; font-weight: 800 !important; }

    /* Chat input */
    .stChatInput input {
        border-radius: 12px !important;
        border: 2px solid #4F8EF7 !important;
        background: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #4F8EF7 !important;
        opacity: 0.3;
    }

    /* Buttons in sidebar */
    section[data-testid="stSidebar"] .stButton button {
        background: #4F8EF7 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stDownloadButton button {
        background: #2ECC71 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        border: 1px solid #E8EFFE !important;
        background: #FFFFFF !important;
    }

    /* Success / warning / error badges */
    .stSuccess {
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    .stWarning {
        border-radius: 8px !important;
        font-size: 13px !important;
    }
    .stAlert {
        border-radius: 8px !important;
        font-size: 13px !important;
    }

    /* Caption text */
    .stCaptionContainer {
        color: #7F8C8D !important;
        font-size: 12px !important;
    }

    /* Spinner */
    .stSpinner { color: #4F8EF7 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 DocuMind")
    st.markdown("**Huzaifa Amir**")
    st.markdown("*A RAG-powered AI assistant for LangChain documentation*")
    st.markdown("---")
    st.markdown("### 🛠 Powered By")
    st.markdown("🔗 Python · LangChain · RAG · 📌 Pinecone · Streamlit · 🤖 LLM - Gemini · 🌐 Tavily")
    st.markdown("---")
    st.markdown("### ⚙️ Session")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

    st.markdown("---")

    if st.button("📥 Export Chat History", use_container_width=True):
        history_text = ""
        for msg in st.session_state.get("messages", []):
            role = msg["role"].upper()
            history_text += f"[{role}]\n{msg['content']}\n\n"
        st.download_button(
            label="⬇️ Download .txt",
            data=history_text,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ── Header ────────────────────────────────────────────────────────────
st.markdown("# 🧠 DocuMind ")
st.markdown("#### AI Documentation Assistant for LangChain")
st.caption("Ask any question → DocuMind retrieves real docs → Gemini generates a precise answer")
st.markdown("---")

# ── Message History ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I'm DocuMind. Ask me anything about LangChain and I'll find the answer from the official documentation.",
            "sources": [],
            "num_sources": 0,
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and msg.get("num_sources", 0) > 0:
            num_sources = msg.get("num_sources", 0)
            st.caption(f"🔍 {num_sources} source document(s) retrieved")
            if num_sources >= 3:
                st.success("✅ Relevance: HIGH — Multiple sources found")
            elif num_sources == 2:
                st.warning("⚠️ Relevance: MEDIUM — Limited sources found")
            else:
                st.error("❌ Relevance: LOW — Answer may be incomplete")

        if msg.get("sources"):
            with st.expander("📄 View Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- [{s}]({s})")

# ── Chat Input ────────────────────────────────────────────────────────
prompt = st.chat_input("Ask a question about LangChain…")
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "sources": [],
        "num_sources": 0,
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🔍 Searching docs and generating answer…"):
                result: Dict[str, Any] = run_llm(prompt)
                answer = str(result.get("answer", "")).strip() or "(No answer returned.)"
                sources = _format_sources(result.get("context", []))
                num_sources = len(sources)

            st.markdown(answer)
            st.caption(f"🔍 {num_sources} source document(s) retrieved")

            if num_sources >= 3:
                st.success("✅ Relevance: HIGH — Multiple sources found")
            elif num_sources == 2:
                st.warning("⚠️ Relevance: MEDIUM — Limited sources found")
            else:
                st.error("❌ Relevance: LOW — Answer may be incomplete")

            if sources:
                with st.expander("📄 View Sources"):
                    for s in sources:
                        st.markdown(f"- [{s}]({s})")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "num_sources": num_sources,
            })

        except Exception as e:
            st.error("❌ Failed to generate a response.")
            st.exception(e)



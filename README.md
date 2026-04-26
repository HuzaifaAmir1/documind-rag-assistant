# 🧠 DocuMind — AI Documentation Assistant

<div align="center">

**A RAG-powered AI assistant that answers questions about LangChain documentation**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-green.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Pinecone](https://img.shields.io/badge/Pinecone-🌲-orange.svg)](https://pinecone.io/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-blue.svg)](https://ai.google.dev/)
[![Tavily](https://img.shields.io/badge/Tavily-🔍-purple.svg)](https://tavily.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 What is DocuMind?

DocuMind is an intelligent documentation chatbot built on a **RAG (Retrieval-Augmented Generation)** pipeline. Instead of relying on an LLM's general training data, DocuMind crawls real LangChain documentation, stores it in a vector database, and retrieves the most relevant chunks before generating an answer.

This means answers are grounded in actual documentation — not hallucinated.

---

## ✨ Features

- 🌐 **Web Crawling** — Crawls LangChain docs automatically using Tavily
- 📚 **Smart Chunking** — Splits documents into optimised chunks for better retrieval
- 🔍 **Vector Search** — Stores and retrieves embeddings using Pinecone
- 🤖 **Gemini-Powered** — Uses Google Gemini for answer generation
- 📊 **Confidence Scoring** — Shows High / Medium / Low relevance for every answer
- 🔗 **Source Citations** — Every answer links back to the exact documentation page
- 📥 **Chat Export** — Download your full conversation as a .txt file
- 🎨 **Clean UI** — Light-themed Streamlit interface with dark sidebar

---

## 🏗️ Architecture

User Question
│
▼
┌─────────────────┐
│  Streamlit UI   │  ← main.py
└────────┬────────┘
│
▼
┌─────────────────┐
│  RAG Agent      │  ← backend/core.py
│  (LangGraph)    │
└────────┬────────┘
│
┌────┴────┐
▼         ▼
┌────────┐ ┌──────────────┐
│Pinecone│ │ Gemini LLM   │
│Vectors │ │ (Generator)  │
└────────┘ └──────────────┘

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| 🖥️ Frontend | Streamlit |
| 🧠 AI Framework | LangChain + LangGraph |
| 🔍 Vector Database | Pinecone |
| 🌐 Web Crawling | Tavily |
| 🤖 LLM | Google Gemini 2.0 Flash |
| 📐 Embeddings | Gemini Embedding 001 |
| 🐍 Backend | Python 3.11 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API key (free at aistudio.google.com)
- Pinecone API key (free at pinecone.io)
- Tavily API key (free at tavily.com)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/HuzaifaAmir1/documind-rag-assistant.git
cd documind-rag-assistant
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
```

**3. Install dependencies**
```bash
pip install langchain langchain-openai langchain-pinecone langchain-community streamlit pinecone openai tavily-python python-dotenv tiktoken langgraph langchain-google-genai langchain-tavily langchain-text-splitters
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_gemini_api_key_here
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
TAVILY_API_KEY=your_tavily_api_key_here
```

**5. Run the ingestion pipeline**
```bash
python ingestion.py
```

**6. Launch the app**
```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

documind-rag-assistant/
├── backend/
│   ├── init.py
│   └── core.py              # RAG agent — retrieval + generation logic
├── .streamlit/
│   └── config.toml          # Light theme configuration
├── static/                  # App assets
├── main.py                  # Streamlit UI
├── ingestion.py             # Doc crawling + Pinecone indexing pipeline
├── consts.py                # Configuration constants
├── logger.py                # Logging utilities
└── .env                     # API keys (never committed)

---

## 💡 What I Learned Building This

- How RAG pipelines work end-to-end — from crawling to vector storage to generation
- Why chunking strategy matters — too large = poor retrieval, too small = lost context
- How to use LangGraph's `create_react_agent` to build tool-calling AI agents
- How to swap LLM providers (OpenAI → Gemini) using the OpenAI-compatible API format
- How vector similarity search works in Pinecone and why cosine similarity is used
- How prompt engineering directly affects answer quality and hallucination rates

---

## 🔮 Future Improvements

- [ ] Add support for multiple documentation sources (LangGraph, LangSmith)
- [ ] Implement conversation memory for multi-turn context
- [ ] Add a re-ranking step to improve retrieval precision
- [ ] Deploy to Streamlit Cloud for public access
- [ ] Add user feedback buttons (thumbs up/down) to track answer quality

---

## ⚙️ Environment Variables

| Variable | Description |
|----------|-------------|
| `PINECONE_API_KEY` | Pinecone vector database API key |
| `OPENAI_API_KEY` | Gemini API key (used via OpenAI-compatible endpoint) |
| `OPENAI_BASE_URL` | Gemini API base URL |
| `TAVILY_API_KEY` | Tavily web crawling API key |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built by <a href="https://github.com/HuzaifaAmir1">Huzaifa Amir</a>
</div>
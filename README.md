# Spool – YouTube Video Summarizer

> **Note:** This is a personal project and not a production app.

Spool turns the typical YouTube viewing experience into an interactive chat. Instead of manually scrubbing through long videos, it uses LangChain to orchestrate a smart retrieval workflow—combining transcripts, hybrid search, and LLM reasoning—to give you a chatbot that actually researches and answers your questions based on the video content.

## What makes it interesting
Under the hood it's a proper LangChain pipeline, so it does a bit more than a plain prompt-reply loop:
1. **Hybrid Retrieval**: Combines semantic search (Chroma) with keyword search (BM25) via an Ensemble Retriever for highly accurate context retrieval.
2. **Dynamic Ingestion**: Fetches transcripts directly using the unofficial YouTube Transcript API, splits them, and embeds them on the fly.
3. **Conversational Memory**: Maintains chat history across your session so follow-up questions feel natural.

## Features
- **Video Chat**: Ask questions and get answers directly from the video's transcript.
- **Hybrid Retrieval**: Uses Chroma + Google Generative AI Embeddings along with BM25 for robust context fetching.
- **Memory**: Remembers conversation history to maintain context during the chat.
- **Clean UI**: A clean, reactive Streamlit interface that embeds the video right alongside your chat.

## Tech Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | Python 3.11+, LangChain | Orchestration and pipeline engine |
| **LLM** | Google Gemini (`langchain-google-genai`) | Reasoning, generation |
| **Vector Store** | Chroma (`langchain-chroma`) | Semantic document retrieval |
| **Keyword Search** | BM25 (`rank-bm25`) | Exact keyword matching |
| **Embeddings** | Google Generative AI Embeddings | Turning text into meaning |
| **Document Loaders** | YouTube Transcript API | Ingesting video transcripts |
| **UI** | Streamlit | A clean, reactive chat interface |
| **Ops** | Ruff, MyPy, pytest | Fast linting, type safety, testing |

## How It Works
Imagine you type: *"What are the main points discussed in the video?"*
1. **Chat Node**: Gemini reads your message and the conversational history.
2. **Retrieval**: Spool's Ensemble Retriever fetches the most relevant transcript chunks using both Chroma (semantic) and BM25 (keyword).
3. **Generation**: Gemini synthesizes the retrieved transcript chunks into a clean, natural response.
4. **Memory Node**: Spool appends the QA pair to its chat history so nothing important gets dropped.

## Directory Structure
```text
Spool/
├── configs/                # YAML config files
├── src/
│   ├── exception/          # Custom exceptions
│   ├── infra/              # Configuration and infrastructure setup
│   ├── logger/             # Custom logging utilities
│   ├── spool/
│   │   ├── data/           # Transcript loaders, splitters, and Chroma store
│   │   └── llm/            # Model config, prompt generator, and retrievers
│   └── ui/
│       ├── components.py   # Streamlit UI components
│       └── core.py         # Pipeline initialization and state management
├── app.py                  # Entry point for Streamlit
└── pyproject.toml
```

## Getting Started

### 1. Setup
Clone the repo and install everything with `uv`:
```bash
git clone <repo-url>
cd Spool
uv sync
```

### 2. Configure
You'll need a Google API key. Create a `.env` in the project root:
```env
GOOGLE_API_KEY="your_google_api_key"
```

### 3. Run
```bash
uv run streamlit run app.py
```
Open **http://localhost:8501** and start chatting.

# One-Desk

One-Desk is a full‑stack application that combines:
- A FastAPI backend for document processing, embeddings, vector search, and LLM-powered retrieval.
- A React (v19) + Vite frontend for a fast, modern client experience.

It is designed to support workflows like RAG (Retrieval Augmented Generation), including PDF/DOCX ingestion, vector indexing with FAISS, and querying via popular LLM providers.

## Key Features

- FastAPI backend with automatic OpenAPI docs at `/docs` and `/redoc`.
- Document parsing: PDF and DOCX support (PyMuPDF, pdfplumber, python-docx).
- Embeddings and semantic search: sentence-transformers + FAISS.
- Optional RAG helpers: LangChain integrations available.
- LLM providers:
  - OpenAI (via `openai` SDK)
  - Google Gemini (via `google-generativeai`)
- Caching and performance: Redis and DiskCache.
- Auth-ready foundation: JWT signing (python-jose), password hashing (passlib[bcrypt]).
- Observability: structured logging (structlog) and Prometheus metrics.
- Frontend: React 19 + Vite with modern dev tooling.
- Developer experience: pytest, pytest-asyncio, black, isort.

## Repository Structure

```
.
├─ .gitignore
├─ frontend/                 # React + Vite app
│  ├─ package.json           # React 19 + Vite 7, ESLint 9
│  └─ README.md              # Template notes from Vite/React
├─ project/                  # Backend (FastAPI) - pinned dependencies
│  └─ requirements.txt       # Pinned backend deps (OpenAI, FAISS, etc.)
└─ requirements.txt          # Backend deps (LangChain, Gemini, etc.) - unpinned/looser
```

## Tech Stack

- Backend:
  - Python (FastAPI, Uvicorn)
  - Pydantic v2, pydantic-settings
  - sentence-transformers, FAISS, NumPy
  - PyMuPDF, pdfplumber, python-docx
  - OpenAI SDK, Google Generative AI
  - (Optional helpers) LangChain, langchain-community, langchain-google-genai
  - Redis, DiskCache
  - structlog, prometheus-client
  - Tooling: pytest, pytest-asyncio, black, isort

- Frontend:
  - React 19, Vite 7
  - ESLint 9 and React Hooks plugin
  - Type support available via @types packages

- Languages in repo:
  - Python, JavaScript, CSS, HTML

## Prerequisites

- Python 3.10+ recommended
- Node.js 18+ and npm 9+ (for the frontend)
- Redis (optional but recommended for caching), e.g., via Docker:
  ```
  docker run -p 6379:6379 --name redis -d redis:7
  ```

## Setup and Installation

You can set up the backend using either the pinned dependencies in `project/requirements.txt` (stable, reproducible) or the broader set in the root `requirements.txt` (more flexible, latest).

### 1) Backend (recommended: pinned)

```bash
# From repo root
cd project

# Create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install pinned backend dependencies
pip install -U pip
pip install -r requirements.txt
```

### 2) Backend (alternative: latest/unpinned)

```bash
# From repo root
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
```

### 3) Frontend

```bash
cd frontend
npm install
```

## Configuration

Create a `.env` file in your backend working directory (repo root or `project/`, depending on where you run the app). Common variables:

```
# LLM providers (use what you need)
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

# Caching / storage
REDIS_URL=redis://localhost:6379
# Optional: configure vector index path
VECTOR_DB_DIR=.vectorstore

# App settings (examples)
ENV=development
LOG_LEVEL=INFO
```

If you use pydantic-settings, these will be loaded automatically when configured in the app.

## Running the App

### Backend (FastAPI)

Run with Uvicorn (adjust the module:app path to match your codebase):

```bash
# Example patterns — choose the one that matches your entrypoint
uvicorn main:app --reload
# or
uvicorn app.main:app --reload
# or from project/:
cd project && uvicorn main:app --reload
```

Once running, visit:
- API docs (Swagger): http://localhost:8000/docs
- API docs (ReDoc): http://localhost:8000/redoc

### Frontend (React + Vite)

```bash
cd frontend
npm run dev
```

By default, Vite serves on http://localhost:5173 (check your terminal output).

## Building

- Frontend production build:
  ```bash
  cd frontend
  npm run build
  npm run preview  # optional local preview
  ```

- Backend: Typically deployed by starting Uvicorn/Gunicorn. Example:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

## Development Workflow

- Formatting and imports:
  ```bash
  black .
  isort .
  ```
- Tests:
  ```bash
  pytest
  ```
- Linting (frontend):
  ```bash
  cd frontend
  npm run lint
  ```

## Notes on Capabilities

- Document ingestion: The dependencies support processing PDFs (PyMuPDF, pdfplumber) and DOCX (python-docx).
- Embeddings & retrieval: sentence-transformers for embedding generation and FAISS for efficient vector search.
- RAG helpers: LangChain utilities are included in the top-level requirements to speed up retrieval pipelines if desired.
- Multi-provider LLMs: Both OpenAI and Google Gemini SDKs are supported; set API keys accordingly.
- Caching: Redis and DiskCache can be used to cache intermediate computations and responses.
- Observability: `structlog` for structured logs, `prometheus-client` for exporting metrics.

## Troubleshooting

- If FastAPI docs are not accessible, confirm your `uvicorn` target (`module:app`) matches the actual app.
- Ensure your `.env` is in the correct directory and that environment variables are loaded by the settings layer.
- Vite requires Node 18+; verify your Node.js version if the frontend fails to start.

## Contributing

1. Fork the repo and create a feature branch.
2. Set up backend and frontend as described above.
3. Add/modify tests where applicable.
4. Format and lint your changes.
5. Open a pull request with a clear description of your changes.

## License

No license is currently specified in this repository.

---
If you maintainers have a canonical entrypoint (e.g., `project/main.py` or `project/app/main.py`) or a specific environment variable schema, please align the commands and configuration sections accordingly.

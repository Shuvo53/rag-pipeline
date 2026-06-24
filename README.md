# Local RAG Pipeline 🔍

A fully local Retrieval-Augmented Generation (RAG) pipeline built with Ollama, ChromaDB, and LLaMA 3.2. No API costs, no internet required after setup.

## What it does
Lets you ask natural language questions about any PDF and get accurate answers grounded strictly in that document.

## Tech Stack
- **Ollama** — local LLM server
- **LLaMA 3.2** — answer generation
- **nomic-embed-text** — text embeddings
- **ChromaDB** — vector store (persists on disk)
- **pypdf** — PDF text extraction

## Requirements
- Mac M1 or any machine with 8GB+ RAM
- Python 3.11+
- Ollama installed

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
```

### 2. Create virtual environment
```bash
python3 -m venv rag-env
source rag-env/bin/activate
```

### 3. Install dependencies
```bash
pip install chromadb ollama pypdf langchain langchain-community
```

### 4. Install Ollama and pull models
```bash
brew install ollama
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 5. Add your PDF
Drop any PDF into the project folder and update the filename in `rag_pipeline.py`:
```python
chunks = load_and_chunk("yourfile.pdf")
```

### 6. Run
```bash
ollama serve  # in a separate terminal if not already running
python3 rag_pipeline.py
```

## Usage
Once running, type any question about your PDF and hit Enter.
Type `exit` to quit.

## Project Structure
rag-project/

├── rag_pipeline.py       # main pipeline

├── test_ollama.py        # verification script

├── rag_architecture.pdf  # sample document

├── chroma_db/            # vector store (auto-generated)

└── rag-env/              # virtual environment


## Notes
- `chroma_db/` is auto-generated on first run and persists between sessions
- To switch documents, delete `chroma_db/` and update the PDF filename
- Answers are strictly grounded in the PDF — won't hallucinate outside the document
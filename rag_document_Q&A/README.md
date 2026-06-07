# 🔍 RAG Document Q&A — Company Intelligence Agent

> Ask natural language questions against any company document. Get analyst-quality answers with source citations — in seconds.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=flat-square)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?style=flat-square&logo=google)](https://ai.google.dev)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6B35?style=flat-square)](https://chromadb.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## What This Solves

Reading through a 100-page earnings report to answer 3 questions takes hours. This agent does it in seconds — and synthesizes, not just copies.

**Tested on:** Walt Disney FY2025 Earnings Report

**Sample answers:**

> **Q: "What is our current revenue trend?"**
> A: "Walt Disney's total revenue for Fiscal 2025 reached $53.4 billion — a 12% increase from $47.6 billion in Fiscal 2024, indicating strong positive momentum."

> **Q: "Which departments are underperforming?"**
> A: "Linear Networks and Entertainment DTC SVOD are underperforming. Linear Networks operating income declined $107M YoY; DTC SVOD reported a $2.6B loss in FY2025."

> **Q: "What were the key risks last quarter?"**
> A: "Key risks include a $452M net loss from A+E investment impairment, a 15% decline in domestic advertising revenue, and declining affiliate revenues."

---

## Architecture

```
PDF / DOCX Documents
        │
        ▼
  LangChain Loader  ──▶  PyPDFLoader / Docx2txtLoader
        │
        ▼
  Text Chunking  ──▶  RecursiveCharacterTextSplitter (500 chars, 50 overlap)
        │
        ▼
  Embeddings  ──▶  Sentence Transformers (all-mpnet-base-v2)
        │
        ▼
  ChromaDB  ──▶  Vector store (persistent)
        │
        ▼
  Two-Stage Retrieval:
    1. Dense vector search (top-15 chunks)
    2. CrossEncoder reranking (top-5)
        │
        ▼
  Gemini 2.5 Flash  ──▶  Analyst-style synthesis
        │
        ▼
  Answer + Source Attribution
```

---

## Quick Start

```bash
git clone https://github.com/Swty13/genai-coding.git
cd genai-coding

pip install -r requirements.txt

export GEMINI_API_KEY="your_key_here"

# Step 1: Ingest your documents (drop PDFs into /data)
python document_processor.py

# Step 2: Ask questions via CLI
python main.py

# Step 3: Or launch the Streamlit UI
streamlit run app.py

# Optional: Run evaluation
python run_eval.py
```

---

## Key Design Decisions

| Decision | What & Why |
|---|---|
| **Two-stage retrieval** | Dense vector (recall) + CrossEncoder reranking (precision) — better than either alone |
| **Sentence Transformers** | Local embeddings, no API cost, strong semantic understanding |
| **ChromaDB** | Persistent local vector store, zero infrastructure overhead |
| **Gemini 2.5 Flash** | Fast, cheap, analyst-quality synthesis with system instructions |
| **Chunk overlap** | 50-char overlap prevents answers from splitting across chunk boundaries |

---

## Evaluation Results

Evaluated on Walt Disney FY2025 earnings report. No ground-truth labels — scored on retrieval confidence (cosine similarity) and answer quality.

See [`results/eval_20260223_1343.json`](./results/eval_20260223_1343.json) and [`results/eval_scores.png`](./results/eval_scores.png).

---

## Supported Document Types

- ✅ PDF (text-based and scanned with OCR fallback)
- ✅ DOCX
- ✅ TXT
- 🔜 HTML, CSV (coming soon)

---

## Stack

- **Document loading**: LangChain (PyPDFLoader, Docx2txtLoader)
- **Chunking**: RecursiveCharacterTextSplitter
- **Embeddings**: Sentence Transformers (all-mpnet-base-v2)
- **Vector store**: ChromaDB
- **Reranker**: CrossEncoder
- **LLM**: Google Gemini 2.5 Flash
- **UI**: Streamlit

---



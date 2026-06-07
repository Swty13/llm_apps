# LLM Apps - Production AI Application Collection

> A curated collection of real-world LLM applications — each solving a specific business problem, fully implemented and ready to run.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=flat-square)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📁 Projects

| Project | What it does | Stack | Business Value |
|---|---|---|---|
| [🔍 RAG Document Q&A](https://github.com/Swty13/genai-coding) | Chat with company documents | LangChain · ChromaDB · Gemini | Cuts research time by ~80% |
| [✍️ Blog Writer with CrewAI](https://github.com/Swty13/blog-writer-crewai) | 4-agent system that writes full blog posts | CrewAI · Streamlit · OpenAI | Content in minutes, not hours |
| [🎙️ Podcast Summarizer](https://github.com/Swty13/Podcast_Summarizer) | YouTube podcast → structured summary | Gemini · Streamlit | 2-hr podcast → 5-min summary |
| [🤖 Reddit MCP Agent](https://github.com/Swty13/llm_apps/tree/master/mcp_apps/reddit_mcp_agent) | Reddit analytics via Model Context Protocol | MCP · FastAPI · Streamlit | Real-time community intelligence |

---

## 🔍 RAG Document Q&A

**Repo:** [github.com/Swty13/rag_document_Q-A](https://github.com/Swty13/rag_document_Q-A)

Ask natural language questions against any company document — earnings reports, legal contracts, internal policies. Built with a two-stage retrieval pipeline (dense vector → CrossEncoder reranking) and Google Gemini for synthesis.

**Tested on:** Walt Disney FY2025 Earnings Report (PDF)

**Sample Q&A:**
> *"What is our current revenue trend?"*
> → "Walt Disney's total revenue for Fiscal 2025 reached $53.4 billion, a 12% increase from $47.6 billion in Fiscal 2024."

**Stack:** LangChain · ChromaDB · Sentence Transformers · Gemini 2.5 Flash · Streamlit

➡️ **[View full project →](https://github.com/Swty13/rag_document_Q-A)**

---

## ✍️ Blog Writer with CrewAI

**Repo:** [github.com/Swty13/blog-writer-crewai](https://github.com/Swty13/blog-writer-crewai)

A multi-agent system that takes a URL, PDF, or image and produces a fully written, SEO-optimized blog post. Four specialized agents work in sequence: Research → Strategy → Writing → Editing.

**Input sources:** URL, PDF, Image
**Output:** Complete blog post (300–3000 words), SEO keywords, structured sections

**Stack:** CrewAI · Streamlit · Azure OpenAI · PyPDF2

➡️ **[View full project →](https://github.com/Swty13/blog-writer-crewai)**

---

## 🎙️ Podcast Summarizer

**Repo:** [github.com/Swty13/Podcast_Summarizer](https://github.com/Swty13/Podcast_Summarizer)

Paste any YouTube podcast URL and get a clean, structured summary in seconds. No more sitting through 2-hour episodes to find the 10 minutes that matter. Powered by Google Gemini and the YouTube transcript API.

**Input:** YouTube URL
**Output:** Key points, main takeaways, timestamps

**Stack:** Google Gemini · YouTube Transcript API · Streamlit

➡️ **[View full project →](https://github.com/Swty13/Podcast_Summarizer)**

---

## 🤖 Reddit MCP Agent

**Repo:** [github.com/Swty13/llm_apps — mcp_apps/reddit_mcp_agent](https://github.com/Swty13/llm_apps/tree/master/mcp_apps/reddit_mcp_agent)

A full Reddit data exploration suite built on the Model Context Protocol (MCP). Three interfaces — Streamlit dashboard, FastAPI REST API, Flask web app — for browsing hot posts, analyzing comments, tracking subreddit stats, and even creating posts.

**Interfaces:** Streamlit · FastAPI (with Swagger docs) · Flask
**Features:** Hot posts, search, comment analysis, analytics dashboard, post creation

**Stack:** MCP · PRAW · Streamlit · FastAPI · Plotly

➡️ **[View full project →](https://github.com/Swty13/llm_apps/tree/master/mcp_apps/reddit_mcp_agent)**

---

## 🛠️ Common Stack

- **Language**: Python 3.10+
- **LLMs**: OpenAI GPT-4, Google Gemini, Azure OpenAI
- **Frameworks**: LangChain, CrewAI, MCP
- **UIs**: Streamlit, FastAPI, Flask
- **Vector DBs**: ChromaDB, FAISS

---



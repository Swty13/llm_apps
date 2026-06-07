# 🎙️ Podcast Summarizer

> Paste a YouTube podcast URL. Get a clean, structured summary in seconds. No more sitting through 2-hour episodes.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=flat-square&logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## What This Does

Paste any YouTube podcast URL → get a structured summary with key points, main takeaways, and notable quotes. Built for researchers, content teams, and anyone who values their time.

**Business use cases:**
- Research teams monitoring competitor podcasts
- Content marketers repurposing podcast content
- Executives who need briefings without listening
- Students and learners extracting knowledge fast

**Result:** A 2-hour podcast becomes a 5-minute read.

[![Watch Demo](https://raw.githubusercontent.com/Swty13/Podcast_Summarizer/main/pod_image.png)](https://github.com/Swty13/Podcast_Summarizer/blob/main/podcast_video.mov)

---

## How It Works

```
YouTube URL
     │
     ▼
YouTube Transcript API  ──▶  Extracts full episode transcript
     │
     ▼
Google Gemini  ──▶  Summarizes + structures key points
     │
     ▼
Streamlit UI  ──▶  Displays clean, readable summary
```

---

## Quick Start

```bash
git clone https://github.com/Swty13/Podcast_Summarizer.git
cd Podcast_Summarizer

pip install -r requirements.txt

# Add your Gemini API key
export GOOGLE_API_KEY="your_key_here"

streamlit run main.py
```

Open `http://localhost:8501`, paste a YouTube URL, click **Summarize**.

---

## Features

- **YouTube integration** — works with any public YouTube podcast/video
- **Auto-transcription** — uses YouTube's own transcript (no audio processing needed)
- **AI summarization** — Gemini extracts key points, not just truncates text
- **Structured output** — main topics, key takeaways, notable quotes
- **Fast** — most episodes summarized in under 30 seconds

---

## Stack

- **UI**: Streamlit
- **LLM**: Google Gemini API
- **Transcript**: `youtube_transcript_api`
- **Language**: Python 3.10+

---

## Requirements

```
streamlit
google-generativeai
youtube_transcript_api
requests
```

---



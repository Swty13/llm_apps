# 🔥 Reddit MCP Explorer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.18.0-green.svg)](https://modelcontextprotocol.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Beautiful, modern interfaces for exploring Reddit data using the Model Context Protocol (MCP)**

A comprehensive Reddit data exploration suite featuring multiple beautiful UIs built on top of the Model Context Protocol. Explore subreddits, analyze posts, view comments, and gain insights with interactive visualizations.


![Streamlit Interface](/images/image_mcp_reddit.png)
*Beautiful Streamlit interface with real-time analytics*


## ✨ Features

### 🎨 **Multiple Beautiful Interfaces**
- **🌟 Streamlit App** - Interactive dashboard with real-time analytics
- **⚡ FastAPI Server** - REST API with OpenAPI documentation
- **🌐 Flask Web App** - Modern glassmorphism design

### 🛠️ **Powerful Reddit Tools**
- 🔥 **Hot Posts Explorer** - Fetch trending posts with metrics
- 🔍 **Advanced Search** - Search within subreddits with filters
- 💬 **Comment Analysis** - Deep dive into post discussions
- 📊 **Analytics Dashboard** - Visualizations and correlations
- ℹ️ **Subreddit Information** - Complete community stats
- ➕ **Post Creation** - Create text and link posts
- 🔐 **Smart Authentication** - Handles both script and web apps

### 📈 **Analytics & Visualizations**
- Score distribution histograms
- Author activity analysis
- Engagement correlation charts
- Time-based posting patterns
- Performance metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Reddit API credentials

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/reddit_mcp_agent.git
cd reddit-mcp-explorer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Reddit API
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new app (choose "script" for full functionality)
3. Create your `.env` file:

```bash
# src/.env
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="YourApp-MCP/1.0"
export REDDIT_USERNAME="your_username"  # Optional, for posting
export REDDIT_PASSWORD="your_password"  # Optional, for posting
```

### 4. Run Your Preferred Interface

#### 🎨 Streamlit App (Recommended)
```bash
./run_streamlit.sh
# or
cd src && source .env && streamlit run streamlit_app.py
```
**Access:** http://localhost:8501

#### ⚡ FastAPI Server
```bash
./run_fastapi.sh
# or
cd src && source .env && python fastapi_server.py
```
**API Docs:** http://localhost:8000/docs

## 🏗️ Architecture

```
reddit-mcp-explorer/
├── src/
│   ├── server.py              # Core MCP server
│   ├── reddit_client.py       # Async MCP client
│   ├── reddit_sync_client.py  # Synchronous wrapper
│   ├── streamlit_app.py       # 🎨 Main Streamlit UI
│   ├── fastapi_server.py      # ⚡ REST API server
│   ├── reddit_ui.py           # 🌐 Flask web interface
│   ├── input_utils.py         # Input validation utilities
│   └── .env                   # Environment configuration
├── requirements.txt           # Python dependencies
├── run_streamlit.sh          # Streamlit launcher
├── run_fastapi.sh            # FastAPI launcher
└── README.md                 # This file
```

## 🔧 API Reference

### REST Endpoints (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fetch_posts` | POST | Get hot posts from subreddit |
| `/api/search_posts` | POST | Search posts within subreddit |
| `/api/get_comments` | POST | Retrieve post comments |
| `/api/subreddit_info` | POST | Get subreddit information |
| `/api/post_comment` | POST | Reply to posts |
| `/api/create_post` | POST | Create new posts |

### Example Usage

#### Fetch Posts
```python
import requests

response = requests.post("http://localhost:8000/api/fetch_posts",
                        json={"subreddit": "python", "limit": 10})
data = response.json()
```

#### Direct MCP Client
```python
from reddit_sync_client import get_reddit_client

client = get_reddit_client()
posts = client.fetch_posts("python", 10)
```

## 🎯 Use Cases

- **🔬 Content Research** - Analyze trending topics and discussions
- **📈 Community Insights** - Understand subreddit dynamics and user behavior
- **🎯 Engagement Analysis** - Find optimal posting strategies and timing
- **📊 Data Collection** - Gather Reddit data for research and analysis
- **🤖 Bot Development** - Build Reddit automation and monitoring tools
- **📰 Content Discovery** - Find relevant posts and discussions

## 🛡️ Features & Security

- **Smart Input Validation** - Automatic cleaning of subreddit names and post IDs
- **Error Handling** - Comprehensive error handling with clear messages
- **Rate Limiting** - Respectful API usage following Reddit guidelines
- **Authentication Flexibility** - Supports both authenticated and read-only modes
- **Async Performance** - High-performance async operations
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 🧪 Testing

### Test the MCP Connection
```bash
cd src && source .env && python test_connection.py
```

### Test Synchronous Client
```bash
cd src && source .env && python test_sync_client.py
```

## 📚 Documentation

- **[Reddit API](https://www.reddit.com/dev/api/)** - Official Reddit API docs
- **[MCP Protocol](https://modelcontextprotocol.io/)** - Model Context Protocol specification
- **[PRAW Documentation](https://praw.readthedocs.io/)** - Python Reddit API wrapper
- **[Streamlit Docs](https://docs.streamlit.io/)** - Streamlit framework
- **[FastAPI Docs](https://fastapi.tiangolo.com/)** - FastAPI framework

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📋 Requirements

### Core Dependencies
- `mcp>=1.18.0` - Model Context Protocol
- `praw>=7.7.0` - Python Reddit API Wrapper
- `streamlit>=1.28.0` - Interactive web apps
- `fastapi>=0.104.0` - Modern web framework
- `plotly>=5.17.0` - Interactive visualizations
- `pandas>=2.1.0` - Data analysis
- `uvicorn[standard]` - ASGI server

### Reddit App Setup
1. **Script App** (Full functionality):
   - Post creation ✅
   - Comment posting ✅
   - Full read access ✅

2. **Web App** (Read-only):
   - Post creation ❌
   - Comment posting ❌
   - Full read access ✅

## 🐛 Troubleshooting

### Common Issues

**"Server connection closed" error:**
```bash
# Make sure MCP is installed
pip install mcp

# Check environment variables
source .env && env | grep REDDIT
```

**"Invalid JSON response" error:**
- Usually caused by subreddit names with spaces
- The app now automatically cleans input (e.g., "r/ python" → "python")

**"Script app required" error:**
- Change your Reddit app type to "script" for posting features
- Or use read-only mode for browsing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [PRAW](https://praw.readthedocs.io/) for Reddit API access
- Beautiful UIs with [Streamlit](https://streamlit.io/) and [FastAPI](https://fastapi.tiangolo.com/)
- Data visualizations with [Plotly](https://plotly.com/)

---

<p align="center">
  <strong>🚀 Happy Reddit Exploring! 🚀</strong>
</p>

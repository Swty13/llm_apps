#!/usr/bin/env python3
"""
FastAPI server for Reddit MCP Client
Provides REST API endpoints for Reddit operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
from reddit_client import RedditMCPClient

app = FastAPI(
    title="Reddit MCP API",
    description="REST API for Reddit MCP operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
reddit_client = None
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "server.py")

# Pydantic models for request/response
class FetchPostsRequest(BaseModel):
    subreddit: str
    limit: Optional[int] = 10

class SearchPostsRequest(BaseModel):
    subreddit: str
    query: str
    limit: Optional[int] = 10

class GetCommentsRequest(BaseModel):
    post_id: str

class SubredditInfoRequest(BaseModel):
    subreddit: str

class PostCommentRequest(BaseModel):
    post_id: str
    comment_text: str

class CreatePostRequest(BaseModel):
    subreddit: str
    title: str
    content: Optional[str] = None
    url: Optional[str] = None

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

async def get_reddit_client():
    """Get or create Reddit MCP client"""
    global reddit_client
    if reddit_client is None:
        reddit_client = RedditMCPClient(server_path)
        await reddit_client.start()
    return reddit_client

@app.on_event("startup")
async def startup_event():
    """Initialize Reddit client on startup"""
    try:
        await get_reddit_client()
        print("✅ Reddit MCP client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Reddit client: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    global reddit_client
    if reddit_client:
        await reddit_client.close()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Reddit MCP FastAPI Server",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/fetch_posts", response_model=APIResponse)
async def fetch_posts(request: FetchPostsRequest):
    """Fetch hot posts from a subreddit"""
    try:
        client = await get_reddit_client()
        result = await client.fetch_posts(request.subreddit, request.limit)
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search_posts", response_model=APIResponse)
async def search_posts(request: SearchPostsRequest):
    """Search for posts in a subreddit"""
    try:
        client = await get_reddit_client()
        result = await client.search_posts(request.subreddit, request.query, request.limit)
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/get_comments", response_model=APIResponse)
async def get_comments(request: GetCommentsRequest):
    """Get comments for a specific post"""
    try:
        client = await get_reddit_client()
        result = await client.get_comments(request.post_id)
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subreddit_info", response_model=APIResponse)
async def get_subreddit_info(request: SubredditInfoRequest):
    """Get information about a subreddit"""
    try:
        client = await get_reddit_client()
        result = await client.get_subreddit_info(request.subreddit)
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/post_comment", response_model=APIResponse)
async def post_comment(request: PostCommentRequest):
    """Post a comment on a Reddit post"""
    try:
        client = await get_reddit_client()
        result = await client.post_comment(request.post_id, request.comment_text)
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create_post", response_model=APIResponse)
async def create_post(request: CreatePostRequest):
    """Create a new post in a subreddit"""
    try:
        client = await get_reddit_client()
        result = await client.post_to_subreddit(
            request.subreddit,
            request.title,
            request.content,
            request.url
        )
        return APIResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        client = await get_reddit_client()
        return {"status": "healthy", "reddit_client": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Reddit MCP FastAPI Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Interactive API: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
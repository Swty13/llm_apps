#!/usr/bin/env python3
"""
Synchronous wrapper for Reddit MCP Client
Works better with Streamlit's execution model
"""

import asyncio
import threading
import queue
import json
import os
from typing import Dict, List, Any
from reddit_client import RedditMCPClient

class RedditSyncClient:
    """Synchronous wrapper for Reddit MCP Client"""

    def __init__(self):
        self.client = None
        self.loop = None
        self.thread = None
        self.initialized = False

    def _run_event_loop(self, loop, ready_event):
        """Run event loop in separate thread"""
        asyncio.set_event_loop(loop)
        ready_event.set()
        loop.run_forever()

    def initialize(self):
        """Initialize the client and event loop"""
        if self.initialized:
            return True

        try:
            # Create new event loop in separate thread
            self.loop = asyncio.new_event_loop()
            ready_event = threading.Event()

            self.thread = threading.Thread(
                target=self._run_event_loop,
                args=(self.loop, ready_event),
                daemon=True
            )
            self.thread.start()
            ready_event.wait()  # Wait for loop to be ready

            # Create client
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(current_dir, "server.py")
            self.client = RedditMCPClient(server_path)

            # Initialize client
            future = asyncio.run_coroutine_threadsafe(
                self.client.start(), self.loop
            )
            future.result(timeout=10)  # Wait max 10 seconds

            self.initialized = True
            return True

        except Exception as e:
            print(f"❌ Failed to initialize Reddit client: {e}")
            return False

    def _run_async(self, coro, timeout=30):
        """Run async coroutine and return result"""
        if not self.initialized:
            raise Exception("Client not initialized. Call initialize() first.")

        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result(timeout=timeout)

    def fetch_posts(self, subreddit: str, limit: int = 10) -> Dict:
        """Fetch hot posts from a subreddit"""
        return self._run_async(self.client.fetch_posts(subreddit, limit))

    def search_posts(self, subreddit: str, query: str, limit: int = 10) -> Dict:
        """Search for posts in a subreddit"""
        return self._run_async(self.client.search_posts(subreddit, query, limit))

    def get_comments(self, post_id: str) -> Dict:
        """Get comments for a specific post"""
        return self._run_async(self.client.get_comments(post_id))

    def get_subreddit_info(self, subreddit: str) -> Dict:
        """Get information about a subreddit"""
        return self._run_async(self.client.get_subreddit_info(subreddit))

    def post_comment(self, post_id: str, comment_text: str) -> Dict:
        """Post a comment on a Reddit post"""
        return self._run_async(self.client.post_comment(post_id, comment_text))

    def post_to_subreddit(self, subreddit: str, title: str, content: str = None, url: str = None) -> Dict:
        """Create a new post in a subreddit"""
        return self._run_async(self.client.post_to_subreddit(subreddit, title, content, url))

    def close(self):
        """Close the client and cleanup"""
        if self.client and self.loop:
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self.client.close(), self.loop
                )
                future.result(timeout=5)
            except:
                pass

        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

        self.initialized = False

# Global client instance for Streamlit
_global_client = None

def get_reddit_client():
    """Get or create global Reddit client"""
    global _global_client
    if _global_client is None:
        _global_client = RedditSyncClient()
        if not _global_client.initialize():
            raise Exception("Failed to initialize Reddit client")
    return _global_client
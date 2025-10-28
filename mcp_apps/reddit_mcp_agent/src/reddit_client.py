#!/usr/bin/env python3
import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

class RedditMCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.process = None

    async def start(self):
        """Start the MCP server process"""
        self.process = await asyncio.create_subprocess_exec(
            sys.executable, self.server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Initialize the connection
        await self._send_message({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "reddit-client",
                    "version": "1.0.0"
                }
            }
        })

        # Wait for initialization response
        response = await self._read_message()
        if response.get("result"):
            print("✅ Connected to Reddit MCP server")
        else:
            raise Exception(f"Failed to initialize: {response}")

    async def _send_message(self, message: Dict[str, Any]):
        """Send a JSON-RPC message to the server"""
        if not self.process:
            raise Exception("Server not started")

        json_str = json.dumps(message) + "\n"
        self.process.stdin.write(json_str.encode())
        await self.process.stdin.drain()

    async def _read_message(self) -> Dict[str, Any]:
        """Read a JSON-RPC message from the server"""
        if not self.process:
            raise Exception("Server not started")

        line = await self.process.stdout.readline()
        if not line:
            raise Exception("Server connection closed")

        return json.loads(line.decode().strip())

    def _safe_json_parse(self, text: str) -> Dict:
        """Safely parse JSON with error handling"""
        if not text or text.strip() == "":
            raise Exception("Empty response from server")

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {text[:100]}... Error: {e}")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server"""
        message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        await self._send_message(message)
        response = await self._read_message()

        if "error" in response:
            raise Exception(f"Tool error: {response['error']}")

        return response.get("result", {}).get("content", [{}])[0].get("text", "")

    async def fetch_posts(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """Fetch hot posts from a subreddit"""
        result = await self.call_tool("fetchPosts", {
            "subreddit": subreddit,
            "limit": limit
        })
        return self._safe_json_parse(result)

    async def search_posts(self, subreddit: str, query: str, limit: int = 10) -> List[Dict]:
        """Search for posts in a subreddit"""
        result = await self.call_tool("searchPosts", {
            "subreddit": subreddit,
            "query": query,
            "limit": limit
        })
        return self._safe_json_parse(result)

    async def get_comments(self, post_id: str) -> Dict:
        """Get comments for a specific post"""
        result = await self.call_tool("getComments", {
            "post_id": post_id
        })
        return self._safe_json_parse(result)

    async def get_subreddit_info(self, subreddit: str) -> Dict:
        """Get information about a subreddit"""
        result = await self.call_tool("getSubredditInfo", {
            "subreddit": subreddit
        })
        return self._safe_json_parse(result)

    async def post_comment(self, post_id: str, comment_text: str) -> Dict:
        """Post a comment on a Reddit post"""
        result = await self.call_tool("postComment", {
            "post_id": post_id,
            "comment_text": comment_text
        })
        return self._safe_json_parse(result)

    async def post_to_subreddit(self, subreddit: str, title: str, content: str = None, url: str = None) -> Dict:
        """Create a new post in a subreddit"""
        args = {
            "subreddit": subreddit,
            "title": title
        }
        if content:
            args["content"] = content
        if url:
            args["url"] = url

        result = await self.call_tool("postToSubreddit", args)
        return self._safe_json_parse(result)

    async def close(self):
        """Close the connection to the server"""
        if self.process:
            self.process.terminate()
            await self.process.wait()

async def main():
    """Example usage of the Reddit MCP client"""
    server_path = "server.py"

    client = RedditMCPClient(server_path)

    try:
        await client.start()

        # Example: Fetch posts from r/python
        print("\n🔥 Hot posts from r/python:")
        posts = await client.fetch_posts("python", limit=3)
        for i, post in enumerate(posts["posts"], 1):
            print(f"{i}. {post['title']}")
            print(f"   👤 {post['author']} | ⬆️ {post['score']} | 💬 {post['num_comments']}")
            print(f"   🔗 {post['permalink']}\n")

        # Example: Search for posts
        print("🔍 Searching for 'tutorial' in r/python:")
        search_results = await client.search_posts("python", "tutorial", limit=2)
        for i, post in enumerate(search_results["posts"], 1):
            print(f"{i}. {post['title']}")
            print(f"   👤 {post['author']} | ⬆️ {post['score']}\n")

        # Example: Get subreddit info
        print("ℹ️ Subreddit info for r/python:")
        info = await client.get_subreddit_info("python")
        print(f"Subscribers: {info['subscribers']:,}")
        print(f"Description: {info['public_description'][:100]}...")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
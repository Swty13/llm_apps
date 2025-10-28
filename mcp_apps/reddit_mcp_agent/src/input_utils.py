#!/usr/bin/env python3
"""
Input validation utilities for Reddit MCP client
"""

def clean_subreddit_name(subreddit_input: str) -> str:
    """Clean and validate subreddit name input"""
    if not subreddit_input:
        return ""

    # Remove r/ prefix if present, strip whitespace, remove spaces
    cleaned = subreddit_input.strip().replace("r/", "").replace(" ", "")

    # Basic validation - subreddit names should be alphanumeric with underscores
    if cleaned and not cleaned.replace("_", "").replace("-", "").isalnum():
        return ""

    return cleaned

def validate_post_id(post_id: str) -> str:
    """Clean and validate Reddit post ID"""
    if not post_id:
        return ""

    # Remove t3_ prefix if present, strip whitespace
    cleaned = post_id.strip().replace("t3_", "")

    # Basic validation - post IDs should be alphanumeric
    if cleaned and not cleaned.isalnum():
        return ""

    return cleaned
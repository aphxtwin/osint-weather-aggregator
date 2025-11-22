"""
Minimal OSINT data fetching service using Reddit Search API.
Only fetches recent post titles + selftext as required by the assignment.
"""

import httpx
import logging
from typing import List, Dict, Any
from app.config import REDDIT_SEARCH_QUERY, REDDIT_SEARCH_LIMIT, REDDIT_SEARCH_SORT

logger = logging.getLogger(__name__)

REDDIT_SEARCH_URL = "https://www.reddit.com/r/all/search.json"
BRAND_NAME = "Gymshark"  # Hardcoded brand name


async def fetch_osint_data() -> Dict[str, Any]:
    """
    Fetch minimal OSINT data from Reddit search API.

    Returns:
        A dict containing brand_name and posts list with text snippets for LLM processing.
    """
    logger.info(f"Fetching Reddit OSINT data for query: {REDDIT_SEARCH_QUERY}")

    params = {
        "q": REDDIT_SEARCH_QUERY,
        "limit": REDDIT_SEARCH_LIMIT,
        "sort": REDDIT_SEARCH_SORT,
        "restrict_sr": False,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(REDDIT_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

    posts_raw = data.get("data", {}).get("children", [])

    # Minimal mapping of required info
    posts = []
    for item in posts_raw:
        if item.get("kind") != "t3":  # skip non-posts
            continue

        info = item.get("data", {})

        # Minimal required fields for the assignment
        posts.append({
            "title": info.get("title"),
            "text": info.get("selftext") or "",
        })

    logger.info(f"Fetched {len(posts)} Reddit posts for {BRAND_NAME}")

    return {
        "brand_name": BRAND_NAME,
        "posts": posts
    }

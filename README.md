# osint-weather-aggregator

PROJECT GOAL: Build a microservice that: Fetches weather data for one city, collects brand mentions from public sources (OSINT), uses Gemini 1.5 Flash to generate sentiment + news summaries, stores everything in a database, exposes data through FastAPI endpoints, and runs automatically once per day.

## Quick Setup

**Prerequisites:** Docker and Docker Compose installed

1. Clone the repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Configure your `.env` file with required API keys:
   - `GEMINI_API_KEY` - Get from https://ai.google.dev/
   - `N8N_ENCRYPTION_KEY` - Generate with: `openssl rand -base64 24`
   - `N8N_POSTGRES_PASSWORD` - Any secure password
4. Run setup again:
   ```bash
   ./setup.sh
   ```

That's it! Your services will be running at:
- FastAPI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- n8n: http://localhost:5678
- pgAdmin: http://localhost:5051

## Gemini AI Prompts

### Sentiment Analysis Prompt
```
Analyze the following brand-related text snippets and
provide a concise 1 or 2 sentence summary of the
overall public sentiment.
Be direct and avoid exaggeration.
Base your answer strictly on the text provided.
Text:

{osint_snippets}
```

### Trend Analysis Prompt
```
Summarize the major news or emerging trends about this brand
in 1 or 2 sentences based strictly on the text below. Keep
the tone neutral and avoid adding assumptions.

Text:
{osint_snippets}
```

**Model Used:** `gemini-2.5-flash`

**Input Format:** OSINT text snippets are formatted as:
```
Post 1:
Title: {post_title}
Text: {post_text}

Post 2:
Title: {post_title}
Text: {post_text}
...
```

## OSINT Sources

### Reddit
**API Endpoint:** Reddit Search API (`/r/all/search.json`)

**Data Collected:**
- Post titles
- Post selftext/body content

**Configuration** (via environment variables):
- `REDDIT_SEARCH_QUERY` - Search query (default: "gymshark")
- `REDDIT_SEARCH_LIMIT` - Number of posts to fetch (default: 10)
- `REDDIT_SEARCH_SORT` - Sort order: "new", "hot", "top", "relevance" (default: "new")

**Why Reddit:**
- Public API with no authentication required for read-only access



## Daily Automation with n8n

This project uses **n8n** (self-hosted workflow automation) for daily data aggregation.

![n8n Workflow](docs/images/workflow.png)


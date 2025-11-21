# osint-weather-aggregator

PROJECT GOAL: Build a microservice that: Fetches weather data for one city, collects brand mentions from public sources (OSINT), uses Gemini 1.5 Flash to generate sentiment + news summaries, stores everything in a database, exposes data through FastAPI endpoints, and runs automatically once per day.

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

"""
Gemini AI service for text analysis using Google's Gemini 1.5 Flash model.
"""
import logging
from google import genai
from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)


def initialize_gemini() -> genai.Client:
    """
    Initialize and configure the Gemini client.

    Returns:
        Configured Gemini Client instance

    Raises:
        ValueError: If API key is not configured
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured")

    return genai.Client(api_key=GEMINI_API_KEY)


def call_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and get the response.

    Args:
        prompt: Text prompt to send to Gemini

    Returns:
        Generated text response from Gemini

    Raises:
        Exception: If the API call fails
    """
    try:
        logger.info(f"Calling Gemini API with prompt length: {len(prompt)} characters")

        client = initialize_gemini()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        logger.info("Gemini API call successful")
        return response.text

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}", exc_info=True)
        raise


def analyze_sentiment(osint_snippets: str) -> str:
    """
    Analyze sentiment from brand-related OSINT text snippets.

    Args:
        osint_snippets: Text snippets from OSINT sources

    Returns:
        1-2 sentence sentiment summary from Gemini

    Raises:
        Exception: If the API call fails
    """
    prompt = f"""
    Analyze the following brand-related text snippets and
    provide a concise 1 or 2 sentence summary of the
    overall public sentiment.
    Be direct and avoid exaggeration.
    Base your answer strictly on the text provided.
    Text:

    {osint_snippets}
    """

    logger.info("Analyzing sentiment with Gemini")
    return call_gemini(prompt)


def analyze_trends(osint_snippets: str) -> str:
    """
    Analyze trends from brand-related OSINT text snippets.

    Args:
        osint_snippets: Text snippets from OSINT sources

    Returns:
        1-2 sentence trend summary from Gemini

    Raises:
        Exception: If the API call fails
    """
    prompt = f"""
    Summarize the major news or emerging trends about this brand 
    in 1 or 2 sentences based strictly on the text below. Keep 
    the tone neutral and avoid adding assumptions.

    Text:
    {osint_snippets}"""

    logger.info("Analyzing trends with Gemini")
    return call_gemini(prompt)
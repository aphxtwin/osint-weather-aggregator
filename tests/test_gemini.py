"""
Quick test script for Gemini API integration.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables BEFORE importing app modules
from dotenv import load_dotenv
env_path = project_root / '.env'
print(f"Loading .env from: {env_path}")
print(f".env file exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Debug: Check if API key is loaded
import os
api_key = os.getenv('GEMINI_API_KEY')
print(f"GEMINI_API_KEY loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API key length: {len(api_key)} characters")
print()

# NOW import app modules (after .env is loaded)
from app.services.gemini import call_gemini, analyze_sentiment, analyze_trends


def test_basic_call():
    """Test basic Gemini API call"""
    print("Testing basic Gemini API call...")
    try:
        response = call_gemini("Say hello in one sentence.")
        print(f"✓ Success: {response}")
        return True
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False


def test_sentiment_analysis():
    """Test sentiment analysis function"""
    print("\nTesting sentiment analysis...")
    sample_text = """
    - Customer review: "Love the quality of these shoes! Super comfortable."
    - Reddit post: "Just got my order, pretty disappointed with the shipping time."
    - Tweet: "Best purchase I made this year, highly recommend!"
    """
    try:
        response = analyze_sentiment(sample_text)
        print(f"✓ Sentiment Analysis: {response}")
        return True
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False


def test_trend_analysis():
    """Test trend analysis function"""
    print("\nTesting trend analysis...")
    sample_text = """
    - News article: "Brand announces new sustainable materials initiative"
    - Forum discussion: "Anyone notice they're expanding into European markets?"
    - Blog post: "The company just launched a collaboration with a major athlete"
    """
    try:
        response = analyze_trends(sample_text)
        print(f"✓ Trend Analysis: {response}")
        return True
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("GEMINI API TEST")
    print("=" * 60)

    results = []
    results.append(test_basic_call())
    results.append(test_sentiment_analysis())
    results.append(test_trend_analysis())

    print("\n" + "=" * 60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
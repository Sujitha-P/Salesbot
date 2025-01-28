import logging
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

def analyze_sentiment(user_input):
    try:
        sentiment_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Classify the sentiment of the following text related to consumer electronics. Provide only the sentiment category in one liner: Positive, Negative, Neutral, Very Positive, Very Negative."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        sentiment = sentiment_request.choices[0].message.content
        return sentiment.strip()
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return "Neutral"
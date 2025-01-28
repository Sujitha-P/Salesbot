import logging
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL


client = Groq(api_key=GROQ_API_KEY)

def analyze_engagement(user_input):
    try:
        engagement_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Assess the level of buyer engagement based on the following text related to consumer electronics. Provide only with one of the following levels in one liner: Low or Moderate or High."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        engagement = engagement_request.choices[0].message.content
        return engagement.strip()
    except Exception as e:
        logging.error(f"Error analyzing engagement: {e}")
        return "Moderate"
import logging
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

def analyze_emotion(user_input):
    try:
        emotion_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Analyze the emotional state based on the following text related to consumer electronics. Provide only with one of the following emotions with one liner: Excitement or Frustration or Confusion or Hesitation or Satisfaction or Dissatisfaction or Curiosity or Skepticism."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        emotion = emotion_request.choices[0].message.content
        return emotion.strip()
    except Exception as e:
        logging.error(f"Error analyzing emotion: {e}")
        return "Neutral"
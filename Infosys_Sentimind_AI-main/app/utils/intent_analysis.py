import logging
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

def analyze_purchase_intent(user_input):
    try:
        purchase_intent_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Classify the purchase intent of the following text related to consumer electronics. Provide with only one of the following categories in one liner: Immediate purchase intent or Exploratory purchase intent or Comparative shopping intent or Upgrade/replacement intent or Research-stage intent or Price comparison intent."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        purchase_intent = purchase_intent_request.choices[0].message.content
        return purchase_intent.strip()
    except Exception as e:
        logging.error(f"Error analyzing purchase intent: {e}")
        return "Research-stage intent"

def analyze_behavioral_intent(user_input):
    try:
        behavioral_intent_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Classify the behavioral intent signals of the following text related to consumer electronics. Provide with only one of the following signals in one liner: Website browsing intent or Product page exploration or Content download intent or Pricing page investigation or Cart abandonment signals or Repeated product view intent."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        behavioral_intent = behavioral_intent_request.choices[0].message.content
        return behavioral_intent.strip()
    except Exception as e:
        logging.error(f"Error analyzing behavioral intent: {e}")
        return "Website browsing intent"

def analyze_advanced_intent(user_input):
    try:
        advanced_intent_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Classify the advanced intent detection capabilities based on the following text related to consumer electronics. Provide with only one of the following markers in one liner: High-value lead identification or Sales-qualified lead (SQL) potential or Purchase probability scoring or Customer lifecycle stage intent or Technology stack compatibility intent or Personalization readiness."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        advanced_intent = advanced_intent_request.choices[0].message.content
        return advanced_intent.strip()
    except Exception as e:
        logging.error(f"Error analyzing advanced intent: {e}")
        return "High-value lead identification"

def generate_summary(transcription):
    try:
        summary_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Summarize the following conversation in a concise and professional manner. Highlight key points, decisions, and action items. Limit the summary to 50 words and use bullet points if possible."
            },
            {
                "role": "user",
                "content": transcription,
            }],
            model=LLM_MODEL
        )
        summary = summary_request.choices[0].message.content
        return summary.strip()
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return "Unable to generate summary."

def analyze_performance(transcription):
    try:
        performance_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Analyze the following conversation and provide performance metrics. Include sentiment trends, engagement levels, and key discussion points. Limit the summary to 50 words and use bullet points if possible."
            },
            {
                "role": "user",
                "content": transcription,
            }],
            model=LLM_MODEL
        )
        performance_analytics = performance_request.choices[0].message.content
        return performance_analytics.strip()
    except Exception as e:
        logging.error(f"Error analyzing performance: {e}")
        return "Unable to analyze performance."

def update_deal_status(performance_analytics):
    try:
        deal_status_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Based on the following performance analytics, update the deal status. Provide one of the following statuses: Open, Negotiation, Closed-Won, Closed-Lost. Limit the summary to 50 words and use bullet points if possible."
            },
            {
                "role": "user",
                "content": performance_analytics,
            }],
            model=LLM_MODEL
        )
        deal_status = deal_status_request.choices[0].message.content
        return deal_status.strip()
    except Exception as e:
        logging.error(f"Error updating deal status: {e}")
        return "Open"

def generate_follow_up_suggestions(transcription, performance_analytics):
    try:
        follow_up_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Based on the following conversation and performance analytics, generate follow-up suggestions. Include actionable steps and recommendations. Limit the summary to 50 words and use bullet points if possible."
            },
            {
                "role": "user",
                "content": f"Conversation: {transcription}\n\nPerformance Analytics: {performance_analytics}",
            }],
            model=LLM_MODEL
        )
        follow_up_suggestions = follow_up_request.choices[0].message.content
        return follow_up_suggestions.strip()
    except Exception as e:
        logging.error(f"Error generating follow-up suggestions: {e}")
        return "Unable to generate follow-up suggestions."

def provide_negotiation_tactics(user_input):
    try:
        tactics_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Provide negotiation tactics for the consumer electronics sales scenario. Be concise and actionable."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        tactics = tactics_request.choices[0].message.content
        return tactics.strip()
    except Exception as e:
        logging.error(f"Error providing negotiation tactics: {e}")
        return "Unable to provide negotiation tactics."

def handle_objections(user_input):
    try:
        objections_request = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Provide suggestions for handling objections in the consumer electronics sales scenario. Be concise and actionable."
            },
            {
                "role": "user",
                "content": user_input,
            }],
            model=LLM_MODEL
        )
        objections = objections_request.choices[0].message.content
        return objections.strip()
    except Exception as e:
        logging.error(f"Error handling objections: {e}")
        return "Unable to handle objections."
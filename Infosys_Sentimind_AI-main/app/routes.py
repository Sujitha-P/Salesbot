from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.utils.sentiment_analysis import analyze_sentiment
from app.utils.emotion_analysis import analyze_emotion
from app.utils.engagement_analysis import analyze_engagement
from app.utils.intent_analysis import analyze_purchase_intent, analyze_behavioral_intent, analyze_advanced_intent, generate_summary, analyze_performance, update_deal_status, generate_follow_up_suggestions, handle_objections, provide_negotiation_tactics
from app.utils.product_recommendation import recommend_product
from app.utils.crm_utils import check_existing_user, get_last_product, add_feedback
from app.utils.google_sheets import write_to_google_sheets
from datetime import datetime
import logging

router = APIRouter()

# Serve static files (if needed)
router.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint to serve the HTML file
@router.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

# Endpoint to get response
@router.post("/get_response")
async def get_response(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input")
        user_name = data.get("user_name", "You")
        email = data.get("email")

        is_existing_user = check_existing_user(email)
        last_product = get_last_product(email) if is_existing_user else None

        if not user_input:
            return JSONResponse({
                "response": "No input received!",
                "sentiment": "Neutral",
                "emotion": "Neutral",
                "purchase_intent": "Research-stage intent",
                "behavioral_intent": "Website browsing intent",
                "advanced_intent": "High-value lead identification",
                "suggestions": [],
                "is_existing_user": is_existing_user,
                "user_name": user_name,
                "last_product": last_product
            })

        # Step 1: Sentiment analysis
        sentiment_response = analyze_sentiment(user_input)

        # Step 2: Emotional state detection
        emotion_response = analyze_emotion(user_input)

        # Step 3: Buyer engagement analysis
        engagement_response = analyze_engagement(user_input)

        # Step 4: Purchase intent analysis
        purchase_intent_response = analyze_purchase_intent(user_input)

        # Step 5: Behavioral intent signals analysis
        behavioral_intent_response = analyze_behavioral_intent(user_input)

        # Step 6: Advanced intent detection capabilities
        advanced_intent_response = analyze_advanced_intent(user_input)

        # Step 7: Generate suggestions using Groq API and deal.py
        suggestions_response = recommend_product(user_input, email, user_name)

        return JSONResponse({
            "response": user_input,
            "sentiment": sentiment_response,
            "emotion": emotion_response,
            "engagement": engagement_response,
            "purchase_intent": purchase_intent_response,
            "behavioral_intent": behavioral_intent_response,
            "advanced_intent": advanced_intent_response,
            "suggestions": suggestions_response,
            "is_existing_user": is_existing_user,
            "user_name": user_name,
            "last_product": last_product
        })

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing your request. Please try again later.")

# Endpoint to handle feedback
@router.post("/handle_feedback")
async def handle_feedback(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input")
        email = data.get("email")
        feedback = data.get("feedback")  # 'thumbs_up' or 'thumbs_down'
        user_name = data.get("user_name", "You")

        if not user_input or not email or not feedback:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Add feedback to CRM
        add_feedback(email, user_input, feedback)

        # Regenerate recommendations only for thumbs down
        if feedback == "thumbs_down":
            new_recommendations = recommend_product(user_input, email, user_name=user_name, feedback=feedback)
        else:
            # For thumbs up, keep the current recommendations
            new_recommendations = recommend_product(user_input, email, user_name=user_name)

        return JSONResponse({"new_recommendations": new_recommendations})

    except Exception as e:
        logging.error(f"Error handling feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to process feedback")

# Endpoint for post-call insights
@router.post("/post_call_insights")
async def post_call_insights(request: Request):
    try:
        data = await request.json()
        transcription = data.get("transcription")
        user_name = data.get("user_name", "Unknown")
        email = data.get("email", "unknown@example.com")

        if not transcription:
            raise HTTPException(status_code=400, detail="No transcription provided")

        # Step 1: Generate a summary of the call
        summary = generate_summary(transcription)

        # Step 2: Analyze performance (e.g., sentiment trends, engagement)
        performance_analytics = analyze_performance(transcription)

        # Step 3: Update deal status (e.g., based on purchase intent)
        deal_status = update_deal_status(performance_analytics)

        # Step 4: Generate follow-up suggestions
        follow_up_suggestions = generate_follow_up_suggestions(transcription, performance_analytics)

        # Step 5: Provide negotiation coaching
        negotiation_tactics = provide_negotiation_tactics(transcription)
        objection_handling = handle_objections(transcription)

        # Step 6: Retrieve sentiment, emotion, and intent analysis
        sentiment = analyze_sentiment(transcription)
        emotion = analyze_emotion(transcription)
        purchase_intent = analyze_purchase_intent(transcription)
        behavioral_intent = analyze_behavioral_intent(transcription)
        advanced_intent = analyze_advanced_intent(transcription)

        # Step 7: Generate product recommendations
        recommendations = recommend_product(transcription, email, user_name)

        # Prepare data for Google Sheets
        insights_data = {
            "user_name": user_name,
            "email": email,
            "sentiment": sentiment,
            "emotion": emotion,
            "purchase_intent": purchase_intent,
            "behavioral_intent": behavioral_intent,
            "advanced_intent": advanced_intent,
            "recommendations": recommendations,
            "summary": summary,
            "performance_analytics": performance_analytics,
            "deal_status": deal_status,
            "follow_up_suggestions": follow_up_suggestions,
            "negotiation_tactics": negotiation_tactics,
            "objection_handling": objection_handling
        }

        # Automatically write to Google Sheets
        write_to_google_sheets(insights_data)

        return JSONResponse(insights_data)

    except Exception as e:
        logging.error(f"Error generating post-call insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate post-call insights")

# Endpoint for negotiation coaching
@router.post("/negotiation_coach")
async def negotiation_coach(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input")

        if not user_input:
            raise HTTPException(status_code=400, detail="No input provided")

        # Step 1: Provide negotiation tactics
        negotiation_tactics = provide_negotiation_tactics(user_input)

        # Step 2: Handle objections
        objection_handling = handle_objections(user_input)

        return JSONResponse({
            "negotiation_tactics": negotiation_tactics,
            "objection_handling": objection_handling
        })

    except Exception as e:
        logging.error(f"Error providing negotiation coaching: {e}")
        raise HTTPException(status_code=500, detail="Failed to provide negotiation coaching")
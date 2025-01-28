from pydantic import BaseModel, EmailStr
from typing import Optional, List

class InsightsRequest(BaseModel):
    """
    Schema for the request to generate insights.
    """
    transcription: str
    email: Optional[EmailStr] = "unknown@example.com"
    user_name: Optional[str] = "Unknown"

class InsightsResponse(BaseModel):
    """
    Schema for the response from insights analysis.
    """
    user_name: str
    email: str
    sentiment: str
    emotion: str
    purchase_intent: str
    behavioral_intent: str
    advanced_intent: str
    recommendations: List[str]
    summary: Optional[str]
    performance_analytics: Optional[str]
    deal_status: Optional[str]
    follow_up_suggestions: Optional[str]

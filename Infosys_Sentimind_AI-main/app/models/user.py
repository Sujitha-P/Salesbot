from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """
    Base user model to represent common user fields.
    """
    email: EmailStr
    name: Optional[str] = "Unknown"

class UserFeedback(UserBase):
    """
    Schema for user feedback.
    """
    feedback: str  # 'thumbs_up' or 'thumbs_down'
    user_input: str

class UserRequest(UserBase):
    """
    Schema for user requests, such as chat input.
    """
    user_input: str

class ExistingUser(UserBase):
    """
    Schema for existing user data.
    """
    last_product: Optional[str] = None
    is_existing_user: bool = False

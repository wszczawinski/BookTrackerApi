from pydantic import BaseModel
from datetime import datetime

from .user_responses import UserPublic


class LoginResponse(BaseModel):
    message: str
    user: UserPublic
    expires_at: datetime


class RefreshResponse(BaseModel):
    message: str
    expires_at: datetime


class LogoutResponse(BaseModel):
    message: str

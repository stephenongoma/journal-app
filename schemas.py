from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


# Must match MoodEnum in models.py exactly
class MoodEnum(str, Enum):
    happy = "happy"
    sad = "sad"
    neutral = "neutral"
    angry = "angry"
    anxious = "anxious"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# Token is what the /auth/login endpoint returns to the client
class Token(BaseModel):
    access_token: str   # the JWT string e.g. "eyJhbGci..."
    token_type: str     # always "bearer" — tells client how to send it back


class EntryCreate(BaseModel):
    title: str
    content: str
    mood: Optional[MoodEnum] = None   # optional — user can set mood or leave it blank


class EntryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    mood: Optional[MoodEnum] = None   # optional — only update mood if sent


class EntryResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    mood: Optional[MoodEnum] = None   # included in response, may be null

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class EntryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class EntryResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True
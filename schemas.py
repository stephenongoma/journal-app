from pydantic import BaseModel, EmailStr

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
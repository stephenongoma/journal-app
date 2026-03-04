import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

# Load environment variables from .env file
load_dotenv()

# --- JWT CONFIG ---
# SECRET_KEY is used to SIGN tokens — anyone with this key can forge tokens
# so keep it in .env and never commit it to GitHub!

#Reads SECRET_KEY from .env — never hardcoded in code again
SECRET_KEY = os.getenv("SECRET_KEY")

# ALGORITHM tells jose HOW to sign — HS256 (HMAC + SHA256) is the industry standard
ALGORITHM = "HS256"

# How long before the token expires and the user must log in again
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# oauth2_scheme does TWO things:
# 1. Tells FastAPI's docs UI to show the 🔒 Authorize button
# 2. Automatically extracts the token from the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict) -> str:
        # Copy so we don't mutate the original dict passed in
    to_encode = data.copy()

       # Set expiry time — datetime.utcnow() + timedelta gives us a future timestamp
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

       # "exp" is a standard JWT claim — jose will automatically reject expired tokens
    to_encode.update({"exp": expire})

     # jwt.encode() signs the payload with our SECRET_KEY and returns a string token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    # Depends(oauth2_scheme) extracts the Bearer token from the request header for us
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Pre-build the exception we'll raise if ANYTHING goes wrong
    # We use the same error for all failures — don't tell attackers WHY it failed
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        # This header tells the client "you need to authenticate with Bearer token"
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # jwt.decode() does THREE things automatically:
        # 1. Verifies the signature (was it signed with OUR secret key?)
        # 2. Checks the token hasn't expired ("exp" claim)
        # 3. Returns the payload dict if everything is valid
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # "sub" (subject) is the standard JWT claim for "who this token belongs to"
        # We stored the user's id here during login
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        # JWTError covers: bad signature, expired token, malformed token
        raise credentials_exception

    # Token is valid — now fetch the actual user from DB to get fresh data
    # (e.g. if user was deleted after token was issued, this catches it)
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user  # This gets injected into any route that uses Depends(get_current_user)

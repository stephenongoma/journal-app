from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from passlib.context import CryptContext
from auth import create_access_token, get_current_user

# Creates all tables in PostgreSQL if they don't exist yet
# Reads from models.py to know what tables/columns to create
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CryptContext manages password hashing
# bcrypt is the recommended algorithm — it's slow BY DESIGN to resist brute-force attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
def read_root():
    return {"message": "Journal App API is running!"}


@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email BEFORE trying to insert
    # Without this, PostgreSQL would throw a ugly IntegrityError (unique constraint)
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # NEVER store plain-text passwords — always hash them
    # pwd_context.hash() adds a random "salt" so two identical passwords hash differently
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password  # storing the hash, not the raw password
    )

    db.add(new_user)      # stages the INSERT
    db.commit()           # executes it against PostgreSQL
    db.refresh(new_user)  # re-fetches from DB so new_user.id is populated
    return new_user


@app.post("/auth/login", response_model=schemas.Token)
def login(
    # OAuth2PasswordRequestForm expects form fields: "username" and "password"
    # It's an OAuth2 spec convention — we use email AS the username field
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Look up user by email (form_data.username holds the email we sent)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    # pwd_context.verify() hashes the plain password and compares to the stored hash
    # "not user" catches wrong email, "not verify" catches wrong password
    # We return the SAME error for both — don't reveal which one was wrong
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Store user.id as "sub" (subject) inside the token payload
    # str() because JWT claims must be strings
    token = create_access_token(data={"sub": str(user.id)})

    # Return the token — client stores this and sends it with every future request
    return {"access_token": token, "token_type": "bearer"}


# Depends(get_current_user) protects this route:
# FastAPI will call get_current_user(), validate the token,
# and inject the User object — or raise 401 if token is missing/invalid
@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    # current_user is already fetched and validated — just return it
    return current_user

@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check duplicate email
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # ✅ ADD THIS — checks username before PostgreSQL throws an IntegrityError
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password before storing — never store plain text!
    hashed_password = pwd_context.hash(user.password)
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
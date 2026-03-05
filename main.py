from models import Entry
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from passlib.context import CryptContext
from auth import create_access_token, get_current_user

# Create all tables in PostgreSQL if they don't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# bcrypt is used to hash passwords — slow by design to resist brute-force attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")
def read_root():
    return {"message": "Journal App API is running!"}


# Register a new user
@app.post("/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Block duplicate emails
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    # Block duplicate usernames
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password before saving — never store plain text
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


# Login and get a JWT token
@app.post("/auth/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # expects email + password form fields
    db: Session = Depends(get_db)
):
    # Look up user by email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    # Return the same error for wrong email OR wrong password — don't reveal which one
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create a JWT token with the user's id stored inside it
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# Get the currently logged-in user (protected route)
@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    # get_current_user validates the token and returns the user
    return current_user


# --- Journal Entry CRUD Endpoints ---
# All routes below require a valid JWT token


# Create a new journal entry
@app.post("/entries", response_model=schemas.EntryResponse, status_code=201)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Link the entry to the logged-in user via owner_id
    new_entry = Entry(**entry.dict(), owner_id=current_user.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


# Get all entries belonging to the logged-in user
@app.get("/entries", response_model=list[schemas.EntryResponse])
def get_entries(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Filter by owner_id so users only see their own entries
    return db.query(Entry).filter(Entry.owner_id == current_user.id).all()


# Get a single entry by ID (only if it belongs to the logged-in user)
@app.get("/entries/{entry_id}", response_model=schemas.EntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


# Update an existing entry (only if it belongs to the logged-in user)
@app.put("/entries/{entry_id}", response_model=schemas.EntryResponse)
def update_entry(entry_id: int, updates: schemas.EntryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    # Only update fields that were actually sent — ignore missing ones
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


# Delete an entry (only if it belongs to the logged-in user)
@app.delete("/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    entry = db.query(Entry).filter(Entry.id == entry_id, Entry.owner_id == current_user.id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
# Journal App — Session Summary
## About This Project
- **Student:** Stephen Ongoma, CS student at Dedan Kimathi University
- **Goal:** Build a personal diary/journal phone app backend while learning Python
- **GitHub:** https://github.com/stephenongoma/journal-app

---

## Environment Setup
- ✅ Python 3.14
- ✅ PostgreSQL (added to PATH via User Environment Variables)
- ✅ VS Code + Python extension
- ✅ Git (connected to GitHub)
- ✅ Virtual environment: `venv\Scripts\activate`
- ✅ Packages installed: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`, `passlib[bcrypt]`, `python-jose[cryptography]`, `python-multipart`

---

## Project Structure
```
C:\Users\Buda_Boss\OneDrive\Desktop\journal-app\
├── main.py          # FastAPI routes and app entry point
├── auth.py          # JWT token logic and get_current_user dependency
├── models.py        # SQLAlchemy database models (table definitions)
├── schemas.py       # Pydantic schemas (request/response shapes)
├── database.py      # PostgreSQL connection and get_db dependency
├── .env             # Secret keys and DB URL — NEVER commit to GitHub
├── .env.example     # Safe version to commit — shows what vars are needed
├── .gitignore       # Ignores venv/, .env, __pycache__
└── venv/            # Virtual environment (not on GitHub)
```

---

## Database
- **PostgreSQL** running locally on `localhost:5432`
- **Database name:** `journal_db`
- **Tables created:** `users`, `entries` (auto-created by SQLAlchemy on startup)

---

## Every Session — Start With These Commands
```bash
cd C:\Users\Buda_Boss\OneDrive\Desktop\journal-app
venv\Scripts\activate
uvicorn main:app --reload
```
Then open: http://127.0.0.1:8000/docs

## Every Session — End With These Commands
```bash
git add .
git commit -m "describe what you built"
git push
```

---

## Sessions Completed

### ✅ Session 1 — FastAPI Basics
- Installed Python, PostgreSQL, VS Code, Git
- Created virtual environment
- Built first FastAPI server with 2 endpoints:
  - `GET /` — welcome message
  - `GET /hello/{name}` — personalized hello

### ✅ Session 2 — PostgreSQL + User Registration
- Created `.env` file for secrets
- Connected FastAPI to PostgreSQL using SQLAlchemy
- Created `users` table via SQLAlchemy models
- Built `POST /auth/register` endpoint
- Learned: SQLAlchemy models, Pydantic schemas, dependency injection with `Depends(get_db)`

### ✅ Session 3 — JWT Authentication
- Installed `python-jose`, `python-multipart`
- Created `auth.py` with JWT token creation and verification
- Built `POST /auth/login` endpoint — returns JWT token
- Built `GET /users/me` protected route using `Depends(get_current_user)`
- Fixed `.env` security leak — removed from GitHub, rotated SECRET_KEY
- Learned: JWT structure, OAuth2PasswordBearer, password hashing with bcrypt,
  dependency injection for auth, HTTP status codes, reading secrets with `os.getenv()`

### ✅ Session 4 — Journal Entries CRUD
- Fixed `.env` still being tracked by Git — ran `git rm --cached .env`
- Added `Entry` model to `models.py` with a foreign key linking to `users`
- Added entry schemas to `schemas.py` — `EntryCreate`, `EntryUpdate`, `EntryResponse`
- Built all 5 journal entry endpoints (all JWT protected):
  - `POST /entries` — create an entry
  - `GET /entries` — get YOUR entries only
  - `GET /entries/{id}` — get one entry
  - `PUT /entries/{id}` — update an entry
  - `DELETE /entries/{id}` — delete an entry
- Tested all endpoints successfully in `/docs`
- Learned: foreign keys, ownership checks, path parameters, `exclude_unset=True`, 204 status code

---

## Working Endpoints
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/` | No | Health check |
| POST | `/auth/register` | No | Create new user |
| POST | `/auth/login` | No | Login, returns JWT token |
| GET | `/users/me` | ✅ Yes | Get current logged-in user |
| POST | `/entries` | ✅ Yes | Create a new journal entry |
| GET | `/entries` | ✅ Yes | Get all your entries |
| GET | `/entries/{id}` | ✅ Yes | Get one entry by ID |
| PUT | `/entries/{id}` | ✅ Yes | Update an entry |
| DELETE | `/entries/{id}` | ✅ Yes | Delete an entry |

---

## Key Concepts Learned So Far
| Concept | Summary |
|---|---|
| FastAPI routing | `@app.get()`, `@app.post()` decorators define endpoints |
| Pydantic schemas | Validate request input and shape response output |
| SQLAlchemy models | Python classes that map to PostgreSQL tables |
| `Depends()` | FastAPI dependency injection — reusable logic across routes |
| Password hashing | bcrypt via passlib — never store plain text passwords |
| JWT tokens | `HEADER.PAYLOAD.SIGNATURE` — signed but not encrypted |
| `"sub"` claim | Standard JWT field for storing user identity (user id) |
| `response_model` | Controls what fields are returned — hides password hash |
| `.env` security | Secrets live in `.env` only — never commit to GitHub |
| HTTP status codes | 200 success, 201 created, 204 deleted, 400 bad request, 401 unauthorized, 404 not found |
| Foreign keys | `owner_id` links every entry to the user who created it |
| Ownership checks | `filter(Entry.owner_id == current_user.id)` — users only see their own data |
| Path parameters | `/entries/{entry_id}` — the ID comes from the URL |
| `exclude_unset=True` | Only updates fields the user actually sent — ignores missing ones |

---

## Session 5 — What To Build Next
1. Add **pagination** to `GET /entries` — limit how many entries are returned at once
2. Add **search** — filter entries by keyword in title or content
3. Add **mood tracking** — add a `mood` field to entries (happy, sad, neutral, etc.)
4. Add **tags** — label entries for easy filtering
5. Learn: query parameters, optional filters, Enum types in SQLAlchemy

---

## App Features Planned
- Personal diary / daily entries
- Mood tracking
- Search & tags
- Photos / media
- Reminders & streaks
- Password / biometric lock

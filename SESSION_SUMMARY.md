# Journal App — Session 1 Summary

## About This Project
- **Student:** Stephen Ongoma, CS student at Dedan Kimathi University
- **Goal:** Build a personal diary/journal phone app backend while learning Python
- **GitHub:** https://github.com/stephenongoma/journal-app

---

## What We Built
A working FastAPI backend server with 2 endpoints:
- `GET /` — returns a welcome message
- `GET /hello/{name}` — returns a personalized hello message

---

## What's Installed on Your PC
- ✅ Python 3.14
- ✅ PostgreSQL (added to PATH via User Environment Variables)
- ✅ VS Code + Python extension
- ✅ Git (connected to GitHub)
- ✅ Packages inside venv: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`

---

## Project Location
```
C:\Users\Buda_Boss\OneDrive\Desktop\journal-app\
├── main.py          # your FastAPI server
├── .gitignore       # ignores venv, .env, __pycache__
└── venv/            # virtual environment (not on GitHub)
```

---

## Every Session — Start With These Commands
```bash
venv\Scripts\activate
uvicorn main:app --reload
```

## Every Session — End With These Commands
```bash
git add .
git commit -m "describe what you built"
git push
```

---

## Next Session — What To Build
1. Create a `.env` file to store PostgreSQL password securely
2. Connect FastAPI to PostgreSQL using SQLAlchemy
3. Create the `users` table in the database
4. Build the **user registration endpoint** — `POST /auth/register`
5. Learn Python concepts: classes, decorators, functions in more depth

---

## App Features Planned
- Personal diary / daily entries
- Mood tracking
- Search & tags
- Photos / media
- Reminders & streaks
- Password / biometric lock

## Full Backend Architecture
Refer to `journal-app-backend.md` for the full database schema and API design.

---

## To Resume With Claude
Paste this into a new chat:
> "I'm a CS student at Dedan Kimathi University building a journal app in Python/FastAPI.
> I have PostgreSQL installed, my FastAPI server is running, and my code is on GitHub at
> https://github.com/stephenongoma/journal-app. We completed Session 1 and need to connect
> to PostgreSQL and build user registration next. Please refer to SESSION_SUMMARY.md in my project."

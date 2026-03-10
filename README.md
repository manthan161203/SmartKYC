# Smart KYC

Local-first KYC application with FastAPI (backend), React/Vite (frontend), SQLite (database), and filesystem-based uploads.

## Overview

This repository is configured to run fully local:
- No Supabase required for document/profile storage
- SQLite database (`smart_kyc.db`)
- Uploaded files stored under `uploaded_files/`
- Backend serves uploaded files via `/uploads/*`

## Project Structure

```text
Smart_KYC/
├── backend/                 # FastAPI app, services, models, utils
├── frontend/                # React + Vite app
├── migrations/              # Alembic migrations
├── uploaded_files/          # Local document/profile uploads
├── main.py                  # FastAPI entrypoint
├── requirements.txt         # Python dependencies
└── .env                     # Local environment configuration
```

## Requirements

- Python 3.10+
- Node.js 18+
- npm
- Linux/macOS/WSL recommended (OCR/ML libs are heavier)

## Environment (`.env`)

Use local DB + local storage values.

```env
# Database
DB_ENGINE=sqlite
SQLITE_PATH=smart_kyc.db

# Mail (for OTP/reset email)
SENDER_MAIL=your_email@example.com
PASSKEY_MAIL=your_app_password
SMTP_PORT=587
SMTP_SERVER=smtp.gmail.com

# Redis (OTP cache)
REDIS_HOST=localhost
REDIS_PORT=6379
OTP_EXPIRY_TIME=600

# JWT
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=10080

# LLM extraction (optional but used in extraction flow)
GEMINI_KEY=

# Not used in local mode
SUPABASE_URL=
SUPABASE_KEY=
```

## Backend Setup

```bash
# from repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run backend on a unique port:

```bash
./.venv/bin/python -m uvicorn main:app --reload --host 127.0.0.1 --port 8010
```

## Frontend Setup

```bash
cd frontend
npm install
```

Run frontend and point it to backend port `8010`:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8010 npm run dev -- --host 127.0.0.1 --port 5174
```

Open: `http://127.0.0.1:5174`

## Core URLs

- API root: `http://127.0.0.1:8010/`
- Health: `http://127.0.0.1:8010/health`
- Uploaded files: `http://127.0.0.1:8010/uploads/<relative_path>`

Example:
- Disk path: `uploaded_files/1/profile_photo.jpg`
- URL: `http://127.0.0.1:8010/uploads/1/profile_photo.jpg`

## API Groups

- `/auth/*` register, login, OTP, forgot/reset/change password
- `/user/*` profile and profile photo management
- `/document_store_and_process/*` upload + OCR + extraction pipeline
- `/extract_details/*` retrieve extracted document fields
- `/verify_document/*` mark document verification
- `/verify_kyc/*` face verification and KYC status update

## Common Issues

### 1) `Address already in use`
Use different ports or kill old process:

```bash
lsof -ti :8010 | xargs -r kill -9
lsof -ti :5174 | xargs -r kill -9
```

### 2) Registration failed
Most common causes:
- Frontend using wrong backend URL (set `VITE_API_BASE_URL` correctly)
- Email/phone already exists

### 3) OTP not working
Check:
- Redis is running
- SMTP credentials are valid

### 4) Extraction failing
Check:
- `GEMINI_KEY` is set
- OCR dependencies installed correctly

## Local Data Notes

- `smart_kyc.db` stores all app data.
- `uploaded_files/` stores KYC docs and profile images.
- Deleting these resets local state.

## Development Commands

```bash
# Backend health
curl http://127.0.0.1:8010/health

# Frontend production build
cd frontend && npm run build
```

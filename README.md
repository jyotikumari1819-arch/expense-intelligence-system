# Expense Intelligence System

A full-stack expense tracker with AI-powered categorization and spending insights, built with FastAPI, MongoDB, and React.

## Overview

Expense Intelligence System lets users log their spending and get more than just a list of numbers back — it automatically categorizes each expense using Google's Gemini API and generates a short, plain-English monthly summary of spending habits. Authentication (signup, login, password reset) is built from scratch rather than relying on a third-party auth provider, using bcrypt password hashing and JWTs.

## Features

- 🔐 **Custom JWT authentication** — signup, login, and a full forgot/reset password flow
- 💰 **Expense CRUD** — add, view, and delete expenses, scoped per user
- 🤖 **AI auto-categorization** — leave the category blank and Gemini classifies the expense from its description (falls back to keyword matching if no API key is configured, so the app always works)
- 📊 **Monthly dashboard** — spending breakdown by category (pie chart) plus an AI-generated natural-language summary of the month
- 🎨 **Deliberate, non-generic UI** — a ledger/receipt-inspired design system (serif headings, monospace numerals, hairline rules) instead of default "SaaS card" styling

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python), Motor (async MongoDB driver) |
| Database | MongoDB |
| Auth | bcrypt password hashing, JWT (python-jose) |
| AI | Google Gemini API |
| Frontend | React + Vite |
| Charting | Recharts |
| Routing | react-router-dom |

## Project Structure

```
expense-intelligence-system/
├── backend/
│   ├── main.py              # FastAPI app entrypoint, CORS, router registration
│   ├── config.py            # Environment-driven settings
│   ├── database.py          # MongoDB (Motor) connection + indexes
│   ├── models.py            # Pydantic request/response schemas
│   ├── auth_utils.py        # Password hashing, JWT issue/verify, route protection
│   ├── email_service.py     # Password-reset email (SMTP, with console fallback)
│   ├── ai_service.py        # Gemini calls for categorization + insights, with fallback
│   ├── requirements.txt
│   ├── .env.example
│   └── routers/
│       ├── auth.py           # signup, login, forgot-password, reset-password
│       ├── expenses.py       # CRUD
│       ├── categories.py     # category list
│       └── insights.py       # dashboard summary + AI monthly insight
└── frontend/
    ├── src/
    │   ├── api.js             # fetch wrapper for the backend
    │   ├── App.jsx             # routing
    │   ├── index.css           # design system
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Signup.jsx
    │   │   ├── ForgotPassword.jsx
    │   │   ├── ResetPassword.jsx
    │   │   └── Dashboard.jsx
    │   └── components/
    │       ├── ExpenseForm.jsx
    │       ├── ExpenseList.jsx
    │       ├── SpendingChart.jsx
    │       └── InsightsPanel.jsx
    ├── package.json
    └── vite.config.js
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A MongoDB database (local install or a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) cluster)
- (Optional) A free [Gemini API key](https://aistudio.google.com/apikey) for real AI categorization/insights — without one, the app uses a keyword-based fallback

### Backend setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your own values:

```
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=expense_intelligence
JWT_SECRET_KEY=some_long_random_string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY=your_gemini_key_or_leave_blank

# Optional — for real password-reset emails. Leave blank to print the
# reset link to the console instead (fine for local development).
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

Run the server:

```bash
python -m uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## How Authentication Works

- Passwords are hashed with **bcrypt** before storage — plaintext passwords are never saved.
- On login, a **JWT** is issued containing the user's ID and an expiry claim, and is attached as a Bearer token on every subsequent request.
- A FastAPI **dependency** (`get_current_user`) validates the token on every protected route.
- Forgot/reset password uses a **separate, short-lived, single-purpose JWT** (distinct from the login token) so a leaked reset link can't be reused as general account access. In local development, the reset link is printed to the backend console instead of emailed, unless SMTP settings are provided.

## Known Limitations / Roadmap

- No JWT revocation — a token is valid until it naturally expires (no logout blacklist yet)
- Insights are aggregated in Python rather than via a MongoDB aggregation pipeline — would need optimizing for large expense volumes
- No pagination on the expenses list yet
- No automated tests yet
- Planned: receipt upload + OCR, per-category budgets with alerts, CSV/PDF export

## License

This project is for portfolio/educational purposes.

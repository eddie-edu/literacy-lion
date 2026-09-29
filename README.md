# Novice Teacher Resource Hub

A digital resource hub built for novice and student teachers at Penn State Abington who teach literacy to young English language learners. The hub centralizes vetted instructional resources and includes an authenticated AI chatbot that draws on those resources to help teachers with classroom decision-making. Developed as a CMPSC 487 capstone project in partnership with a Penn State Abington grant initiative and Solis Cohen Elementary School.

**Client:** Teri Dodaro, Assistant Teaching Professor & Clinical Placement Coordinator, Penn State Abington (tlm128@psu.edu)

**Team:** Timothy Karhnak-Glasby, Eddie Heller, Vladislava Melnichuk, Jason Coffer, Jason Baffour, Jooyoung Yoo, Israel Molethu, Sarnel Brgulja

## Overview

The hub is organized into six main pages:

- **Landing page** — introduces the site and how to use it
- **Resource archive** — browsable/searchable library of literacy instruction resources, each with a summary and a link to the original source
- **Chatbot** — gated behind access-code authentication; teachers can ask instructional questions (e.g. how to teach a specific technique to ESL students of a given language) and the AI responds using only resources stored in the hub
- **Terms & Conditions/Privacy Statement** — brief page for the Terms and Conditions and Privacy Statement
- **About us page** — mission statement, the vision behind the site, the founders and our team, etc
- **FAQ page** — Frequently Asked Questions


## Structure

- `backend/` — FastAPI API (Python)
- `frontend/` — React/Next.js client
- `docs/` — architecture notes and meeting notes

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch strategy, commit conventions, and PR review process before opening a pull request.

## Prerequisites

- Python 3.11+
- Node.js 18+
- A `.env` file in `backend/` — see `.env.example` for required variables (database connection string, chatbot access-code secret, and any AI/LLM API keys)

## Backend

**macOS/Linux:**
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Windows:**
```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docs

See [docs/architecture.md](docs/architecture.md) for a high-level overview and [docs/meeting-notes/](docs/meeting-notes/) for notes from project meetings.

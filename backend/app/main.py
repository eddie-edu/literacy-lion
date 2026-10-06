import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from .admin import setup_admin
from app.assistant.config import settings, validate_settings

app = FastAPI(title="AI Resource Hub")
engine = create_engine(os.environ["DATABASE_URL"])
setup_admin(app, engine, os.environ["ADMIN_SESSION_SECRET"])

@app.on_event("startup")
def validate_assistant_config() -> None:
    # Fail fast on missing thresholds at boot, instead of letting the first
    # request that reaches classify_coverage raise the RuntimeError.
    validate_settings(settings)


@app.get("/health")
def health_check():
    return {"status": "ok"}

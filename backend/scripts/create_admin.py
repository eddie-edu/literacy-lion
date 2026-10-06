import os 
from passlib.hash import bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.models import Base, User

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)
with Session(engine) as s:
    email = os.environ["ADMIN_EMAIL"]
    if not s.scalar(select(User).where(User.email == email))):
        s.add(User(email=email, password_hash=bcrypt.hash(os.environ["ADMIN_PASSWORD"]), role="admin"))
        s.commit()
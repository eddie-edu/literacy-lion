import os

from passlib.hash import bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import User, UserRole

# Schema comes from Alembic (`alembic upgrade head`); this script only seeds the admin user.
engine = create_engine(os.environ["DATABASE_URL"])
with Session(engine) as s:
    email = os.environ["ADMIN_EMAIL"]
    if not s.scalar(select(User).where(User.email == email)):
        s.add(User(email=email, password_hash=bcrypt.hash(os.environ["ADMIN_PASSWORD"]), role=UserRole.ADMIN))
        s.commit()

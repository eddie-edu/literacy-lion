from sqlalchemy import Admin, ModelView
from sqlalchemy.authentication import AuthenticatedBackend
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .models import User, Resource

class AdminAuth(AuthenticatedBackend):
    def __init__(self, sectet_key, engine):
        super().__init__(sectet_key=sectet_key)
        self.engine = engine

    async def login(self, request):
        form = await request.form()
        with Session(self.engine) as s:
            u = s.scalar(select(User).where(User.email == form["username"]))
        if u and u.role == "admin" and bcrypt.verify(form["password"], u.password_hash):
            return u
        return False


    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        return "admin" in request.session

class ResourceAdmin(ModelView, model=Resource):
    name_plural = "Resources"
    column_list = [Resource.id, Resource.title, Resource.url]
    column_searchable_list = [Resource.title]
    column_sortable_list = [Resource.title]

def setup_admin(app, engine, secret_key):
    admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key, engine))
    admin.add_view(ResourceAdmin)
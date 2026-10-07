from passlib.hash import bcrypt
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Document, User, UserRole


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key, engine):
        super().__init__(secret_key=secret_key)
        self.engine = engine

    async def login(self, request):
        form = await request.form()
        with Session(self.engine) as s:
            u = s.scalar(select(User).where(User.email == form["username"]))
        if u and u.role == UserRole.ADMIN and bcrypt.verify(form["password"], u.password_hash):
            request.session.update({"admin": str(u.id)})
            return True
        return False

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        return "admin" in request.session


class DocumentAdmin(ModelView, model=Document):
    name_plural = "Documents"
    column_list = [Document.id, Document.title, Document.publisher, Document.url, Document.source_type]
    column_searchable_list = [Document.title]
    column_sortable_list = [Document.title]
    form_columns = [Document.title, Document.summary, Document.publisher, Document.url, Document.source_type]


def setup_admin(app, engine, secret_key):
    admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key, engine))
    admin.add_view(DocumentAdmin)

# database setup and wrapper functions for each table
# they all return plain data (dicts, lists, True/False, None)
# ids can be strings or UUIDs going in, and always come back as strings

import os
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from .models import ChatSession, Chunk, Document, Message, MessageSource, User, UserRole

# same default as sqlalchemy.url in alembic.ini, so the app and the migrations point at the same database unless DATABASE_URL is set
DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/literacy_lion"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

VALID_MESSAGE_ROLES = ["user", "assistant"]


# Helper functions

def _to_uuid(value):
    # turn a string or UUID into a UUID, returns None if it isn't a valid id
    if value is None:
        return None
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except ValueError:
        return None


def _as_utc(date_value):
    # SQLite gives back dates without a timezone, so treat those as UTC
    if date_value is None:
        return None
    if date_value.tzinfo is None:
        return date_value.replace(tzinfo=timezone.utc)
    return date_value


def _date_to_string(date_value):
    if date_value is None:
        return None
    return _as_utc(date_value).isoformat()


def _role_to_string(role):
    # role is stored as a UserRole enum, but we hand back "user" or "admin"
    if isinstance(role, UserRole):
        return role.value
    return role


def _user_to_dict(user):
    # password_hash is left out on purpose
    return {
        "id": str(user.id),
        "email": user.email,
        "role": _role_to_string(user.role),
        "created_at": _date_to_string(user.created_at),
    }


def _chat_session_to_dict(chat_session):
    return {
        "id": str(chat_session.id),
        "user_id": str(chat_session.user_id),
        "title": chat_session.title,
        "created_at": _date_to_string(chat_session.created_at),
        "updated_at": _date_to_string(chat_session.updated_at),
    }


def _message_to_dict(message):
    return {
        "id": str(message.id),
        "session_id": str(message.session_id),
        "role": message.role,
        "content": message.content,
        "coverage": message.coverage,
        "created_at": _date_to_string(message.created_at),
    }


def _document_to_dict(document):
    return {
        "id": str(document.id),
        "title": document.title,
        "publisher": document.publisher,
        "url": document.url,
        "source_type": document.source_type,
        "uploaded_at": _date_to_string(document.uploaded_at),
    }


def _chunk_to_dict(chunk):
    return {
        "id": str(chunk.id),
        "document_id": str(chunk.document_id),
        "text": chunk.text,
        "page_start": chunk.page_start,
        "page_end": chunk.page_end,
        "section": chunk.section,
        "embedding": chunk.embedding,
    }


def _label_number(label):
    # get the number out of a citation label like "S12" so S2 sorts before S10
    digits = ""
    for character in label:
        if character.isdigit():
            digits = digits + character
    if digits == "":
        return 0
    return int(digits)


# Users

def create_user(email, password_hash, role="user"):
    # create a user, the password must already be hashed by the caller
    # returns the new user as a dict, or None if the email is already taken
    user_role = UserRole(role)  # raises ValueError if role isn't "user" or "admin"

    with SessionLocal() as db:
        existing_user = db.scalars(select(User).where(User.email == email)).first()
        if existing_user is not None:
            return None

        new_user = User(email=email, password_hash=password_hash, role=user_role)
        db.add(new_user)
        db.commit()
        return _user_to_dict(new_user)


def get_user_by_id(user_id):
    user_uuid = _to_uuid(user_id)
    if user_uuid is None:
        return None

    with SessionLocal() as db:
        user = db.get(User, user_uuid)
        if user is None:
            return None
        return _user_to_dict(user)


def get_user_by_email(email):
    with SessionLocal() as db:
        user = db.scalars(select(User).where(User.email == email)).first()
        if user is None:
            return None
        return _user_to_dict(user)


def get_user_for_login(email):
    # look up a user for logging in
    # this is the only function that returns password_hash
    # only use it to check a password, and never send its result to the frontend
    with SessionLocal() as db:
        user = db.scalars(select(User).where(User.email == email)).first()
        if user is None:
            return None
        login_info = _user_to_dict(user)
        login_info["password_hash"] = user.password_hash
        return login_info


# Chat sessions

def create_chat_session(user_id, title=None):
    # start a new chat for a user, returns None if the user doesn't exist
    user_uuid = _to_uuid(user_id)
    if user_uuid is None:
        return None

    with SessionLocal() as db:
        user = db.get(User, user_uuid)
        if user is None:
            return None

        new_chat = ChatSession(user_id=user_uuid, title=title)
        db.add(new_chat)
        db.commit()
        return _chat_session_to_dict(new_chat)


def get_chat_session(session_id):
    # get one chat, the result includes user_id so routes can check who owns it
    session_uuid = _to_uuid(session_id)
    if session_uuid is None:
        return None

    with SessionLocal() as db:
        chat_session = db.get(ChatSession, session_uuid)
        if chat_session is None:
            return None
        return _chat_session_to_dict(chat_session)


def list_chat_sessions_for_user(user_id):
    # all of a user's chats, most recently active first
    user_uuid = _to_uuid(user_id)
    if user_uuid is None:
        return []

    with SessionLocal() as db:
        query = (
            select(ChatSession)
            .where(ChatSession.user_id == user_uuid)
            .order_by(ChatSession.updated_at.desc(), ChatSession.created_at.desc())
        )
        chat_sessions = db.scalars(query).all()

        results = []
        for chat_session in chat_sessions:
            results.append(_chat_session_to_dict(chat_session))
        return results


def rename_chat_session(session_id, new_title):
    # change a chat's title, returns True if it worked or False if the chat wasn't found
    session_uuid = _to_uuid(session_id)
    if session_uuid is None:
        return False

    with SessionLocal() as db:
        chat_session = db.get(ChatSession, session_uuid)
        if chat_session is None:
            return False

        chat_session.title = new_title
        db.commit()
        return True


def delete_chat_session(session_id):
    # delete a chat along with its messages and their citations
    session_uuid = _to_uuid(session_id)
    if session_uuid is None:
        return False

    with SessionLocal() as db:
        chat_session = db.get(ChatSession, session_uuid)
        if chat_session is None:
            return False

        # the models cascade the delete down to messages and message_sources
        db.delete(chat_session)
        db.commit()
        return True


# Messages

def add_message(session_id, role, content, coverage=None):
    # save a message to a chat, role must be "user" or "assistant"
    # coverage is optional (the assistant uses "strong", "weak", or "none")
    # returns the saved message as a dict, or None if the chat doesn't exist
    if role not in VALID_MESSAGE_ROLES:
        raise ValueError("role must be 'user' or 'assistant', got: " + str(role))

    session_uuid = _to_uuid(session_id)
    if session_uuid is None:
        return None

    with SessionLocal() as db:
        chat_session = db.get(ChatSession, session_uuid)
        if chat_session is None:
            return None

        # messages are put in order by created_at, so if a user message and the assistant reply get saved at the same instant they could tie
        # make sure each new message is always a little later than the last one
        message_time = datetime.now(timezone.utc)
        last_message_query = (
            select(Message)
            .where(Message.session_id == session_uuid)
            .order_by(Message.created_at.desc())
        )
        last_message = db.scalars(last_message_query).first()
        if last_message is not None:
            last_message_time = _as_utc(last_message.created_at)
            if last_message_time >= message_time:
                message_time = last_message_time + timedelta(microseconds=1)

        new_message = Message(
            session_id=session_uuid,
            role=role,
            content=content,
            coverage=coverage,
            created_at=message_time,
        )
        db.add(new_message)

        # bump the chat so it moves to the top of the user's chat list
        chat_session.updated_at = message_time

        db.commit()
        return _message_to_dict(new_message)


def get_messages(session_id, include_sources=False):
    # all messages in a chat, oldest first
    # if include_sources is True, each message also gets a "sources" list (same format as get_message_sources)
    session_uuid = _to_uuid(session_id)
    if session_uuid is None:
        return []

    with SessionLocal() as db:
        query = (
            select(Message)
            .where(Message.session_id == session_uuid)
            .order_by(Message.created_at)
        )
        messages = db.scalars(query).all()

        results = []
        for message in messages:
            message_dict = _message_to_dict(message)
            if include_sources:
                message_dict["sources"] = get_message_sources(message.id)
            results.append(message_dict)
        return results


def get_chat_history(session_id, max_messages=None):
    # chat history for the AI: a list of {"role": ..., "content": ...}, oldest first
    # if max_messages is given, only the most recent max_messages are returned
    messages = get_messages(session_id)

    if max_messages is not None:
        start_index = len(messages) - max_messages
        if start_index < 0:
            start_index = 0
        messages = messages[start_index:]

    history = []
    for message in messages:
        history.append({"role": message["role"], "content": message["content"]})
    return history


# Message sources (citations)

def add_message_source(message_id, chunk_id, label):
    # record that a message cited a chunk, with a label like "S1"
    # returns None if the message or chunk doesn't exist
    message_uuid = _to_uuid(message_id)
    chunk_uuid = _to_uuid(chunk_id)
    if message_uuid is None or chunk_uuid is None:
        return None

    with SessionLocal() as db:
        message = db.get(Message, message_uuid)
        chunk = db.get(Chunk, chunk_uuid)
        if message is None or chunk is None:
            return None

        new_source = MessageSource(message_id=message_uuid, chunk_id=chunk_uuid, label=label)
        db.add(new_source)
        db.commit()
        return {
            "id": str(new_source.id),
            "message_id": str(new_source.message_id),
            "chunk_id": str(new_source.chunk_id),
            "label": new_source.label,
        }


def get_message_sources(message_id):
    # citations for a message, with the document title/publisher/url and pages, sorted by label number (S1, S2, ... S10)
    message_uuid = _to_uuid(message_id)
    if message_uuid is None:
        return []

    with SessionLocal() as db:
        query = (
            select(MessageSource, Chunk, Document)
            .join(Chunk, MessageSource.chunk_id == Chunk.id)
            .join(Document, Chunk.document_id == Document.id)
            .where(MessageSource.message_id == message_uuid)
        )
        rows = db.execute(query).all()

        results = []
        for row in rows:
            source = row[0]
            chunk = row[1]
            document = row[2]
            results.append({
                "label": source.label,
                "chunk_id": str(chunk.id),
                "document_id": str(document.id),
                "title": document.title,
                "publisher": document.publisher,
                "url": document.url,
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "section": chunk.section,
            })

        return _sort_sources_by_label(results)


def _sort_sources_by_label(sources):
    # insertion sort by label number so S2 comes before S10
    sorted_sources = []
    for source in sources:
        source_number = _label_number(source["label"])
        position = 0
        while position < len(sorted_sources):
            if _label_number(sorted_sources[position]["label"]) > source_number:
                break
            position = position + 1
        sorted_sources.insert(position, source)
    return sorted_sources


# Documents

def add_document(title, source_type, publisher=None, url=None):
    # add a document, source_type is "pdf" or "web"
    with SessionLocal() as db:
        new_document = Document(
            title=title,
            source_type=source_type,
            publisher=publisher,
            url=url,
        )
        db.add(new_document)
        db.commit()
        return _document_to_dict(new_document)


def list_documents():
    # all documents, sorted by title A-Z
    with SessionLocal() as db:
        documents = db.scalars(select(Document).order_by(Document.title)).all()

        results = []
        for document in documents:
            results.append(_document_to_dict(document))
        return results


def get_document(document_id):
    document_uuid = _to_uuid(document_id)
    if document_uuid is None:
        return None

    with SessionLocal() as db:
        document = db.get(Document, document_uuid)
        if document is None:
            return None
        return _document_to_dict(document)


def delete_document(document_id):
    # delete a document and all of its chunks
    # any citations (message_sources) pointing at those chunks get deleted too, because the database won't allow a citation to point at a missing chunk
    # the chat messages themselves are kept
    document_uuid = _to_uuid(document_id)
    if document_uuid is None:
        return False

    with SessionLocal() as db:
        document = db.get(Document, document_uuid)
        if document is None:
            return False

        for chunk in document.chunks:
            for source in chunk.sources:
                db.delete(source)

        # the model cascades the delete down to the document's chunks
        db.delete(document)
        db.commit()
        return True


# Chunks

def add_chunk(document_id, text, page_start=None, page_end=None, section=None, embedding=None):
    # add a chunk of text to a document, returns None if the document doesn't exist
    document_uuid = _to_uuid(document_id)
    if document_uuid is None:
        return None

    with SessionLocal() as db:
        document = db.get(Document, document_uuid)
        if document is None:
            return None

        new_chunk = Chunk(
            document_id=document_uuid,
            text=text,
            page_start=page_start,
            page_end=page_end,
            section=section,
            embedding=embedding,
        )
        db.add(new_chunk)
        db.commit()
        return _chunk_to_dict(new_chunk)


def list_chunks_for_document(document_id):
    # all chunks for a document, sorted by starting page
    document_uuid = _to_uuid(document_id)
    if document_uuid is None:
        return []

    with SessionLocal() as db:
        query = (
            select(Chunk)
            .where(Chunk.document_id == document_uuid)
            .order_by(Chunk.page_start)
        )
        chunks = db.scalars(query).all()

        results = []
        for chunk in chunks:
            results.append(_chunk_to_dict(chunk))
        return results

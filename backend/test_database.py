# tests for the wrapper functions in app/database.py
# run from the backend/ folder with:  python test_database.py
# uses a temporary SQLite file instead of PostgreSQL, and deletes it when done

import os
import shutil
import sys
import tempfile
import traceback

# point the wrappers at a temporary SQLite database
# this has to happen before app.database is imported, because it reads DATABASE_URL on import
temp_folder = tempfile.mkdtemp(prefix="literacy_lion_test_")
temp_db_path = os.path.join(temp_folder, "test.db")
os.environ["DATABASE_URL"] = "sqlite:///" + temp_db_path

from sqlalchemy import event
from app import database
from app.models import Base

def turn_on_foreign_keys(connection, connection_record):
    # SQLite ignores foreign keys unless you turn them on, and PostgreSQL always enforces them, so turn them on to match the real database
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

event.listen(database.engine, "connect", turn_on_foreign_keys)

# normally Alembic creates the tables, but for the tests we can build them straight from the models
Base.metadata.create_all(database.engine)

# Users

def test_create_and_get_user():
    user = database.create_user("teacher1@example.com", "fake-hash-1")
    assert user is not None
    assert user["email"] == "teacher1@example.com"
    assert user["role"] == "user"
    assert "password_hash" not in user

    by_id = database.get_user_by_id(user["id"])
    assert by_id == user
    assert "password_hash" not in by_id

    by_email = database.get_user_by_email("teacher1@example.com")
    assert by_email == user
    assert "password_hash" not in by_email

def test_duplicate_email_returns_none():
    database.create_user("dupe@example.com", "fake-hash")
    second_try = database.create_user("dupe@example.com", "another-hash")
    assert second_try is None

def test_admin_role():
    admin = database.create_user("admin@example.com", "fake-hash", role="admin")
    assert admin["role"] == "admin"

def test_bad_role_raises_error():
    raised_error = False
    try:
        database.create_user("badrole@example.com", "fake-hash", role="superuser")
    except ValueError:
        raised_error = True
    assert raised_error

def test_login_lookup_is_only_one_with_password_hash():
    database.create_user("login@example.com", "secret-hash")
    login_info = database.get_user_for_login("login@example.com")
    assert login_info["password_hash"] == "secret-hash"
    assert login_info["email"] == "login@example.com"

def test_missing_users_return_none():
    assert database.get_user_by_id("not-a-real-id") is None
    assert database.get_user_by_id("00000000-0000-0000-0000-000000000000") is None
    assert database.get_user_by_email("nobody@example.com") is None
    assert database.get_user_for_login("nobody@example.com") is None

# Chat sessions

def test_create_get_rename_chat_session():
    user = database.create_user("chatter@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"], "Phonics ideas")
    assert chat["title"] == "Phonics ideas"
    assert chat["user_id"] == user["id"]

    fetched = database.get_chat_session(chat["id"])
    assert fetched["id"] == chat["id"]

    assert database.rename_chat_session(chat["id"], "Phonics games") is True
    assert database.get_chat_session(chat["id"])["title"] == "Phonics games"

def test_chat_session_for_missing_user():
    assert database.create_chat_session("00000000-0000-0000-0000-000000000000") is None
    assert database.rename_chat_session("00000000-0000-0000-0000-000000000000", "x") is False
    assert database.get_chat_session("garbage") is None

def test_list_chat_sessions_newest_first():
    user = database.create_user("lister@example.com", "fake-hash")
    first_chat = database.create_chat_session(user["id"], "First")
    second_chat = database.create_chat_session(user["id"], "Second")

    chats = database.list_chat_sessions_for_user(user["id"])
    assert len(chats) == 2
    assert chats[0]["id"] == second_chat["id"]
    assert chats[1]["id"] == first_chat["id"]

    # sending a message in the older chat should move it back to the top
    database.add_message(first_chat["id"], "user", "hello again")
    chats = database.list_chat_sessions_for_user(user["id"])
    assert chats[0]["id"] == first_chat["id"]

    # other users' chats should not show up
    other_user = database.create_user("other@example.com", "fake-hash")
    database.create_chat_session(other_user["id"], "Not yours")
    assert len(database.list_chat_sessions_for_user(user["id"])) == 2

def test_delete_chat_session_removes_messages():
    user = database.create_user("deleter@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])
    message = database.add_message(chat["id"], "assistant", "an answer")
    document = database.add_document("Some Doc", "pdf")
    chunk = database.add_chunk(document["id"], "some text", page_start=1, page_end=1)
    database.add_message_source(message["id"], chunk["id"], "S1")

    assert database.delete_chat_session(chat["id"]) is True
    assert database.get_chat_session(chat["id"]) is None
    assert database.get_messages(chat["id"]) == []
    assert database.get_message_sources(message["id"]) == []
    assert database.delete_chat_session(chat["id"]) is False

    # the document and its chunks are not part of the chat so they can stay
    assert database.get_document(document["id"]) is not None
    assert len(database.list_chunks_for_document(document["id"])) == 1

# Messages

def test_add_and_get_messages_in_order():
    user = database.create_user("messager@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])

    # save several right after each other
    database.add_message(chat["id"], "user", "How do I teach blends?")
    database.add_message(chat["id"], "assistant", "Start with picture cards.", coverage="strong")
    database.add_message(chat["id"], "user", "Any games?")
    database.add_message(chat["id"], "assistant", "Try blend bingo.", coverage="weak")

    messages = database.get_messages(chat["id"])
    assert len(messages) == 4
    assert messages[0]["content"] == "How do I teach blends?"
    assert messages[1]["content"] == "Start with picture cards."
    assert messages[1]["coverage"] == "strong"
    assert messages[2]["content"] == "Any games?"
    assert messages[3]["content"] == "Try blend bingo."

def test_chat_history_for_ai():
    user = database.create_user("history@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])
    database.add_message(chat["id"], "user", "one")
    database.add_message(chat["id"], "assistant", "two")
    database.add_message(chat["id"], "user", "three")

    history = database.get_chat_history(chat["id"])
    assert history == [
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
    ]

    last_two = database.get_chat_history(chat["id"], max_messages=2)
    assert last_two == [
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
    ]

    assert database.get_chat_history(chat["id"], max_messages=50) == history

def test_bad_message_role_and_missing_chat():
    user = database.create_user("badmsg@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])

    raised_error = False
    try:
        database.add_message(chat["id"], "system", "not allowed")
    except ValueError:
        raised_error = True
    assert raised_error

    assert database.add_message("00000000-0000-0000-0000-000000000000", "user", "hi") is None
    assert database.get_messages("not-an-id") == []
    assert database.get_chat_history("not-an-id") == []

# Message sources (citations)

def test_message_sources_with_document_info():
    user = database.create_user("citer@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])
    answer = database.add_message(chat["id"], "assistant", "See [S1] and [S2].")

    document = database.add_document(
        "ESL Phonics Guide", "pdf", publisher="State DOE", url="https://example.com/guide.pdf"
    )
    chunk_a = database.add_chunk(document["id"], "text a", page_start=4, page_end=5)
    chunk_b = database.add_chunk(document["id"], "text b", page_start=10, page_end=10, section="Blends")

    # add them out of order (including S10) to check sorting
    database.add_message_source(answer["id"], chunk_b["id"], "S10")
    database.add_message_source(answer["id"], chunk_a["id"], "S2")
    saved = database.add_message_source(answer["id"], chunk_a["id"], "S1")
    assert saved["label"] == "S1"

    sources = database.get_message_sources(answer["id"])
    assert len(sources) == 3
    assert sources[0]["label"] == "S1"
    assert sources[1]["label"] == "S2"
    assert sources[2]["label"] == "S10"
    assert sources[0]["title"] == "ESL Phonics Guide"
    assert sources[0]["publisher"] == "State DOE"
    assert sources[0]["url"] == "https://example.com/guide.pdf"
    assert sources[0]["page_start"] == 4
    assert sources[0]["page_end"] == 5
    assert sources[2]["section"] == "Blends"

    messages = database.get_messages(chat["id"], include_sources=True)
    assert len(messages[0]["sources"]) == 3

def test_message_source_with_missing_ids():
    assert database.add_message_source("bad", "bad", "S1") is None
    assert database.add_message_source(
        "00000000-0000-0000-0000-000000000000", "00000000-0000-0000-0000-000000000000", "S1"
    ) is None
    assert database.get_message_sources("bad") == []

# Documents and chunks

def test_documents_add_list_get():
    zebra = database.add_document("Zebra Reading Plan", "web", url="https://example.com/z")
    apple = database.add_document("Apple Alphabet Book", "pdf")

    fetched = database.get_document(zebra["id"])
    assert fetched["title"] == "Zebra Reading Plan"
    assert fetched["source_type"] == "web"
    assert fetched["url"] == "https://example.com/z"

    titles = []
    for document in database.list_documents():
        titles.append(document["title"])
    assert titles.index("Apple Alphabet Book") < titles.index("Zebra Reading Plan")

    assert database.get_document(apple["id"])["publisher"] is None
    assert database.get_document("bad") is None

def test_chunks_add_and_list():
    document = database.add_document("Chunky Doc", "pdf")
    database.add_chunk(document["id"], "page three", page_start=3, page_end=3)
    database.add_chunk(document["id"], "page one", page_start=1, page_end=2, embedding="[0.1, 0.2]")

    chunks = database.list_chunks_for_document(document["id"])
    assert len(chunks) == 2
    assert chunks[0]["text"] == "page one"
    assert chunks[0]["embedding"] == "[0.1, 0.2]"
    assert chunks[1]["text"] == "page three"

    assert database.add_chunk("00000000-0000-0000-0000-000000000000", "orphan") is None
    assert database.list_chunks_for_document("bad") == []

def test_delete_document_removes_chunks_and_citations():
    user = database.create_user("docdeleter@example.com", "fake-hash")
    chat = database.create_chat_session(user["id"])
    answer = database.add_message(chat["id"], "assistant", "Cited [S1].")
    document = database.add_document("Doomed Doc", "pdf")
    chunk = database.add_chunk(document["id"], "soon gone", page_start=1)
    database.add_message_source(answer["id"], chunk["id"], "S1")

    assert database.delete_document(document["id"]) is True
    assert database.get_document(document["id"]) is None
    assert database.list_chunks_for_document(document["id"]) == []
    assert database.get_message_sources(answer["id"]) == []

    # the chat message itself is kept
    assert len(database.get_messages(chat["id"])) == 1

    assert database.delete_document(document["id"]) is False
    assert database.delete_document("bad") is False

# Runner

ALL_TESTS = [
    test_create_and_get_user,
    test_duplicate_email_returns_none,
    test_admin_role,
    test_bad_role_raises_error,
    test_login_lookup_is_only_one_with_password_hash,
    test_missing_users_return_none,
    test_create_get_rename_chat_session,
    test_chat_session_for_missing_user,
    test_list_chat_sessions_newest_first,
    test_delete_chat_session_removes_messages,
    test_add_and_get_messages_in_order,
    test_chat_history_for_ai,
    test_bad_message_role_and_missing_chat,
    test_message_sources_with_document_info,
    test_message_source_with_missing_ids,
    test_documents_add_list_get,
    test_chunks_add_and_list,
    test_delete_document_removes_chunks_and_citations,
]

def run_all_tests():
    failed_count = 0
    for test in ALL_TESTS:
        try:
            test()
            print("PASS  " + test.__name__)
        except Exception:
            failed_count = failed_count + 1
            print("FAIL  " + test.__name__)
            traceback.print_exc()
    return failed_count

if __name__ == "__main__":
    failed_count = 0
    try:
        failed_count = run_all_tests()
    finally:
        # close all connections first or Windows won't let us delete the file
        database.engine.dispose()
        shutil.rmtree(temp_folder, ignore_errors=True)

    print()
    if failed_count == 0:
        print("All " + str(len(ALL_TESTS)) + " tests passed!")
    else:
        print(str(failed_count) + " of " + str(len(ALL_TESTS)) + " tests failed.")
        sys.exit(1)

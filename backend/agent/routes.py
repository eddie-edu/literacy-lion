# PUT ROUTES HERE, ALREADY CONNECTED
from http.client import HTTPException

from fastapi import APIRouter, HTTPException
from structures import MessageObject, AIMessage
from logic import chat
import traceback

router = APIRouter()

# under the assumption id is a uuid, change if not the case.
@router.get("/sessions/<id>/messages")
async def get_messages(id: str)-> list[AIMessage]:
    return {}
    # TODO implement this route

@router.post("/sessions/<id>/messages")
async def new_messages(id: str, msg: MessageObject) -> MessageObject: #TODO allow uploading of media files in future, need a CDN for that.
    # TODO get history here. recommend to use same function here and for the get route
    history = {}

    save_me = AIMessage(content=msg.content, role="user")
    # save me too

    try:
        response = await chat(msg, history)
    except Exception:
        traceback.print_exc()
        return HTTPException(500, "Error generating response")

    # add response object to DB, assumed messages DB is just a table with:
    # channel_id: UUID
    # message_id: int or UUID
    # role: assistant or user
    # content: str

    # also have a media, feedback, and citations table for future features
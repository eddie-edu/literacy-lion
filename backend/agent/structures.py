from pydantic import BaseModel
from typing import Literal

class AIMessage(BaseModel):
    role: Literal["assistant", "user"] #system is handled via main prompt
    content: str

class MessageObject(BaseModel):
    content: str

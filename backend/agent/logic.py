from .agent import client, config
from pydantic import BaseModel
from typing import Literal

class AIMessage(BaseModel):
    role: Literal["assistant", "user"]
    content: str

#optionally can have current message in history
async def chat(message: str, history: list[AIMessage]) -> AIMessage:
    # extremely basic, change later
    response = await client.chat.completions.create(
        model=config["MODEL"],
        messages=[
            {"role": "system", "content": config["MAIN_PROMPT"]}, #keep this as first message

            *[msg.model_dump() for msg in history], #history, convert + flatten

            {"role": "user", "content": message} #current message
        ],
        temperature=config["TEMPERATURE"],
        max_tokens=config["MAX_TOKENS"],
    )

    return AIMessage(
        role="assistant",
        content=response.choices[0].message.content
    )
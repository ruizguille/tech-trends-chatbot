from uuid import uuid4
from time import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.db import create_chat, chat_exists
from app.assistants.assistant import RAGAssistant

class ChatIn(BaseModel):
    message: str

router = APIRouter()

@router.post('/chats')
async def create_new_chat():
    chat_id = str(uuid4())[:8]
    created = int(time())
    await create_chat(chat_id, created)
    return {'id': chat_id}

@router.post('/chats/{chat_id}')
async def chat(chat_id: str, chat_in: ChatIn):
    if not await chat_exists(chat_id):
        raise HTTPException(status_code=404, detail=f'Chat {chat_id} does not exist')
    assistant = RAGAssistant(chat_id=chat_id)
    sse_stream = assistant.run(message=chat_in.message)
    return EventSourceResponse(sse_stream)
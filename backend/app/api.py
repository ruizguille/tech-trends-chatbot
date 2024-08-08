from uuid import uuid4
from time import time
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from app.db import create_chat
from app.assistant import RAGAssistant
from app.exceptions import NotFoundError

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
    assistant = RAGAssistant(chat_id=chat_id)
    try:
        return await assistant.run(message=chat_in.message) 
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
from openai import pydantic_function_tool
from time import time
from app.openai import chat_stream
from app.db import get_chat_messages
from app.assistants.tools import QueryKnowledgeBaseTool
from app.assistants.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT

class RAGAssistant:
    def __init__(self, chat_id, history_size=4, max_tool_calls=3):
        self.chat_id = chat_id
        self.main_system_message = {'role': 'system', 'content': MAIN_SYSTEM_PROMPT}
        self.rag_system_message = {'role': 'system', 'content': RAG_SYSTEM_PROMPT}
        self.history_size = history_size
        self.max_tool_calls = max_tool_calls
    
    async def run(self, message):
        user_message = {'role': 'user', 'content': message, 'created': int(time())}
        chat_messages = await get_chat_messages(self.chat_id)
        chat_messages.append({'role': 'user', 'content': message})
        return chat_messages
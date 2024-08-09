import asyncio
from openai import pydantic_function_tool
from time import time
from app.openai import chat_stream
from app.db import get_chat_messages, add_chat_messages
from app.assistants.tools import QueryKnowledgeBaseTool
from app.assistants.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT
from app.utils.sse_stream import SSEStream

class RAGAssistant:
    def __init__(self, chat_id, history_size=4, max_tool_calls=3):
        self.chat_id = chat_id
        self.sse_stream = None
        self.main_system_message = {'role': 'system', 'content': MAIN_SYSTEM_PROMPT}
        self.rag_system_message = {'role': 'system', 'content': RAG_SYSTEM_PROMPT}
        self.history_size = history_size
        self.max_tool_calls = max_tool_calls

    async def _run_chat(self, system_message, chat_messages, **kwargs):
         messages = [system_message, *chat_messages]
         async with chat_stream(messages=messages, **kwargs) as stream:
            async for event in stream:
                if event.type == 'content.delta':
                    await self.sse_stream.send(event.delta)
            
            final_completion = await stream.get_final_completion()
            assistant_message = final_completion.choices[0].message
            return assistant_message
    
    async def _run_assistant_session(self, message):
        new_db_messages = [{'role': 'user', 'content': message, 'created': int(time())}]
        chat_messages = await get_chat_messages(self.chat_id)
        chat_messages.append({'role': 'user', 'content': message})
        assistant_message = await self._run_chat(
            system_message=self.main_system_message,
            chat_messages=chat_messages,
            tools=[
                pydantic_function_tool(QueryKnowledgeBaseTool)
            ],
            tool_choice='auto'
        )
        tool_calls = assistant_message.tool_calls

        if tool_calls:
            chat_messages.append(assistant_message)
            for tool_call in tool_calls[:self.max_tool_calls]:
                kb_tool = tool_call.function.parsed_arguments
                kb_result = await kb_tool()
                chat_messages.append(
                    {'role': 'tool', 'tool_call_id': tool_call.id, 'content': kb_result}
                )
            assistant_message = await self._run_chat(
                system_message=self.rag_system_message,
                chat_messages=chat_messages,
            )
        
        new_db_messages.append({
            'role': 'assistant',
            'content': assistant_message.content,
            'tool_calls': [
                {'name': tc.function.name, 'arguments': tc.function.arguments} for tc in tool_calls
            ],
            'created': int(time())
        })
        await add_chat_messages(self.chat_id, new_db_messages)

    async def _run_assistant_handler(self, message):
        try:
            await self._run_assistant_session(message)
        except Exception as e:
            # TODO: Improve error handling (send SSE message to client)
            print(f'Error: {str(e)}')
        finally:
            await self.sse_stream.close()

    def run(self, message):
        self.sse_stream = SSEStream()
        asyncio.create_task(self._run_assistant_handler(message))
        return self.sse_stream

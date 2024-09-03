import asyncio
from openai import pydantic_function_tool
from time import time
from app.openai import chat_stream
from app.db import get_chat_messages, add_chat_messages
from app.assistants.tools import QueryKnowledgeBaseTool
from app.assistants.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT
from app.utils.sse_stream import SSEStream

class RAGAssistant:
    def __init__(self, chat_id, rdb, history_size=4, max_tool_calls=3):
        self.chat_id = chat_id
        self.rdb = rdb
        self.sse_stream = None
        self.main_system_message = {'role': 'system', 'content': MAIN_SYSTEM_PROMPT}
        self.rag_system_message = {'role': 'system', 'content': RAG_SYSTEM_PROMPT}
        self.tools_schema = [pydantic_function_tool(QueryKnowledgeBaseTool)]
        self.history_size = history_size
        self.max_tool_calls = max_tool_calls

    async def _generate_chat_response(self, system_message, chat_messages, **kwargs):
         messages = [system_message, *chat_messages]
         async with chat_stream(messages=messages, **kwargs) as stream:
            async for event in stream:
                if event.type == 'content.delta':
                    await self.sse_stream.send(event.delta)
            
            final_completion = await stream.get_final_completion()
            assistant_message = final_completion.choices[0].message
            return assistant_message
    
    async def _handle_tool_calls(self, tool_calls, chat_messages):
        for tool_call in tool_calls[:self.max_tool_calls]:
            # There is only one tool in our RAGAssistant, the QueryKnowledgeBaseTool
            kb_tool = tool_call.function.parsed_arguments
            kb_result = await kb_tool(self.rdb)
            chat_messages.append(
                {'role': 'tool', 'tool_call_id': tool_call.id, 'content': kb_result}
            )
        return await self._generate_chat_response(
            system_message=self.rag_system_message,
            chat_messages=chat_messages,
        )
    
    async def _run_conversation_step(self, message):
        user_db_message = {'role': 'user', 'content': message, 'created': int(time())}
        chat_messages = await get_chat_messages(self.rdb, self.chat_id, last_n=self.history_size)
        chat_messages.append({'role': 'user', 'content': message})
        assistant_message = await self._generate_chat_response(
            system_message=self.main_system_message,
            chat_messages=chat_messages,
            tools=self.tools_schema
        )
        tool_calls = assistant_message.tool_calls

        if tool_calls:
            chat_messages.append(assistant_message)
            assistant_message = await self._handle_tool_calls(tool_calls, chat_messages)
        
        assistant_db_message = {
            'role': 'assistant',
            'content': assistant_message.content,
            'tool_calls': [
                {'name': tc.function.name, 'arguments': tc.function.arguments} for tc in tool_calls
            ],
            'created': int(time())
        }
        await add_chat_messages(self.rdb, self.chat_id, [user_db_message, assistant_db_message])

    async def _handle_conversation_task(self, message):
        try:
            await self._run_conversation_step(message)
        except Exception as e:
            # TODO: Improve error handling (send SSE message to client)
            print(f'Error: {str(e)}')
        finally:
            await self.sse_stream.close()

    def run(self, message):
        self.sse_stream = SSEStream()
        asyncio.create_task(self._handle_conversation_task(message))
        return self.sse_stream

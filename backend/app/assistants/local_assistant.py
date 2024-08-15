import asyncio
from rich.console import Console
from openai import pydantic_function_tool
from app.db import get_redis
from app.openai import chat_stream
from app.assistants.tools import QueryKnowledgeBaseTool
from app.assistants.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT

class LocalRAGAssistant:
    def __init__(self, rdb, history_size=4, max_tool_calls=3, log_tool_calls=True, log_tool_results=False):
        self.console = Console()
        self.rdb = rdb
        self.chat_history = []
        self.main_system_message = {'role': 'system', 'content': MAIN_SYSTEM_PROMPT}
        self.rag_system_message = {'role': 'system', 'content': RAG_SYSTEM_PROMPT}
        self.history_size = history_size
        self.max_tool_calls = max_tool_calls
        self.log_tool_calls = log_tool_calls
        self.log_tool_results = log_tool_results

    async def _generate_chat_response(self, system_message, chat_messages, **kwargs):
         messages = [system_message, *chat_messages]
         async with chat_stream(messages=messages, **kwargs) as stream:
            async for event in stream:
                if event.type == 'content.delta':
                    self.console.print(event.delta, style='cyan', end = '')
            
            final_completion = await stream.get_final_completion()
            assistant_message = final_completion.choices[0].message
            if assistant_message.content:
                self.console.print('\n')
            return assistant_message

    async def run(self):
        self.console.print('How can I help you?\n', style='cyan')
        while True:
            chat_messages = self.chat_history[-self.history_size:]
            user_input = input()
            self.console.print()
            user_message = {'role': 'user', 'content': user_input}
            chat_messages.append(user_message)
            assistant_message = await self._generate_chat_response(
                system_message=self.main_system_message,
                chat_messages=chat_messages,
                tools=[
                    pydantic_function_tool(QueryKnowledgeBaseTool)
                ],
                tool_choice='auto'
            )

            if assistant_message.tool_calls:
                chat_messages.append(assistant_message)
                for tool_call in assistant_message.tool_calls[:self.max_tool_calls]:
                    if self.log_tool_calls:
                        self.console.print(f'TOOL CALL:\n{tool_call.to_dict()}', style='red', end='\n\n')
                    kb_tool = tool_call.function.parsed_arguments
                    kb_result = await kb_tool(self.rdb)
                    if self.log_tool_results:
                        self.console.print(f'TOOL RESULT:\n{kb_result}', style='magenta', end='\n\n')
                    chat_messages.append(
                        {'role': 'tool', 'tool_call_id': tool_call.id, 'content': kb_result}
                    )
                assistant_message = await self._generate_chat_response(
                    system_message=self.rag_system_message,
                    chat_messages=chat_messages,
                )
            
            self.chat_history.extend([
                user_message,
                {'role': 'assistant', 'content': assistant_message.content}
            ])


async def run_local_assistant():
    async with get_redis() as rdb:
        await LocalRAGAssistant(rdb).run()

def main():
    asyncio.run(run_local_assistant())


if __name__ == '__main__':
    main()

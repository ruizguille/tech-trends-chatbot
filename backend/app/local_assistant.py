import json
import asyncio
from rich.console import Console
from app.openai import chat_stream
from app.tools import QueryKnowledgeBaseTool
from app.prompts import MAIN_SYSTEM_PROMPT, RAG_SYSTEM_PROMPT

class LocalRAGAssistant:
    def __init__(self, history_size=4, max_tool_calls=3):
        self.console = Console()
        self.chat_history = []
        self.main_system_message = {'role': 'system', 'content': MAIN_SYSTEM_PROMPT}
        self.rag_system_message = {'role': 'system', 'content': RAG_SYSTEM_PROMPT}
        self.response_queue = asyncio.Queue()
        self.history_size = history_size
        self.max_tool_calls = max_tool_calls

    async def process_response(self, response_stream):
        content = ''
        tool_calls = []
        async for chunk in response_stream:
            delta = chunk.choices[0].delta
            if delta.tool_calls:
                delta_tc = delta.tool_calls[0]
                if delta_tc.index == len(tool_calls):
                    tool_calls.append({
                        'id': delta_tc.id,
                        'type': delta_tc.type,
                        'function': {
                            'name': delta_tc.function.name,
                            'arguments': delta_tc.function.arguments
                        }
                    })
                elif delta_tc.function.name:
                    tool_calls[-1]['function']['name'] += delta_tc.function.name
                elif delta_tc.function.arguments:
                    tool_calls[-1]['function']['arguments'] += delta_tc.function.arguments
            elif delta.content:
                content += delta.content
                self.console.print(delta.content, style='cyan', end = '')
        if content:
            self.console.print('\n')
        return content, tool_calls

    async def run(self):
        self.console.print('How can I help you?\n', style='cyan')
        while True:
            chat_messages = self.chat_history[-self.history_size:]
            print(chat_messages, '\n\n')
            user_input = input()
            print()
            user_message = {'role': 'user', 'content': user_input}
            chat_messages.append(user_message)
            response_stream = await chat_stream(
                messages=[self.main_system_message, *chat_messages],
                tools=[QueryKnowledgeBaseTool.openai_tool_schema()],
                tool_choice='auto'
            )
            content, tool_calls = await self.process_response(response_stream)

            if tool_calls:
                chat_messages.append(
                    {'role': 'assistant', 'content': content, 'tool_calls': tool_calls}
                )
                for tool_call in tool_calls[:self.max_tool_calls]:
                    self.console.print(f'TOOL CALL:\n{tool_call}', style='red', end='\n\n')
                    kb_tool = QueryKnowledgeBaseTool(**json.loads(tool_call['function']['arguments']))
                    kb_result = await kb_tool()
                    # self.console.print(f'TOOL RESULT:\n{kb_result}', style='magenta', end='\n\n')
                    chat_messages.append(
                        {'role': 'tool', 'tool_call_id': tool_call['id'], 'content': kb_result}
                    )
                
                response_stream = await chat_stream(
                    messages=[self.rag_system_message, *chat_messages]
                )
                content, _ = await self.process_response(response_stream)
            
            self.chat_history.extend([
                user_message,
                {'role': 'assistant', 'content': content}
            ])


def main():
    asyncio.run(LocalRAGAssistant().run())

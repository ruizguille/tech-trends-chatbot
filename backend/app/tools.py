import numpy as np
from pydantic import BaseModel, Field
from app.db import search_vector_db
from app.openai import get_embedding

class QueryKnowledgeBaseTool(BaseModel):
    """
    Query the knowledge base to answer the user questions.
    """
    query_input: str = Field(description='The natural language query input string. The query input should be clear and standalone.')

    @classmethod    
    def openai_tool_schema(self):
        schema = self.model_json_schema()
        parameters = {
            k: v for k, v in schema.items() if k not in ('title', 'description')
        }
        return {
            'type': 'function',
            'function': {
                'name': schema['title'],
                'description': schema['description'],
                'parameters': parameters
            }
        }

    async def __call__(self):
        query_vector = await get_embedding(self.query_input)
        query_vector = np.array(query_vector, dtype=np.float32).tobytes()
        chunks = search_vector_db(query_vector)
        return f"\n\n{'-'*10}\n\n".join(chunk['text'] for chunk in chunks) + f"\n\n{'-'*10}"

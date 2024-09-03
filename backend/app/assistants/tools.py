from pydantic import BaseModel, Field
from app.db import search_vector_db
from app.openai import get_embedding

class QueryKnowledgeBaseTool(BaseModel):
    """Query the knowledge base to answer user questions about new technology trends, their applications and broader impacts."""
    query_input: str = Field(description='The natural language query input string. The query input should be clear and standalone.')

    async def __call__(self, rdb):
        query_vector = await get_embedding(self.query_input)
        chunks = await search_vector_db(rdb, query_vector)
        formatted_sources = [f'SOURCE: {c['doc_name']}\n"""\n{c['text']}\n"""' for c in chunks]
        return f"\n\n---\n\n".join(formatted_sources) + f"\n\n---"

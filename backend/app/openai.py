import tiktoken
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
tokenizer = tiktoken.encoding_for_model(settings.MODEL)

def token_size(text):
    return len(tokenizer.encode(text))

async def embedding(input, model=settings.MODEL):
    res = await client.embeddings.create(input=input, model=model)
    return res.data[0].embedding

async def embeddings(input, model='text-embedding-3-small'):
    res = await client.embeddings.create(input=input, model=model)
    return [d.embedding for d in res.data]


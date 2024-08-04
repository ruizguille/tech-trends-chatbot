import tiktoken
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
tokenizer = tiktoken.encoding_for_model(settings.MODEL)

def token_size(text):
    return len(tokenizer.encode(text))

async def get_embedding(input, model=settings.EMBEDDING_MODEL, dimensions=settings.EMBEDDING_DIMENSIONS):
    res = await client.embeddings.create(input=input, model=model, dimensions=dimensions)
    return res.data[0].embedding

async def get_embeddings(input, model=settings.EMBEDDING_MODEL, dimensions=settings.EMBEDDING_DIMENSIONS):
    res = await client.embeddings.create(input=input, model=model, dimensions=dimensions)
    return [d.embedding for d in res.data]

async def chat(messages, model=settings.MODEL, temperature=0.1, **kwargs):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs
    )
    message = response.choices[0].message
    return message.content, message.tool_calls


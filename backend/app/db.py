import json
from redis.asyncio import Redis
from redis.commands.search.field import TextField, VectorField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.commands.json.path import Path
from app.config import settings

VECTORS_IDX_NAME = 'idx:vectors'
VECTORS_IDX_PREFIX = 'vectors:'
CHAT_IDX_NAME = 'idx:chat'
CHAT_IDX_PREFIX = 'chat:'

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

async def create_vectors_index():
    schema = (
        TextField('text'),
        TextField('doc_name'),
        VectorField('vector',
            'FLAT', {
                'TYPE': 'FLOAT32',
                'DIM': settings.EMBEDDING_DIMENSIONS,
                'DISTANCE_METRIC': 'COSINE',
            }
        ),
    )
    try:
        await r.ft(VECTORS_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=[VECTORS_IDX_PREFIX], index_type=IndexType.HASH)
        )
        print(f'Index {VECTORS_IDX_NAME} created successfully')
    except Exception as e:
        print(f'Error creating index {VECTORS_IDX_NAME}: {e}')

async def add_to_vector_db(chunks):
    async with r.pipeline(transaction=True) as pipe:
        for chunk in chunks:
            pipe.hset(VECTORS_IDX_PREFIX + chunk['chunk_id'], mapping=chunk)
        await pipe.execute()

async def search_vector_db(query_vector, top_k=5):
    query = (
        Query(f'(*)=>[KNN {top_k} @vector $query_vector AS score]')
        .sort_by('score')
        .return_fields('score', 'chunk_id', 'text', 'doc_name')
        .dialect(2)
    )
    res = await r.ft(VECTORS_IDX_NAME).search(query, {'query_vector': query_vector})
    return [{
        'score': 1 - float(r.score),
        'chunk_id': r.chunk_id,
        'text': r.text,
        'doc_name': r.doc_name
    } for r in res.docs]

async def count_vectors():
    q = Query('*').paging(0, 0)
    return (await r.ft(VECTORS_IDX_NAME).search(q)).total

async def delete_db():
    await r.flushdb()

async def create_chat_index():
    try:
        schema = (
            TextField('text', sortable=True),
        )
        await r.ft(CHAT_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=[CHAT_IDX_PREFIX], index_type=IndexType.JSON)
        )
        print(f'Index {CHAT_IDX_NAME} created successfully')
    except Exception as e:
        print(f'Error creating index {CHAT_IDX_NAME}: {e}')

async def create_chat(chat_id, created):
    chat = {'id': chat_id, 'created': created, 'messages': []}
    await r.json().set(CHAT_IDX_PREFIX + chat_id, Path.root_path(), chat)
    return chat

async def add_chat_messages(chat_id, messages):
    await r.json().arrappend(CHAT_IDX_PREFIX + chat_id, '$.messages', *messages)

async def chat_exists(chat_id):
    return await r.exists(CHAT_IDX_PREFIX + chat_id)

async def get_chat_messages(chat_id, last_n=None):
    if last_n is None:
        messages = await r.json().get(CHAT_IDX_PREFIX + chat_id, '$.messages[*]')
    else:
        messages = await r.json().get(CHAT_IDX_PREFIX + chat_id, f'$.messages[-{last_n}:]')
    return [{'role': m['role'], 'content': m['content']} for m in messages]

async def get_chat(chat_id):
    return await r.json().get(chat_id)

async def get_all_chats():
    res = await r.ft('idx:chat').search(Query('*'))
    return [json.loads(doc.json) for doc in res.docs]

async def delete_chats(*chat_ids):
    keys = [CHAT_IDX_PREFIX + chat_id for chat_id in chat_ids]
    return await r.delete(*keys)

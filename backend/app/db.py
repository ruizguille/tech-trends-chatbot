import json
from redis.asyncio import Redis
from redis.commands.search.field import TextField, VectorField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.commands.json.path import Path
from app.config import settings

VECTOR_IDX_NAME = 'idx:vector'
VECTOR_IDX_PREFIX = 'vector:'
CHAT_IDX_NAME = 'idx:chat'
CHAT_IDX_PREFIX = 'chat:'

def get_redis():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# VECTORS
async def create_vector_index(rdb):
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
        await rdb.ft(VECTOR_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=[VECTOR_IDX_PREFIX], index_type=IndexType.HASH)
        )
        print(f"Vector index '{VECTOR_IDX_NAME}' created successfully")
    except Exception as e:
        print(f"Error creating vector index '{VECTOR_IDX_NAME}': {e}")

async def add_chunks_to_vector_db(rdb, chunks):
    async with rdb.pipeline(transaction=True) as pipe:
        for chunk in chunks:
            pipe.hset(VECTOR_IDX_PREFIX + chunk['chunk_id'], mapping=chunk)
        await pipe.execute()

async def search_vector_db(rdb, query_vector, top_k=5):
    query = (
        Query(f'(*)=>[KNN {top_k} @vector $query_vector AS score]')
        .sort_by('score')
        .return_fields('score', 'chunk_id', 'text', 'doc_name')
        .dialect(2)
    )
    res = await rdb.ft(VECTOR_IDX_NAME).search(query, {'query_vector': query_vector})
    return [{
        'score': 1 - float(d.score),
        'chunk_id': d.chunk_id,
        'text': d.text,
        'doc_name': d.doc_name
    } for d in res.docs]

async def get_all_vectors(rdb):
    res = await rdb.ft(VECTOR_IDX_NAME).search(Query('*'))
    return res.docs


# CHATS
async def create_chat_index(rdb):
    try:
        schema = (
            NumericField('$.created', as_name='created', sortable=True),
        )
        await rdb.ft(CHAT_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=[CHAT_IDX_PREFIX], index_type=IndexType.JSON)
        )
        print(f"Chat index '{CHAT_IDX_NAME}' created successfully")
    except Exception as e:
        print(f"Error creating chat index '{CHAT_IDX_NAME}': {e}")

async def create_chat(rdb, chat_id, created):
    chat = {'id': chat_id, 'created': created, 'messages': []}
    await rdb.json().set(CHAT_IDX_PREFIX + chat_id, Path.root_path(), chat)
    return chat

async def add_chat_messages(rdb, chat_id, messages):
    await rdb.json().arrappend(CHAT_IDX_PREFIX + chat_id, '$.messages', *messages)

async def chat_exists(rdb, chat_id):
    return await rdb.exists(CHAT_IDX_PREFIX + chat_id)

async def get_chat_messages(rdb, chat_id, last_n=None):
    if last_n is None:
        messages = await rdb.json().get(CHAT_IDX_PREFIX + chat_id, '$.messages[*]')
    else:
        messages = await rdb.json().get(CHAT_IDX_PREFIX + chat_id, f'$.messages[-{last_n}:]')
    return [{'role': m['role'], 'content': m['content']} for m in messages] if messages else []

async def get_chat(rdb, chat_id):
    return await rdb.json().get(chat_id)

async def get_all_chats(rdb):
    res = await rdb.ft('idx:chat').search(Query('*'))
    return [json.loads(doc.json) for doc in res.docs]

async def delete_chats(rdb, *chat_ids):
    keys = [CHAT_IDX_PREFIX + chat_id for chat_id in chat_ids]
    return await rdb.delete(*keys)


# GENERAL
async def setup_db(rdb):
    # Create the vector index (deleting the existing one if present)
    try:
        await rdb.ft(VECTOR_IDX_NAME).dropindex(delete_documents=True)
        print(f"Deleted vector index '{VECTOR_IDX_NAME}' and all associated documents")
    except Exception as e:
        pass
    finally:
        await create_vector_index(rdb)

    # Make sure that the chat index exists, and create it if it doesn't
    try:
        await rdb.ft(CHAT_IDX_NAME).info()
    except Exception:
        await create_chat_index(rdb)

async def clear_db(rdb):
    for index_name in [VECTOR_IDX_NAME, CHAT_IDX_NAME]:
        try:
            await rdb.ft(index_name).dropindex(delete_documents=True)
            print(f"Deleted index '{index_name}' and all associated documents")
        except Exception as e:
            print(f"Index '{index_name}': {e}")

from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from app.config import settings

VECTORS_IDX_NAME = 'idx:vectors'
VECTORS_IDX_PREFIX = 'vectors:'

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def create_vectors_index(idx_name=VECTORS_IDX_NAME, idx_prefix=VECTORS_IDX_PREFIX):
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
        r.ft(idx_name).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=[idx_prefix], index_type=IndexType.HASH)
        )
        print(f'Index {idx_name} created successfully')
    except Exception as e:
        print(f'Error creating index {idx_name}: {e}')

def add_to_vector_db(chunks, idx_prefix=VECTORS_IDX_PREFIX):
    pipe = r.pipeline()
    for chunk in chunks:
        key = idx_prefix + chunk['chunk_id']
        pipe.hset(key, mapping=chunk)
    pipe.execute()

def search_vector_db(query_vector, top_k=5, idx_name=VECTORS_IDX_NAME):
    query = (
        Query(f'(*)=>[KNN {top_k} @vector $query_vector AS score]')
        .sort_by('score')
        .return_fields('score', 'chunk_id', 'text', 'doc_name')
        .dialect(2)
    )
    res = r.ft(idx_name).search(query, {'query_vector': query_vector}).docs
    return [{
        'score': 1 - float(r.score),
        'chunk_id': r.chunk_id,
        'text': r.text,
        'doc_name': r.doc_name
    } for r in res]

def reset_db():
    r.flushdb()

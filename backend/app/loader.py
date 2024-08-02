import os
from tqdm import tqdm
from pdfminer.high_level import extract_text
from app.splitter import TextSplitter
from app.openai import get_embeddings, token_size
from app.config import settings

DOCS_DIR = 'data/docs'

def load_docs():
    docs = []
    pdf_files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.pdf')]
    for filename in tqdm(pdf_files):
        file_path = os.path.join(DOCS_DIR, filename)
        text = extract_text(file_path)
        docs.append(text)
    print(f'Loaded {len(docs)} PDF documents')

    chunks = []
    text_splitter = TextSplitter(chunk_size=512, chunk_overlap=150)
    print('\nSplitting documents into chunks')
    for i, doc in enumerate(docs):
        doc_chunks = text_splitter.split(doc)
        chunks += doc_chunks
        print(f'Doc {i+1}: {len(doc_chunks)} chunks')
    chunk_sizes = [token_size(c) for c in chunks]
    print(f'Total chunks: {len(chunks)}')
    print(f'Min chunk size: {min(chunk_sizes)} tokens')
    print(f'Max chunk size: {max(chunk_sizes)} tokens')
    print(f'Average chunk size: {round(sum(chunk_sizes)/len(chunks))} tokens')

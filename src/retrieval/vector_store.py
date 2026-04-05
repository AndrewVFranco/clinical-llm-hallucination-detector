import chromadb
from sentence_transformers import SentenceTransformer
from src.core.config import settings
import os

os.environ["HUGGING_FACE_HUB_TOKEN"] = settings.HF_TOKEN
model = SentenceTransformer("pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb")
_collection = None

def _embed_text(text: str) -> list[float]:
    embedding = model.encode(text)
    embedding = embedding.tolist()
    return embedding


def get_collection():
    global _collection
    if _collection is None:
        print(settings.CHROMA_DB_LOCATION)
        client = chromadb.PersistentClient(path=settings.CHROMA_DB_LOCATION)
        _collection = client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)
    return _collection


def add_abstracts(abstracts: list[dict]):
    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for item in abstracts:
        ids.append(item["pmid"])
        embeddings.append(_embed_text(item["abstract"]))
        documents.append(item["abstract"])
        metadatas.append({"pmid": item["pmid"], "title": item["title"]})

    get_collection().add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

def query_abstracts(query: str, n_results: int = 5) -> list[dict]:
    embedding = _embed_text(query)
    results = get_collection().query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results

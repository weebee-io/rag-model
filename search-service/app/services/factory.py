from .bm25 import BM25Retriever
from .dense import DenseRetriever
from .hybrid import HybridRetriever
from ..core.config import settings

def get_retriever(mode: str):
    modes = {
        "bm25": BM25Retriever,
        "dense": DenseRetriever,
        "hybrid": HybridRetriever,
    }
    cls = modes.get(mode.lower())
    return cls() if cls else None

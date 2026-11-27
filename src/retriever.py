from .tokenizer import Tokenizer
from .chunk import Chunk


class Retriever:
    def __init__(self, bm25, chunks: list[Chunk]):
        self._tokenizer = Tokenizer()
        self._bm25 = bm25
        self._chunks = chunks

    def get_relevant_chunks(self, query: str, top_k: int = 5) -> list[Chunk]:
        tokenized_query = self._tokenizer.tokenize(query)
        scores = self._bm25.get_scores(tokenized_query)
        top_scores = sorted(range(len(scores)),
                            key=lambda i: scores[i],
                            reverse=True)[:top_k]
        return [self._chunks[s] for s in top_scores]
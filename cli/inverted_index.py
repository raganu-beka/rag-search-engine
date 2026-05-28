import pickle
from collections import Counter
from pathlib import Path
from typing import Any

from tokenization import tokenize

CACHE_ROOT_DIR = "./cache"
INDEX_CACHE_FILEPATH = "./cache/index.pkl"
DOCMAP_CACHE_FILEPATH = "./cache/docmap.pkl"
TERM_FREQUENCIES_CACHE_FILEPATH = "./cache/term_frequencies.pkl"


class InvertedIndex:

    def __init__(self) -> None:
        self.index: dict[str, set[int]] = dict()
        self.docmap: dict[int, Any] = dict()
        self.term_frequencies: dict[int, Counter] = dict()

    def build(self, movies: list[dict[str, Any]]):
        for movie in movies:
            id = int(movie["id"])
            text = f"{movie["title"]} {movie["description"]}"

            self._add_document(id, text)
            self.docmap[id] = movie

    def save(self):
        Path(CACHE_ROOT_DIR).mkdir(parents=True, exist_ok=True)

        with open(INDEX_CACHE_FILEPATH, "wb") as f:
            pickle.dump(self.index, f)

        with open(DOCMAP_CACHE_FILEPATH, "wb") as f:
            pickle.dump(self.docmap, f)

        with open(TERM_FREQUENCIES_CACHE_FILEPATH, "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def load(self):
        if not Path(INDEX_CACHE_FILEPATH).exists():
            raise Exception(
                f"Index cache file does not exist at: {INDEX_CACHE_FILEPATH}"
            )
        if not Path(DOCMAP_CACHE_FILEPATH).exists():
            raise Exception(
                f"Docmap cache file does not exist at: {DOCMAP_CACHE_FILEPATH}"
            )
        if not Path(TERM_FREQUENCIES_CACHE_FILEPATH).exists():
            raise Exception(
                f"Term frequencies cache file does not exist at: {TERM_FREQUENCIES_CACHE_FILEPATH}"
            )

        with open(INDEX_CACHE_FILEPATH, "rb") as f:
            self.index = pickle.load(f)

        with open(DOCMAP_CACHE_FILEPATH, "rb") as f:
            self.docmap = pickle.load(f)

        with open(TERM_FREQUENCIES_CACHE_FILEPATH, "rb") as f:
            self.term_frequencies = pickle.load(f)

    def get_documents(self, term: str) -> list[int]:
        doc_ids = self.index.get(term.lower()) or []
        return sorted(doc_ids)

    def get_tf(self, doc_id: int, term: str) -> int:
        if doc_id not in self.term_frequencies:
            raise ValueError(f"Document ID ({doc_id}) is not found")

        token = tokenize_term(term)
        return self.term_frequencies[doc_id][token]

    def _add_document(self, doc_id: int, text: str):
        text_tokens = tokenize(text)

        for token in text_tokens:
            self.index.setdefault(token, set()).add(doc_id)

        self.term_frequencies[doc_id] = Counter(text_tokens)


def tokenize_term(term: str) -> str:
    tokens = tokenize(term)
    if len(tokens) != 1:
        raise ValueError(f"Term ({term}) must contain exactly one token")

    return tokens[0]

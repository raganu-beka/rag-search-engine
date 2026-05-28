import pickle
from pathlib import Path
from typing import Any

from tokenization import tokenize

CACHE_ROOT_DIR = "./cache"
INDEX_CACHE_FILEPATH = "./cache/index.pkl"
DOCMAP_CACHE_FILEPATH = "./cache/docmap.pkl"


class InvertedIndex:

    def __init__(self) -> None:
        self.index: dict[str, set[int]] = dict()
        self.docmap: dict[int, Any] = dict()

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

    def load(self):
        if not Path(INDEX_CACHE_FILEPATH).exists():
            raise Exception(
                f"Index cache file does not exist at: {INDEX_CACHE_FILEPATH}"
            )

        if not Path(DOCMAP_CACHE_FILEPATH).exists():
            raise Exception(
                f"Docmap cache file does not exist at: {DOCMAP_CACHE_FILEPATH}"
            )

        with open(INDEX_CACHE_FILEPATH, "rb") as f:
            self.index = pickle.load(f)

        with open(DOCMAP_CACHE_FILEPATH, "rb") as f:
            self.docmap = pickle.load(f)

    def get_documents(self, term: str) -> list[int]:
        doc_ids = self.index.get(term.lower()) or []
        return sorted(doc_ids)

    def _add_document(self, doc_id: int, text: str):
        for token in tokenize(text):
            self.index.setdefault(token, set()).add(doc_id)

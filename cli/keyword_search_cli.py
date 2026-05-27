import argparse
import json
from typing import Any

import search
import tokenization
from inverted_index import InvertedIndex

MOVIES_DATA_FILENAME = "./data/movies.json"


def load_movies_data(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r", encoding="utf-8") as f:
        movies_data = json.load(f)
        return movies_data["movies"]


def search_movies_by_keyword(
    movies: list[dict[str, Any]], query: str, *, max_results: int = 5
) -> list[dict[str, Any]]:

    def tokenize(query: str) -> list[str]:
        return tokenization.tokenize(query)

    def get_movie_title(movie: dict[str, Any]):
        return movie["title"]

    return search.search_by_keyword(
        movies, query, get_movie_title, tokenize, max_results=max_results
    )


def print_movies(movies: list[dict[str, Any]]) -> None:
    for i, movie in enumerate(movies):
        print(f"{i+1}. {movie["title"]}")


def search_movies(keyword: str) -> None:
    movies = load_movies_data(MOVIES_DATA_FILENAME)
    movie_resuls = search_movies_by_keyword(movies, keyword)
    print_movies(movie_resuls)


def print_token_first_doc(index: InvertedIndex, token: str) -> None:
    docs = index.get_documents(token)

    if not docs:
        print(f"No documents for token for token '{token}'")
        return

    print(f"First document for token '{token}' = {docs[0]}")


def build_movies_index() -> None:
    movies = load_movies_data(MOVIES_DATA_FILENAME)
    index = InvertedIndex()

    index.build(movies)
    index.save()

    print_token_first_doc(index, "merida")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build movies index")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            search_movies(args.query)

        case "build":
            build_movies_index()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

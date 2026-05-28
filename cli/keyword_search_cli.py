import argparse
import json
from typing import Any

import search
import tokenization
from inverted_index import InvertedIndex, tokenize_term

MOVIES_DATA_FILENAME = "./data/movies.json"


def load_movies_data(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r", encoding="utf-8") as f:
        movies_data = json.load(f)
        return movies_data["movies"]


def search_movies_with_inverted_index(
    query: str,
    inverted_index: InvertedIndex,
    *,
    max_results: int = 5,
) -> list[dict[str, Any]]:

    def tokenize(query: str) -> list[str]:
        return tokenization.tokenize(query)

    return search.search_with_inverted_index(
        query, tokenize, inverted_index, max_results=max_results
    )


def print_movies(movies: list[dict[str, Any]]) -> None:
    for movie in movies:
        print(f"{movie["id"]}. {movie["title"]}")


def search_movies(query: str) -> None:
    index = InvertedIndex()
    try:
        index.load()
    except Exception as e:
        print(e)
        return

    movie_resuls = search_movies_with_inverted_index(query, index)
    print_movies(movie_resuls)


def build_movies_index() -> None:
    movies = load_movies_data(MOVIES_DATA_FILENAME)
    index = InvertedIndex()

    index.build(movies)
    index.save()


def print_term_frequency(doc_id: int, term: str):
    try:
        term_token = tokenize_term(term)
    except ValueError as e:
        print(e)
        return

    try:
        index = InvertedIndex()
        index.load()
    except Exception as e:
        print(e)
        return

    print(index.get_tf(doc_id, term_token))


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build movies index")

    tf_parser = subparsers.add_parser("tf", help="Get term frequency")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            search_movies(args.query)

        case "build":
            print("Building inverted index...")
            build_movies_index()
            print("Inverted index built")

        case "tf":
            print(f"{args.term} frequency in document {args.doc_id}...")
            print_term_frequency(args.doc_id, args.term)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

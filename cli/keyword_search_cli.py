import argparse
import json
from typing import Any

import search
import tokenization
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()


def _load_stopwords_from_file(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()


STOPWORDS = _load_stopwords_from_file("./data/stopwords.txt")


def load_movies_data(filename: str) -> list[dict[str, Any]]:
    with open(filename, "r", encoding="utf-8") as f:
        movies_data = json.load(f)
        return movies_data["movies"]


def search_movies_by_keyword(
    movies: list[dict[str, Any]], query: str, *, max_results: int = 5
) -> list[dict[str, Any]]:

    def tokenize(query: str) -> list[str]:
        return tokenization.tokenize(query, STOPWORDS)

    def get_movie_title(movie: dict[str, Any]):
        return movie["title"]

    return search.search_by_keyword(movies, query, get_movie_title, tokenize)


def print_movies(movies: list[dict[str, Any]]) -> None:
    for i, movie in enumerate(movies):
        print(f"{i+1}. {movie["title"]}")


def search_movies(keyword: str) -> None:
    MOVIES_DATA_FILENAME = "./data/movies.json"

    movies = load_movies_data(MOVIES_DATA_FILENAME)
    movie_resuls = search_movies_by_keyword(movies, keyword)

    print_movies(movie_resuls)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            search_movies(args.query)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()

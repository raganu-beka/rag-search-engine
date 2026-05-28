from typing import Any, Callable

from inverted_index import InvertedIndex


def search_by_keyword(
    data: list[Any],
    query: str,
    get_searchable_text: Callable[[Any], str],
    tokenizer: Callable[[str], list[str]],
    *,
    max_results: int = 5,
) -> list[Any]:
    query_tokens = tokenizer(query)

    def matches(item):
        searchable_text = get_searchable_text(item)
        item_tokens = tokenizer(searchable_text)
        return any(q in t for t in item_tokens for q in query_tokens)

    results = [item for item in data if matches(item)]
    return results[:max_results]


def search_with_inverted_index(
    query: str,
    tokenizer: Callable[[str], list[str]],
    index: InvertedIndex,
    *,
    max_results: int = 5,
) -> list[Any]:
    results = []
    search_tokens = tokenizer(query)

    for token in search_tokens:
        results.extend(index.get_documents(token))

        if len(results) >= max_results:
            break

    return [index.docmap[doc_id] for doc_id in results[:max_results]]

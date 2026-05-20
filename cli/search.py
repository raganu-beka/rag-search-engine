from typing import Any, Callable


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

def load_stopwords_from_file(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()

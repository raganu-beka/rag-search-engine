import string

from nltk.stem import PorterStemmer

_stemmer = PorterStemmer()


def tokenize(query: str, stopwords: list[str]) -> list[str]:
    normalized = query.lower()

    punctionation_trans_dict = dict()
    for char in string.punctuation:
        punctionation_trans_dict[char] = ""

    punctionation_trans_table = str.maketrans(punctionation_trans_dict)
    normalized = normalized.translate(punctionation_trans_table)

    return [_stemmer.stem(t) for t in normalized.split(" ") if t not in stopwords]


__all__ = ["tokenize"]

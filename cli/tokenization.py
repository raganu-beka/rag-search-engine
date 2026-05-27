import string

from nltk.stem import PorterStemmer
from utils import load_stopwords_from_file

STOPWORDS = load_stopwords_from_file("./data/stopwords.txt")


_stemmer = PorterStemmer()


def tokenize(query: str) -> list[str]:
    normalized = query.lower()

    punctionation_trans_dict = dict()
    for char in string.punctuation:
        punctionation_trans_dict[char] = ""

    punctionation_trans_table = str.maketrans(punctionation_trans_dict)
    normalized = normalized.translate(punctionation_trans_table)

    return [_stemmer.stem(t) for t in normalized.split(" ") if t not in STOPWORDS]


__all__ = ["tokenize"]

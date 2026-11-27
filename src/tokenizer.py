import re
from nltk.stem import PorterStemmer


class Tokenizer:
    def __init__(self):
        self._pattern = re.compile(r"\b\w+\b")
        self._stemmer = PorterStemmer()

    def tokenize(self, text: str) -> list[str]:
        raw_tokens = self._pattern.findall(text.lower())
        return [self._stemmer.stem(t) for t in raw_tokens]

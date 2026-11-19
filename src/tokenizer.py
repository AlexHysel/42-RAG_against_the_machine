import re


class Tokenizer:
    def __init__(self):
        self._pattern = re.compile(r"\b\w+\b")

    def tokenize(self, text: str) -> list[str]:
        return self._pattern.findall(text.lower())
import re
import json
from pydantic import BaseModel, PrivateAttr, FilePath


class DelimiterConfig(BaseModel):
    _delimiters: dict[re.Pattern[str], tuple[str]] = PrivateAttr()

    def __init__(self, delimiters: dict[str, tuple[str]]):
        super().__init__()
        self._delimiters = {re.compile(k): tuple(v) for k, v in delimiters.items()}

    @classmethod
    def from_file(cls, file_path: FilePath) -> DelimiterConfig:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return DelimiterConfig(data)

    def get_delimiters_for(self, file_name: str) -> tuple[str] | None:
        """Returns a set of delimiters for file_name."""

        file_name = file_name.split("/")[-1]
        for rgx, dels in self._delimiters.items():
            if rgx.match(file_name):
                return dels
        return None

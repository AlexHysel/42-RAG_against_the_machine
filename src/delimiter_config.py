import re
import json
from pydantic import BaseModel, PrivateAttr
from pathlib import Path


class DelimiterConfig(BaseModel):
    _delimiters: dict[re.Pattern[str], tuple[str, ...]] = PrivateAttr()

    def __init__(self, delimiters: dict[str, tuple[str]]):
        super().__init__()
        self._delimiters = {re.compile(k): tuple(v) for k, v in delimiters.items()}
        print(f'DelimiterConfig created with {len(self._delimiters)} patterns')

    @classmethod
    def from_file(cls, file_path: Path) -> 'DelimiterConfig':
        """Create DelimiterConfig from config json file."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return DelimiterConfig(data)

    def get_delimiters_for(self, file_path: Path) -> tuple[str] | None:
        """Returns a set of delimiters for file_name."""

        for rgx, dels in self._delimiters.items():
            if rgx.match(file_path.name):
                return dels
        return None

    def supports(self, file_path: Path) -> bool:
        """Returns true if supports such files. Otherwise false."""

        return any(d.match(file_path.name) for d in self._delimiters)

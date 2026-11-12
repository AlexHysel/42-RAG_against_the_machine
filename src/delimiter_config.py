import re
from pydantic import BaseModel, PrivateAttr


class DelimiterConfig(BaseModel):
    _delimiters: dict[re.Pattern[str], set[str]] = PrivateAttr()

    def __init__(self, delimiters: dict[str, set[str]]):
        super().__init__()
        self._delimiters = {re.compile(k): v for k, v in delimiters.items()}

    def get_delimiters_for(self, file_name: str) -> set[str] | None:
        """Returns a set of delimiters for file_name."""

        file_name = file_name.split("/")[-1]
        for rgx, dels in self._delimiters.items():
            if rgx.match(file_name):
                return dels
        return None

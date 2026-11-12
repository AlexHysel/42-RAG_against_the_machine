from pydantic import BaseModel
from delimiter_config import DelimiterConfig


class Chunker:
    delimiters: DelimiterConfig

    def Chunk(content: str, file_path=None):
        pass

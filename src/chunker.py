from pydantic import BaseModel, FilePath
import re
from delimiter_config import DelimiterConfig
from chunk import Chunk


chunk_size = 2000
overlap_size = 200

class Chunker(BaseModel):
    delimiter_config: DelimiterConfig

    def ChunkFile(self, file_path: FilePath) -> list[Chunk]:
        delimiters = self.delimiter_config.get_delimiters_for(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        chunks = self.Chunk(content, delimiters)
        for chunk in chunks: chunk.file_path = file_path
        return chunks

    def Chunk(self, text: str,
              delimiters: tuple[str],
              offset: int = 0,
              ) -> list[Chunk]:
        if len(text) < chunk_size:
            return [Chunk.create(offset, text)]
        else:
            return self.Chunk()

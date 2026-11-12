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

    def Chunk(self,
              text: str,
              delimiters: tuple[str],
              offset: int = 0,
              ) -> list[Chunk]:
        if len(text) < chunk_size:
            return [Chunk.create(offset, text)]
            
        parts = []
        if len(delimiters) > 0:
            parts = self._splitWithOverlap(text, delimiters[0])
        else:
            parts = self._splitBySize(text)

        chunks = []
        for part, part_offset in parts:
            chunks.extend(self.Chunk(part, delimiters[1:], offset + part_offset))
        return chunks

    def _splitBySize(self, text: str) -> list[tuple[str, int]]:
        parts = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                split_at = text.rfind(" ", start, end)

                if split_at > start:
                    end = split_at + 1

            parts.append((text[start:end], start))

            if end >= len(text):
                break

            start = max(start + 1, end - overlap_size)

        return parts

    def _splitWithOverlap(self,
                          text: str,
                          delimiter: str
                          ) -> list[tuple[str, int]]:
        """Returns a list of tuples with text and offset."""

        indices = [m.start() for m in re.finditer(re.escape(delimiter), text)]
        indices = [0] + indices + [len(text)]

        parts = []
        for i in range(len(indices) - 1):
            start = max(0, indices[i] - overlap_size)
            end = indices[i + 1]
            part = text[start:end]
            if part:
                parts.append((part, start))

        return parts
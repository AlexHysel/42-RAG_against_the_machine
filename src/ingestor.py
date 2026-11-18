from pydantic import FilePath
from pathlib import Path


class Ingestor:

    def get_all_files(directory: Path) -> list[FilePath]:
        return [
            FilePath(path)
            for path in directory.rglob('*')
            if path.is_file()
        ]
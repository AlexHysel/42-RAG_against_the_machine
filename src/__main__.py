from pathlib import Path
import fire

from .chunker import Chunker
from .chunk import Chunk
from .delimiter_config import DelimiterConfig


def get_all_files(directory: Path) -> list[Path]:
    """Recursively find all files in a directory."""
    return [
        path
        for path in directory.rglob("*")
        if path.is_file()
    ]


def index(
    max_chunk_size: int = 2000,
    dataset_path: str = "data/raw",
    save_directory: str = "data/processed",
):
    """Build and save the BM25 index."""
    source_directory = Path(dataset_path)
    output_directory = Path(save_directory)

    if not source_directory.is_dir():
        raise ValueError(f"Dataset directory does not exist: {source_directory}")

    files = get_all_files(source_directory)

    print(f"Found {len(files)} files")

    delimiter_config = DelimiterConfig.from_file("src/delimiters.json")
    chunker = Chunker(delimiter_config=delimiter_config, chunk_size=2000, overlap_size=200)
    # TODO: Chunk all supported files
    # TODO: Build BM25 index
    # TODO: Save index to output_directory


def search(query: str, k: int = 10):
    """Search for the most relevant chunks."""
    # TODO: Load index
    # TODO: Retrieve top-k results
    pass


def search_dataset(
    dataset_path: str,
    k: int = 10,
    save_directory: str = "data/output/search_results",
):
    """Search for all questions in a dataset."""
    # TODO
    pass


def answer(query: str, k: int = 10):
    """Generate an answer using retrieved context."""
    # TODO
    pass


def answer_dataset(
    student_search_results_path: str,
    save_directory: str = "data/output/search_results_and_answer",
):
    """Generate answers for a search results dataset."""
    # TODO
    pass


def evaluate(
    student_search_results_path: str,
    dataset_path: str,
):
    """Evaluate retrieval quality using Recall@k."""
    # TODO
    pass


if __name__ == "__main__":
    fire.Fire({
        "index": index,
        "search": search,
        "search_dataset": search_dataset,
        "answer": answer,
        "answer_dataset": answer_dataset,
        "evaluate": evaluate,
    })

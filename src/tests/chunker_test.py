from src.chunker import Chunker
from src.delimiter_config import DelimiterConfig


def make_chunker(delimiters=(), chunk_size=10, overlap_size=2):
    config = DelimiterConfig({
        ".*": delimiters
    })

    return Chunker(
        delimiter_config=config,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )


def test_split_by_size():
    chunker = make_chunker()

    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunker.Chunk(text, ())

    assert [chunk.content for chunk in chunks] == [
        "abcdefghij",
        "ijklmnopqr",
        "qrstuvwxyz",
    ]

    assert [chunk.start for chunk in chunks] == [0, 8, 16]


def test_delimiter_segments_are_merged():
    chunker = make_chunker(("\n",))

    text = "aaa\nbbb\nccc\nddd"
    chunks = chunker.Chunk(text, ("\n",))

    assert [chunk.content for chunk in chunks] == [
        "aaa\nbbb",
        "bb\nccc\nddd",
    ]

    assert [chunk.start for chunk in chunks] == [0, 5]


def test_delimiter_segments_with_overlap():
    chunker = make_chunker(("\n",))

    text = "AAAA\nBBBB\nCCCC\nDDDD"
    chunks = chunker.Chunk(text, ("\n",))

    assert [chunk.content for chunk in chunks] == [
        "AAAA\nBBBB",
        "BB\nCCCC",
        "CC\nDDDD"
    ]

    assert [chunk.start for chunk in chunks] == [0, 7, 12]


def test_chunk_size_limit():
    chunker = make_chunker(
        ("\n",),
        chunk_size=10,
        overlap_size=2,
    )

    text = "AAAA\nBBBB\nCCCC\nDDDD"
    chunks = chunker.Chunk(text, ("\n",))

    assert all(len(chunk.content) <= 10 for chunk in chunks)


def test_chunk_offsets():
    chunker = make_chunker(("\n",))

    text = "AAAA\nBBBB\nCCCC\nDDDD"
    chunks = chunker.Chunk(text, ("\n",))

    for chunk in chunks:
        assert chunk.end - chunk.start == len(chunk.content)
        assert text[chunk.start:chunk.end] == chunk.content


def test_no_delimiter_fallback():
    chunker = make_chunker(
        ("\\n",),
        chunk_size=10,
        overlap_size=2,
    )

    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunker.Chunk(text, ("\\n",))

    assert all(len(chunk.content) <= 10 for chunk in chunks)

    for chunk in chunks:
        assert text[chunk.start:chunk.end] == chunk.content


def test_empty_text():
    chunker = make_chunker()

    assert chunker.Chunk("", ()) == []

from chunker import Chunker
from delimiter_config import DelimiterConfig


def make_chunker(delimiters=()):
    config = DelimiterConfig({
        ".*": delimiters
    })

    return Chunker(
        delimiter_config=config,
        chunk_size=10,
        overlap_size=2,
    )


def print_chunks(chunks):
    for chunk in chunks:
        print(f"[{chunk.start}:{chunk.end}] {chunk.content!r}")


def test_split_by_size():
    chunker = make_chunker()

    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunker.Chunk(text, ())

    print_chunks(chunks)

    assert [chunk.content for chunk in chunks] == [
        "abcdefghij",
        "ijklmnopqr",
        "qrstuvwxyz",
    ]

    assert [chunk.start for chunk in chunks] == [0, 8, 16]


def test_split_with_delimiter():
    chunker = make_chunker(("\n",))

    text = "aaa\nbbb\nccc\nddd"

    chunks = chunker.Chunk(text, ("\n",))

    print_chunks(chunks)

    assert [chunk.content for chunk in chunks] == [
        "aaa",
        "aa\nbbb",
        "bb\nccc",
        "cc\nddd",
    ]

    assert [chunk.start for chunk in chunks] == [0, 1, 5, 9]


def test_split_with_delimiter_and_overlap():
    chunker = make_chunker(("\n",))

    text = "AAAA\nBBBB\nCCCC\nDDDD"

    chunks = chunker.Chunk(text, ("\n",))

    print_chunks(chunks)

    assert [chunk.content for chunk in chunks] == [
        "AAAA",
        "AA\nBBBB",
        "BB\nCCCC",
        "CC\nDDDD",
    ]

    assert [chunk.start for chunk in chunks] == [0, 2, 7, 12]


def test_chunk_offsets():
    chunker = make_chunker(("\n",))

    text = "AAAA\nBBBB\nCCCC\nDDDD"

    chunks = chunker.Chunk(text, ("\n",))

    for chunk in chunks:
        assert text[chunk.start:chunk.end] == chunk.content

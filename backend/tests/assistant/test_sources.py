from app.assistant.schemas import SourceChunk
from app.assistant.sources import build_cited_sources, build_source_block


def make_chunk(**kwargs):
    defaults = dict(
        chunk_id="c1",
        document_id="d1",
        document_title="Reading Basics",
        text="Some source text.",
        score=0.9,
    )
    defaults.update(kwargs)
    return SourceChunk(**defaults)


def test_build_source_block_escapes_quotes_in_titles():
    chunk = make_chunk(document_title='Reading "Basics"')

    block, label_map = build_source_block([chunk])

    assert 'title="Reading &quot;Basics&quot;"' in block
    assert label_map == {"S1": chunk}


def test_build_source_block_labels_in_retrieval_order():
    chunks = [make_chunk(chunk_id="c1"), make_chunk(chunk_id="c2"), make_chunk(chunk_id="c3")]

    block, label_map = build_source_block(chunks)

    assert list(label_map.keys()) == ["S1", "S2", "S3"]
    assert block.index('id="S1"') < block.index('id="S2"') < block.index('id="S3"')


def test_build_cited_sources_cuts_excerpt_at_word_boundary():
    long_text = ("word " * 100).strip()
    chunk = make_chunk(text=long_text)
    _, label_map = build_source_block([chunk])

    sources = build_cited_sources(["S1"], label_map)

    assert len(sources) == 1
    excerpt = sources[0].excerpt
    assert excerpt.endswith("...")
    assert not excerpt[: -len("...")].endswith(" ")


def test_build_cited_sources_only_includes_given_labels_in_order():
    chunks = [make_chunk(chunk_id="c1"), make_chunk(chunk_id="c2"), make_chunk(chunk_id="c3")]
    _, label_map = build_source_block(chunks)

    sources = build_cited_sources(["S2"], label_map)

    assert [s.chunk_id for s in sources] == ["c2"]

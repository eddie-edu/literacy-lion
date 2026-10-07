from app.assistant.schemas import SourceChunk


def make_chunk(**kwargs):
    defaults = dict(chunk_id="c1", document_id="d1", document_title="t", text="x", score=1.0)
    defaults.update(kwargs)
    return SourceChunk(**defaults)


def test_location_single_page():
    assert make_chunk(page_start=5, page_end=5).location == "p. 5"


def test_location_single_page_no_end_given():
    assert make_chunk(page_start=5).location == "p. 5"


def test_location_page_range():
    assert make_chunk(page_start=5, page_end=7).location == "pp. 5–7"


def test_location_section_only():
    assert make_chunk(section="Chapter 2: Phonics").location == "Chapter 2: Phonics"


def test_location_neither_page_nor_section():
    assert make_chunk().location == ""

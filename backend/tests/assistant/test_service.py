from app.assistant.constraints import NO_MATCH_MESSAGE
from app.assistant.schemas import SourceChunk
from app.assistant.service import answer_question


def make_chunk(chunk_id="c1", score=0.9, **kwargs):
    defaults = dict(
        chunk_id=chunk_id,
        document_id="d1",
        document_title="Reading Foundations",
        text="Phonics instruction improves decoding accuracy.",
        score=score,
    )
    defaults.update(kwargs)
    return SourceChunk(**defaults)


def test_no_chunks_short_circuits_to_none(thresholds):
    thresholds(strong=0.8, weak=0.5)
    called = []

    def fake_llm(system, user):
        called.append(True)
        return "[S1]"

    result = answer_question("What is phonics?", [], fake_llm)

    assert result.coverage == "none"
    assert result.answer == NO_MATCH_MESSAGE
    assert result.sources == []
    assert called == []


def test_score_below_min_short_circuits_to_none(thresholds):
    thresholds(strong=0.8, weak=0.5)
    called = []

    def fake_llm(system, user):
        called.append(True)
        return "irrelevant"

    result = answer_question("What is phonics?", [make_chunk(score=0.2)], fake_llm)

    assert result.coverage == "none"
    assert called == []


def test_score_between_thresholds_is_weak_and_flags_user_turn(thresholds):
    thresholds(strong=0.8, weak=0.5)
    captured = {}

    def fake_llm(system, user):
        captured["user"] = user
        return "Some answer [S1]"

    result = answer_question("What is phonics?", [make_chunk(score=0.6)], fake_llm)

    assert result.coverage == "weak"
    assert "<coverage>limited</coverage>" in captured["user"]


def test_score_above_strong_has_no_coverage_flag(thresholds):
    thresholds(strong=0.8, weak=0.5)
    captured = {}

    def fake_llm(system, user):
        captured["user"] = user
        return "Some answer [S1]"

    result = answer_question("What is phonics?", [make_chunk(score=0.95)], fake_llm)

    assert result.coverage == "strong"
    assert "<coverage>limited</coverage>" not in captured["user"]


def test_invalid_citation_is_stripped_and_only_valid_source_kept(thresholds, caplog):
    thresholds(strong=0.8, weak=0.5)
    chunks = [make_chunk(chunk_id=f"c{i}", score=0.9) for i in range(1, 4)]

    def fake_llm(system, user):
        return "Phonics matters [S1] and so does this [S9]."

    with caplog.at_level("WARNING"):
        result = answer_question("What is phonics?", chunks, fake_llm)

    assert "[S9]" not in result.answer
    assert [s.label for s in result.sources] == ["S1"]
    assert any("S9" in record.message for record in caplog.records)


def test_sources_only_include_cited_labels(thresholds):
    thresholds(strong=0.8, weak=0.5)
    chunks = [make_chunk(chunk_id=f"c{i}", score=0.9) for i in range(1, 4)]

    def fake_llm(system, user):
        return "Only the second source is cited [S2]."

    result = answer_question("What is phonics?", chunks, fake_llm)

    assert [s.label for s in result.sources] == ["S2"]
    assert result.sources[0].chunk_id == "c2"

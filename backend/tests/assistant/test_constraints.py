import pytest

from app.assistant import config
from app.assistant.constraints import classify_coverage, extract_citations


def test_classify_coverage_raises_when_thresholds_unset(monkeypatch):
    monkeypatch.setattr(config.settings, "STRONG_MATCH_THRESHOLD", None)
    monkeypatch.setattr(config.settings, "MIN_MATCH_THRESHOLD", None)

    with pytest.raises(RuntimeError):
        classify_coverage([])


def test_extract_citations_dedupes_and_preserves_first_appearance_order():
    answer = "First [S2], then [S1], again [S2]."
    assert extract_citations(answer) == ["S2", "S1"]

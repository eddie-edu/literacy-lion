import pytest

from app.assistant import config


@pytest.fixture
def thresholds(monkeypatch):
    """Set STRONG/MIN match thresholds for a test, via monkeypatch (not config defaults)."""

    def _set(strong: float, weak: float) -> None:
        monkeypatch.setattr(config.settings, "STRONG_MATCH_THRESHOLD", strong)
        monkeypatch.setattr(config.settings, "MIN_MATCH_THRESHOLD", weak)

    return _set

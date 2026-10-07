"""Runtime configuration for the assistant module, loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _float_from_env(name: str) -> float | None:
    value = os.getenv(name)
    if value is None or value == "":
        return None
    return float(value)


@dataclass
class Settings:
    # Thresholds are intentionally left unset until tuned against real queries.
    STRONG_MATCH_THRESHOLD: float | None = None
    MIN_MATCH_THRESHOLD: float | None = None


settings = Settings(
    STRONG_MATCH_THRESHOLD=_float_from_env("STRONG_MATCH_THRESHOLD"),
    MIN_MATCH_THRESHOLD=_float_from_env("MIN_MATCH_THRESHOLD"),
)


def validate_settings(settings: Settings) -> None:
    # Takes settings as a parameter (rather than closing over the module-level
    # `settings` object) so tests can pass a monkeypatched instance.
    """Raise a clear, actionable error if required thresholds are unset.

    Intended to be called once at application startup so misconfiguration is
    caught before serving traffic, rather than surfacing as a RuntimeError on
    the first request that reaches classify_coverage.
    """
    missing = [
        name
        for name in ("STRONG_MATCH_THRESHOLD", "MIN_MATCH_THRESHOLD")
        if getattr(settings, name) is None
    ]
    if missing:
        raise RuntimeError(
            f"Missing required assistant config: {', '.join(missing)}. "
            "Set these environment variables before starting the app."
        )

"""Orchestrates a single assistant turn: coverage gate, prompting, citation validation."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from app.assistant.constraints import (
    NO_MATCH_MESSAGE,
    Coverage,
    classify_coverage,
    extract_citations,
    validate_citations,
)
from app.assistant.schemas import AssistantResponse, SourceChunk
from app.assistant.sources import build_cited_sources, build_source_block

LLMCall = Callable[[str, str], str]

# Loaded once at import time, not per request.
SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.md").read_text(encoding="utf-8")


def answer_question(question: str, chunks: list[SourceChunk], llm_call: LLMCall) -> AssistantResponse:
    coverage = classify_coverage(chunks)

    if coverage is Coverage.NONE:
        return AssistantResponse(answer=NO_MATCH_MESSAGE, coverage=Coverage.NONE.value, sources=[])

    source_block, label_map = build_source_block(chunks)

    user_turn_parts = [source_block]
    if coverage is Coverage.WEAK:
        user_turn_parts.append("<coverage>limited</coverage>")
    user_turn_parts.append(f"Question: {question}")
    user_turn = "\n\n".join(user_turn_parts)

    raw_answer = llm_call(SYSTEM_PROMPT, user_turn)

    cited_labels = extract_citations(raw_answer)
    cleaned_answer, _invalid = validate_citations(raw_answer, label_map)
    # Re-filter against label_map: validate_citations already strips invalid
    # [Sx] tags from the answer text, but cited_labels was extracted before
    # that pass and needs the same filtering applied to it.
    cited_labels = [label for label in cited_labels if label in label_map]

    sources = build_cited_sources(cited_labels, label_map)

    return AssistantResponse(answer=cleaned_answer, coverage=coverage.value, sources=sources)

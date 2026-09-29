"""Builds the <sources> block shown to the LLM and the cited-source list shown to the user."""

from __future__ import annotations

from html import escape

from app.assistant.schemas import CitedSource, SourceChunk

EXCERPT_LENGTH = 200


def build_source_block(chunks: list[SourceChunk]) -> tuple[str, dict[str, SourceChunk]]:
    """Relabel chunks S1..Sn in retrieval order and render them as an XML-style block.

    The model only ever sees these relabeled IDs, never DB chunk_ids.
    """
    label_map: dict[str, SourceChunk] = {}
    parts = ["<sources>"]
    for i, chunk in enumerate(chunks, start=1):
        label = f"S{i}"
        label_map[label] = chunk
        title = escape(chunk.document_title, quote=True)
        location = escape(chunk.location, quote=True)
        text = escape(chunk.text, quote=False)
        parts.append(f'<source id="{label}" title="{title}" location="{location}">{text}</source>')
    parts.append("</sources>")
    return "".join(parts), label_map


def _excerpt(text: str, length: int = EXCERPT_LENGTH) -> str:
    text = text.strip()
    if len(text) <= length:
        return text
    # Cut on the nearest word boundary rather than mid-word; fall back to a
    # hard cut if there's no space before `length` (e.g. one very long word).
    cut = text.rfind(" ", 0, length)
    if cut <= 0:
        cut = length
    return text[:cut].rstrip() + "..."


def build_cited_sources(cited_labels: list[str], label_map: dict[str, SourceChunk]) -> list[CitedSource]:
    """Build the user-facing source list from cited labels only, in citation order."""
    sources = []
    for label in cited_labels:
        chunk = label_map.get(label)
        if chunk is None:
            continue
        sources.append(
            CitedSource(
                label=label,
                chunk_id=chunk.chunk_id,
                title=chunk.document_title,
                publisher=chunk.publisher,
                location=chunk.location,
                excerpt=_excerpt(chunk.text),
                url=chunk.url,
            )
        )
    return sources

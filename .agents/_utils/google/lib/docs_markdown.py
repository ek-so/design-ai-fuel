"""Practical markdown ↔ Google Docs helpers (headings, lists, bold/italic, links, tables)."""

from __future__ import annotations

import re
from typing import Any

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_UL = re.compile(r"^[-*+]\s+(.*)$")
_OL = re.compile(r"^(\d+)\.\s+(.*)$")
_TABLE_ROW = re.compile(r"^\|(.+)\|$")
_TABLE_SEP = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")
_INLINE = re.compile(
    r"(\*\*[^*]+\*\*|__[^_]+__|\*[^*]+\*|_[^_]+_|\[[^\]]+\]\([^)]+\)|`[^`]+`)"
)


def _plain_inline(text: str) -> str:
    """Strip common markdown inline markers for plain extraction."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def _inline_requests(text: str, start_index: int) -> tuple[str, list[dict[str, Any]]]:
    """Build insertable plain text + textStyle requests for a run of inline markdown."""
    requests: list[dict[str, Any]] = []
    parts: list[str] = []
    cursor = 0
    out_index = start_index

    for match in _INLINE.finditer(text):
        if match.start() > cursor:
            chunk = text[cursor : match.start()]
            parts.append(chunk)
            out_index += len(chunk)

        token = match.group(0)
        if token.startswith("**") or token.startswith("__"):
            inner = token[2:-2]
            style = {"bold": True}
        elif token.startswith("*") or token.startswith("_"):
            inner = token[1:-1]
            style = {"italic": True}
        elif token.startswith("`"):
            inner = token[1:-1]
            style = {
                "weightedFontFamily": {"fontFamily": "Roboto Mono", "weight": 400}
            }
        elif token.startswith("["):
            link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            assert link_match
            inner = link_match.group(1)
            style = {"link": {"url": link_match.group(2)}}
        else:
            inner = token
            style = {}

        parts.append(inner)
        end = out_index + len(inner)
        if style:
            requests.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": out_index, "endIndex": end},
                        "textStyle": style,
                        "fields": ",".join(style.keys()),
                    }
                }
            )
        out_index = end
        cursor = match.end()

    if cursor < len(text):
        parts.append(text[cursor:])

    return "".join(parts), requests


def markdown_to_insert_requests(markdown: str, *, start_index: int = 1) -> list[dict[str, Any]]:
    """Convert markdown into Docs batchUpdate requests inserted at start_index."""
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    insert_chunks: list[str] = []
    style_requests: list[dict[str, Any]] = []
    list_ranges: list[tuple[int, int, str]] = []  # start, end, preset
    index = start_index
    i = 0

    while i < len(lines):
        line = lines[i]

        # Table block
        if _TABLE_ROW.match(line) and i + 1 < len(lines) and _TABLE_SEP.match(lines[i + 1]):
            rows: list[list[str]] = []
            while i < len(lines) and _TABLE_ROW.match(lines[i]):
                if _TABLE_SEP.match(lines[i]):
                    i += 1
                    continue
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                rows.append([_plain_inline(c) for c in cells])
                i += 1
            if rows:
                # Insert as tab-separated plain text (Docs table create is heavy); keep readable.
                for row in rows:
                    text = "\t".join(row) + "\n"
                    insert_chunks.append(text)
                    index += len(text)
            continue

        heading = _HEADING.match(line)
        if heading:
            level = min(len(heading.group(1)), 6)
            plain, inline_reqs = _inline_requests(heading.group(2), index)
            text = plain + "\n"
            insert_chunks.append(text)
            end = index + len(plain)
            style_requests.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": end + 1},
                        "paragraphStyle": {"namedStyleType": f"HEADING_{level}"},
                        "fields": "namedStyleType",
                    }
                }
            )
            style_requests.extend(inline_reqs)
            index += len(text)
            i += 1
            continue

        ul = _UL.match(line)
        if ul:
            start = index
            while i < len(lines):
                m = _UL.match(lines[i])
                if not m:
                    break
                plain, inline_reqs = _inline_requests(m.group(1), index)
                text = plain + "\n"
                insert_chunks.append(text)
                style_requests.extend(inline_reqs)
                index += len(text)
                i += 1
            list_ranges.append((start, index, "BULLET_DISC_CIRCLE_SQUARE"))
            continue

        ol = _OL.match(line)
        if ol:
            start = index
            while i < len(lines):
                m = _OL.match(lines[i])
                if not m:
                    break
                plain, inline_reqs = _inline_requests(m.group(2), index)
                text = plain + "\n"
                insert_chunks.append(text)
                style_requests.extend(inline_reqs)
                index += len(text)
                i += 1
            list_ranges.append((start, index, "NUMBERED_DECIMAL_ALPHA_ROMAN"))
            continue

        if line.strip() == "":
            insert_chunks.append("\n")
            index += 1
            i += 1
            continue

        plain, inline_reqs = _inline_requests(line, index)
        text = plain + "\n"
        insert_chunks.append(text)
        style_requests.extend(inline_reqs)
        index += len(text)
        i += 1

    body_text = "".join(insert_chunks)
    if not body_text:
        return []

    requests: list[dict[str, Any]] = [
        {"insertText": {"location": {"index": start_index}, "text": body_text}}
    ]
    for start, end, preset in list_ranges:
        if end > start:
            requests.append(
                {
                    "createParagraphBullets": {
                        "range": {"startIndex": start, "endIndex": end},
                        "bulletPreset": preset,
                    }
                }
            )
    requests.extend(style_requests)
    return requests


def docs_body_to_markdown(document: dict[str, Any]) -> str:
    """Best-effort Docs structural element dump to markdown."""
    body = document.get("body", {}).get("content", [])
    lines: list[str] = []

    for element in body:
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        style = paragraph.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        text_parts: list[str] = []
        for el in paragraph.get("elements", []):
            tr = el.get("textRun")
            if not tr:
                continue
            content = tr.get("content", "")
            ts = tr.get("textStyle", {})
            if ts.get("link", {}).get("url"):
                content = f"[{content.rstrip()}]({ts['link']['url']})" + (
                    "\n" if content.endswith("\n") else ""
                )
            elif ts.get("bold") and ts.get("italic"):
                content = f"***{content.rstrip()}***" + (
                    "\n" if content.endswith("\n") else ""
                )
            elif ts.get("bold"):
                content = f"**{content.rstrip()}**" + (
                    "\n" if content.endswith("\n") else ""
                )
            elif ts.get("italic"):
                content = f"*{content.rstrip()}*" + (
                    "\n" if content.endswith("\n") else ""
                )
            text_parts.append(content)
        text = "".join(text_parts).rstrip("\n")
        bullet = paragraph.get("bullet")
        if bullet is not None:
            lines.append(f"- {text}")
            continue
        if style.startswith("HEADING_"):
            level = style.rsplit("_", 1)[-1]
            try:
                n = int(level)
            except ValueError:
                n = 1
            lines.append(f"{'#' * n} {text}")
        else:
            lines.append(text)

    return "\n".join(lines).strip() + "\n"

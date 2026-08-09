"""Google Slides create / read / export from a simple outline."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from auth import build_service
from cli_common import slides_url
from config import EXPORT_MIME, MIME_GOOGLE_SLIDES
from drive_io import create_file, export_to_path

_SLIDE_HEADING = re.compile(r"^#\s+(.*)$")
_BULLET = re.compile(r"^[-*+]\s+(.*)$")


def slides_service() -> Any:
    return build_service("slides", "v1")


def parse_outline(path: Path) -> list[dict[str, Any]]:
    """Parse outline.md (# title + bullets) or outline.json (list of {title, bullets})."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("JSON outline must be a list of slides")
        slides: list[dict[str, Any]] = []
        for item in data:
            slides.append(
                {
                    "title": str(item.get("title", "Untitled")),
                    "bullets": [str(b) for b in item.get("bullets", [])],
                }
            )
        return slides

    slides = []
    current: dict[str, Any] | None = None
    for line in text.replace("\r\n", "\n").split("\n"):
        heading = _SLIDE_HEADING.match(line)
        if heading:
            if current:
                slides.append(current)
            current = {"title": heading.group(1).strip(), "bullets": []}
            continue
        bullet = _BULLET.match(line)
        if bullet and current is not None:
            current["bullets"].append(bullet.group(1).strip())
    if current:
        slides.append(current)
    if not slides:
        slides = [{"title": path.stem, "bullets": []}]
    return slides


def create_presentation(
    *,
    title: str,
    outline_path: Path | None = None,
    folder_id: str | None = None,
) -> dict[str, str]:
    parents = [folder_id] if folder_id else None
    meta = create_file(name=title, mime_type=MIME_GOOGLE_SLIDES, parents=parents)
    presentation_id = meta["id"]

    if outline_path:
        _populate_from_outline(presentation_id, parse_outline(outline_path))

    return {
        "id": presentation_id,
        "title": title,
        "url": meta.get("url") or slides_url(presentation_id),
    }


def _populate_from_outline(presentation_id: str, slides: list[dict[str, Any]]) -> None:
    svc = slides_service()
    presentation = svc.presentations().get(presentationId=presentation_id).execute()
    existing = presentation.get("slides", [])
    first_id = existing[0]["objectId"] if existing else None

    requests: list[dict[str, Any]] = []

    # Create additional blank slides (first slide already exists)
    for i in range(1, len(slides)):
        requests.append({"createSlide": {"insertionIndex": i}})

    if requests:
        svc.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests}
        ).execute()
        presentation = svc.presentations().get(presentationId=presentation_id).execute()

    page_ids = [s["objectId"] for s in presentation.get("slides", [])]
    text_requests: list[dict[str, Any]] = []

    for idx, slide in enumerate(slides):
        if idx >= len(page_ids):
            break
        page_id = page_ids[idx]
        title = slide["title"]
        bullets = slide.get("bullets") or []
        body = "\n".join(bullets)

        # Title shape + body shape via createShape + insertText (layout-agnostic).
        title_id = f"title_{idx}"
        body_id = f"body_{idx}"
        text_requests.extend(
            [
                {
                    "createShape": {
                        "objectId": title_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": page_id,
                            "size": {
                                "height": {"magnitude": 80, "unit": "PT"},
                                "width": {"magnitude": 600, "unit": "PT"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": 40,
                                "translateY": 40,
                                "unit": "PT",
                            },
                        },
                    }
                },
                {
                    "insertText": {
                        "objectId": title_id,
                        "text": title,
                        "insertionIndex": 0,
                    }
                },
            ]
        )
        if body:
            text_requests.extend(
                [
                    {
                        "createShape": {
                            "objectId": body_id,
                            "shapeType": "TEXT_BOX",
                            "elementProperties": {
                                "pageObjectId": page_id,
                                "size": {
                                    "height": {"magnitude": 300, "unit": "PT"},
                                    "width": {"magnitude": 600, "unit": "PT"},
                                },
                                "transform": {
                                    "scaleX": 1,
                                    "scaleY": 1,
                                    "translateX": 40,
                                    "translateY": 140,
                                    "unit": "PT",
                                },
                            },
                        }
                    },
                    {
                        "insertText": {
                            "objectId": body_id,
                            "text": body,
                            "insertionIndex": 0,
                        }
                    },
                ]
            )

    # Clear default placeholder text on the first auto-created slide when possible
    if first_id and not slides:
        pass

    if text_requests:
        svc.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": text_requests}
        ).execute()


def read_presentation(presentation_id: str) -> str:
    """Return a markdown outline of slide titles and text."""
    presentation = (
        slides_service().presentations().get(presentationId=presentation_id).execute()
    )
    lines: list[str] = []
    for slide in presentation.get("slides", []):
        texts: list[str] = []
        for element in slide.get("pageElements", []):
            shape = element.get("shape")
            if not shape:
                continue
            text_content = shape.get("text", {}).get("textElements", [])
            chunk = []
            for te in text_content:
                tr = te.get("textRun")
                if tr and tr.get("content"):
                    chunk.append(tr["content"])
            joined = "".join(chunk).strip()
            if joined:
                texts.append(joined)
        if not texts:
            lines.append("# Untitled slide\n")
            continue
        lines.append(f"# {texts[0]}")
        for bullet in texts[1:]:
            for part in bullet.splitlines():
                part = part.strip()
                if part:
                    lines.append(f"- {part}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def export_presentation(
    presentation_id: str,
    *,
    fmt: str,
    out_path: Path,
) -> Path:
    fmt = fmt.lower()
    mime = EXPORT_MIME.get(fmt)
    if not mime or fmt not in ("pdf", "pptx"):
        raise ValueError(f"Unsupported slides export format: {fmt}")
    return export_to_path(presentation_id, mime, out_path)

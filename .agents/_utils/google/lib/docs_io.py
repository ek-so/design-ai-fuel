"""Google Docs create / read / update / export."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from auth import build_service
from cli_common import doc_url
from config import EXPORT_MIME, MIME_GOOGLE_DOC
from docs_markdown import docs_body_to_markdown, markdown_to_insert_requests
from drive_io import create_file, export_to_path


def docs_service() -> Any:
    return build_service("docs", "v1")


def create_doc(
    *,
    title: str,
    markdown: str | None = None,
    folder_id: str | None = None,
) -> dict[str, str]:
    parents = [folder_id] if folder_id else None
    meta = create_file(name=title, mime_type=MIME_GOOGLE_DOC, parents=parents)
    if markdown:
        update_doc(meta["id"], markdown=markdown, mode="replace")
    return {
        "id": meta["id"],
        "title": title,
        "url": meta.get("url") or doc_url(meta["id"]),
    }


def read_doc(document_id: str) -> dict[str, Any]:
    return docs_service().documents().get(documentId=document_id).execute()


def read_doc_markdown(document_id: str) -> str:
    return docs_body_to_markdown(read_doc(document_id))


def _end_index(document: dict[str, Any]) -> int:
    content = document.get("body", {}).get("content", [])
    if not content:
        return 1
    return int(content[-1].get("endIndex", 2))


def update_doc(
    document_id: str,
    *,
    markdown: str,
    mode: Literal["replace", "append"] = "replace",
) -> dict[str, str]:
    document = read_doc(document_id)
    requests: list[dict[str, Any]] = []

    if mode == "replace":
        end = _end_index(document)
        # Document body always has a trailing newline at index end-1; delete content before it.
        if end > 2:
            requests.append(
                {
                    "deleteContentRange": {
                        "range": {"startIndex": 1, "endIndex": end - 1}
                    }
                }
            )
        start_index = 1
    else:
        start_index = max(_end_index(document) - 1, 1)

    requests.extend(markdown_to_insert_requests(markdown, start_index=start_index))
    if requests:
        docs_service().documents().batchUpdate(
            documentId=document_id, body={"requests": requests}
        ).execute()

    title = document.get("title", "")
    return {"id": document_id, "title": title, "url": doc_url(document_id)}


def export_doc(
    document_id: str,
    *,
    fmt: str,
    out_path: Path,
) -> Path:
    fmt = fmt.lower()
    if fmt == "md":
        text = read_doc_markdown(document_id)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        return out_path

    mime = EXPORT_MIME.get(fmt)
    if not mime:
        raise ValueError(f"Unsupported docs export format: {fmt}")
    return export_to_path(document_id, mime, out_path)

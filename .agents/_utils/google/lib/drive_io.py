"""Drive helpers: create, search, share, move, folders, binary export."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from auth import build_service
from config import MIME_FOLDER


def drive_service() -> Any:
    return build_service("drive", "v3")


def create_file(
    *,
    name: str,
    mime_type: str,
    parents: list[str] | None = None,
) -> dict[str, str]:
    body: dict[str, Any] = {"name": name, "mimeType": mime_type}
    if parents:
        body["parents"] = parents
    created = (
        drive_service()
        .files()
        .create(body=body, fields="id,name,webViewLink,mimeType")
        .execute()
    )
    return {
        "id": created["id"],
        "title": created.get("name", name),
        "url": created.get("webViewLink", ""),
        "mimeType": created.get("mimeType", mime_type),
    }


def mkdir(*, title: str, parent: str | None = None) -> dict[str, str]:
    parents = [parent] if parent else None
    return create_file(name=title, mime_type=MIME_FOLDER, parents=parents)


def search(query: str, *, page_size: int = 25) -> list[dict[str, str]]:
    # Escape single quotes in Drive query strings
    safe = query.replace("\\", "\\\\").replace("'", "\\'")
    q = f"fullText contains '{safe}' and trashed = false"
    result = (
        drive_service()
        .files()
        .list(
            q=q,
            pageSize=page_size,
            fields="files(id,name,mimeType,webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )
    files = result.get("files", [])
    return [
        {
            "id": f["id"],
            "title": f.get("name", ""),
            "mimeType": f.get("mimeType", ""),
            "url": f.get("webViewLink", ""),
        }
        for f in files
    ]


def get_metadata(file_id: str) -> dict[str, str]:
    meta = (
        drive_service()
        .files()
        .get(fileId=file_id, fields="id,name,mimeType,webViewLink,parents")
        .execute()
    )
    return {
        "id": meta["id"],
        "title": meta.get("name", ""),
        "mimeType": meta.get("mimeType", ""),
        "url": meta.get("webViewLink", ""),
        "parents": ",".join(meta.get("parents") or []),
    }


def share(
    file_id: str,
    *,
    email: str | None = None,
    anyone: bool = False,
    role: str = "reader",
) -> dict[str, str]:
    if anyone:
        body = {"type": "anyone", "role": role}
    elif email:
        body = {"type": "user", "role": role, "emailAddress": email}
    else:
        raise ValueError("Provide --email or --anyone")

    drive_service().permissions().create(
        fileId=file_id,
        body=body,
        fields="id",
        sendNotificationEmail=bool(email),
    ).execute()

    meta = get_metadata(file_id)
    return meta


def move(file_id: str, folder_id: str) -> dict[str, str]:
    meta = (
        drive_service()
        .files()
        .get(fileId=file_id, fields="parents")
        .execute()
    )
    previous = ",".join(meta.get("parents") or [])
    updated = (
        drive_service()
        .files()
        .update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous,
            fields="id,name,webViewLink,parents",
        )
        .execute()
    )
    return {
        "id": updated["id"],
        "title": updated.get("name", ""),
        "url": updated.get("webViewLink", ""),
        "parents": ",".join(updated.get("parents") or []),
    }


def export_bytes(file_id: str, mime_type: str) -> bytes:
    return (
        drive_service()
        .files()
        .export(fileId=file_id, mimeType=mime_type)
        .execute()
    )


def export_to_path(file_id: str, mime_type: str, out_path: Path) -> Path:
    data = export_bytes(file_id, mime_type)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return out_path

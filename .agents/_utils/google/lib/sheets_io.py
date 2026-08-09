"""Google Sheets create / read / update / CSV export."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

from auth import build_service
from cli_common import sheet_url
from config import MIME_GOOGLE_SHEET
from drive_io import create_file


def sheets_service() -> Any:
    return build_service("sheets", "v4")


def _read_csv(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [list(row) for row in csv.reader(f)]


def create_sheet(
    *,
    title: str,
    csv_path: Path | None = None,
    folder_id: str | None = None,
) -> dict[str, str]:
    parents = [folder_id] if folder_id else None
    meta = create_file(name=title, mime_type=MIME_GOOGLE_SHEET, parents=parents)
    if csv_path:
        update_sheet(meta["id"], csv_path=csv_path, a1_range="A1")
    return {
        "id": meta["id"],
        "title": title,
        "url": meta.get("url") or sheet_url(meta["id"]),
    }


def read_sheet(
    spreadsheet_id: str,
    *,
    a1_range: str | None = None,
) -> list[list[str]]:
    if a1_range:
        result = (
            sheets_service()
            .spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=a1_range)
            .execute()
        )
        return result.get("values", [])

    # Default: first sheet, all used cells
    meta = (
        sheets_service()
        .spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets.properties.title")
        .execute()
    )
    sheets = meta.get("sheets", [])
    if not sheets:
        return []
    title = sheets[0]["properties"]["title"]
    result = (
        sheets_service()
        .spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=title)
        .execute()
    )
    return result.get("values", [])


def update_sheet(
    spreadsheet_id: str,
    *,
    csv_path: Path,
    a1_range: str = "A1",
) -> dict[str, str]:
    values = _read_csv(csv_path)
    sheets_service().spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=a1_range,
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    return {
        "id": spreadsheet_id,
        "title": "",
        "url": sheet_url(spreadsheet_id),
    }


def values_to_csv_text(values: list[list[str]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    for row in values:
        writer.writerow(row)
    return buf.getvalue()


def export_sheet_csv(
    spreadsheet_id: str,
    *,
    out_path: Path,
    a1_range: str | None = None,
) -> Path:
    values = read_sheet(spreadsheet_id, a1_range=a1_range)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(values_to_csv_text(values), encoding="utf-8")
    return out_path

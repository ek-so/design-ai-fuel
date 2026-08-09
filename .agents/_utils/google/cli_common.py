"""Argparse helpers and Google URL / file-id parsing."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# docs.google.com/document/d/ID
# docs.google.com/spreadsheets/d/ID
# docs.google.com/presentation/d/ID
# drive.google.com/file/d/ID
# drive.google.com/open?id=ID
_ID_PATTERNS = [
    re.compile(r"/document/d/([a-zA-Z0-9_-]+)"),
    re.compile(r"/spreadsheets/d/([a-zA-Z0-9_-]+)"),
    re.compile(r"/presentation/d/([a-zA-Z0-9_-]+)"),
    re.compile(r"/file/d/([a-zA-Z0-9_-]+)"),
    re.compile(r"[?&]id=([a-zA-Z0-9_-]+)"),
    re.compile(r"/folders/([a-zA-Z0-9_-]+)"),
]

_BARE_ID = re.compile(r"^[a-zA-Z0-9_-]{10,}$")


def parse_file_id(value: str) -> str:
    """Extract a Drive/Docs/Sheets/Slides file id from a URL or bare id."""
    value = value.strip()
    for pattern in _ID_PATTERNS:
        match = pattern.search(value)
        if match:
            return match.group(1)
    if _BARE_ID.match(value):
        return value
    raise argparse.ArgumentTypeError(f"Could not parse Google file id from: {value}")


def add_open_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the result URL in the default browser",
    )


def add_folder_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--folder",
        metavar="ID",
        type=parse_file_id,
        help="Parent Drive folder id or URL",
    )


def resolve_out_path(path: str | None, default_name: str, output_dir: Path) -> Path:
    """Resolve --out path; default under ~/.design-ai-fuel/output/."""
    if path:
        return Path(path).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    return (output_dir / default_name).resolve()


def doc_url(file_id: str) -> str:
    return f"https://docs.google.com/document/d/{file_id}/edit"


def sheet_url(file_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{file_id}/edit"


def slides_url(file_id: str) -> str:
    return f"https://docs.google.com/presentation/d/{file_id}/edit"


def folder_url(file_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{file_id}"


def drive_file_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"

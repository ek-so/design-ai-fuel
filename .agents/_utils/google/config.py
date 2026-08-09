"""Paths, scopes, and env overrides for design-ai-fuel Google Workspace tools."""

from __future__ import annotations

import os
from pathlib import Path

HOME = Path(
    os.environ.get("DESIGN_AI_FUEL_HOME", Path.home() / ".design-ai-fuel")
).expanduser()

VENV_DIR = HOME / ".venv"
OUTPUT_DIR = HOME / "output"
CLIENT_SECRETS = Path(
    os.environ.get("GOOGLE_CLIENT_SECRETS", HOME / "client_secret.json")
).expanduser()
TOKEN_PATH = Path(os.environ.get("GOOGLE_TOKEN", HOME / "token.json")).expanduser()

# Single consent covering Drive + Docs + Sheets + Slides (read/write/share).
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/presentations",
]

MIME_GOOGLE_DOC = "application/vnd.google-apps.document"
MIME_GOOGLE_SHEET = "application/vnd.google-apps.spreadsheet"
MIME_GOOGLE_SLIDES = "application/vnd.google-apps.presentation"
MIME_FOLDER = "application/vnd.google-apps.folder"

EXPORT_MIME = {
    "pdf": "application/pdf",
    "docx": (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ),
    "pptx": (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    ),
    "xlsx": (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ),
    "csv": "text/csv",
    "md": "text/plain",
}


def ensure_home() -> Path:
    """Create the home/output directories if missing."""
    HOME.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return HOME

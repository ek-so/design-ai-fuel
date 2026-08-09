"""Shared helpers for Google Workspace CLIs under .agents/_utils/google/."""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path


def setup_paths(script_path: str | Path) -> Path:
    """Put google/ and google/lib/ on sys.path for config/auth and *_io imports."""
    script = Path(script_path).resolve()
    google_dir = script.parent
    utils_root = google_dir.parent
    lib_dir = google_dir / "lib"

    # Running a script from `_utils/` (legacy) would put that folder on sys.path
    # and make `./google` shadow google-api-python-client. Strip it if present.
    utils_root_resolved = utils_root.resolve()
    sys.path[:] = [
        p for p in sys.path if p and Path(p).resolve() != utils_root_resolved
    ]

    for path in (str(lib_dir), str(google_dir)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    return google_dir


def print_result(
    *, kind: str, file_id: str, url: str, title: str | None = None
) -> None:
    """Print machine-friendly result lines for agent chaining."""
    print(f"kind: {kind}")
    if title:
        print(f"title: {title}")
    print(f"id: {file_id}")
    print(f"url: {url}")


def open_in_browser(url: str) -> None:
    webbrowser.open(url)


def exit_on_missing_dependency(exc: ImportError) -> None:
    print(
        f"Missing dependency: {exc.name or exc}\n"
        "Run: .agents/_utils/google/setup.sh\n"
        "Then: source .agents/_utils/google/activate.sh",
        file=sys.stderr,
    )
    sys.exit(1)

#!/usr/bin/env python3
"""Google Slides CLI: create, read, export."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
sys.path.insert(0, str(_SCRIPT.parent))

from bootstrap import (  # noqa: E402
    exit_on_missing_dependency,
    open_in_browser,
    print_result,
    setup_paths,
)

setup_paths(_SCRIPT)

try:
    from cli_common import (
        add_folder_flag,
        add_open_flag,
        parse_file_id,
        resolve_out_path,
    )
    from config import OUTPUT_DIR
    from slides_io import create_presentation, export_presentation, read_presentation
except ImportError as exc:
    exit_on_missing_dependency(exc)
    raise


def cmd_create(args: argparse.Namespace) -> int:
    outline = Path(args.from_file) if args.from_file else None
    result = create_presentation(
        title=args.title, outline_path=outline, folder_id=args.folder
    )
    print_result(
        kind="presentation",
        file_id=result["id"],
        url=result["url"],
        title=result["title"],
    )
    if args.open:
        open_in_browser(result["url"])
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    text = read_presentation(file_id)
    if args.out:
        out = resolve_out_path(args.out, f"{file_id}.md", OUTPUT_DIR)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"wrote: {out}")
    else:
        sys.stdout.write(text)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    out = resolve_out_path(args.out, f"{file_id}.{args.format}", OUTPUT_DIR)
    path = export_presentation(file_id, fmt=args.format, out_path=out)
    print(f"wrote: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Slides tools for design-ai-fuel")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a presentation from an outline")
    create.add_argument("--title", required=True)
    create.add_argument("--from", dest="from_file", metavar="outline.md|json")
    add_folder_flag(create)
    add_open_flag(create)
    create.set_defaults(func=cmd_create)

    read = sub.add_parser("read", help="Read slides as a markdown outline")
    read.add_argument("target", help="Slides URL or id")
    read.add_argument("--out", metavar="PATH")
    read.set_defaults(func=cmd_read)

    export = sub.add_parser("export", help="Export a presentation")
    export.add_argument("target", help="Slides URL or id")
    export.add_argument("--format", choices=("pdf", "pptx"), required=True)
    export.add_argument("--out", metavar="PATH")
    export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

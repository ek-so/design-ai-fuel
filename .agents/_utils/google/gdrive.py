#!/usr/bin/env python3
"""Google Drive CLI: search, share, mkdir, move."""

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
    from cli_common import add_open_flag, folder_url, parse_file_id
    from drive_io import mkdir, move, search, share
except ImportError as exc:
    exit_on_missing_dependency(exc)
    raise


def cmd_search(args: argparse.Namespace) -> int:
    results = search(args.query, page_size=args.limit)
    if not results:
        print("No results.")
        return 0
    for item in results:
        print(f"- {item['title']}")
        print(f"  id: {item['id']}")
        print(f"  mime: {item['mimeType']}")
        print(f"  url: {item['url']}")
    return 0


def cmd_share(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    if not args.anyone and not args.email:
        print("Provide --email or --anyone", file=sys.stderr)
        return 2
    result = share(
        file_id, email=args.email, anyone=args.anyone, role=args.role
    )
    print_result(
        kind="shared",
        file_id=result["id"],
        url=result["url"],
        title=result.get("title"),
    )
    if args.open:
        open_in_browser(result["url"])
    return 0


def cmd_mkdir(args: argparse.Namespace) -> int:
    parent = parse_file_id(args.parent) if args.parent else None
    result = mkdir(title=args.title, parent=parent)
    url = result.get("url") or folder_url(result["id"])
    print_result(kind="folder", file_id=result["id"], url=url, title=result["title"])
    if args.open:
        open_in_browser(url)
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    file_id = parse_file_id(args.target)
    folder_id = parse_file_id(args.folder)
    result = move(file_id, folder_id)
    print_result(
        kind="moved",
        file_id=result["id"],
        url=result["url"],
        title=result.get("title"),
    )
    print(f"parents: {result.get('parents', '')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Drive tools for design-ai-fuel")
    sub = parser.add_subparsers(dest="command", required=True)

    search_p = sub.add_parser("search", help="Search Drive by full text")
    search_p.add_argument("query")
    search_p.add_argument("--limit", type=int, default=25)
    search_p.set_defaults(func=cmd_search)

    share_p = sub.add_parser("share", help="Share a file")
    share_p.add_argument("target", help="File URL or id")
    share_p.add_argument("--email")
    share_p.add_argument("--anyone", action="store_true")
    share_p.add_argument(
        "--role", choices=("reader", "writer", "commenter"), default="reader"
    )
    add_open_flag(share_p)
    share_p.set_defaults(func=cmd_share)

    mkdir_p = sub.add_parser("mkdir", help="Create a Drive folder")
    mkdir_p.add_argument("--title", required=True)
    mkdir_p.add_argument("--parent", metavar="ID", help="Parent folder id or URL")
    add_open_flag(mkdir_p)
    mkdir_p.set_defaults(func=cmd_mkdir)

    move_p = sub.add_parser("move", help="Move a file into a folder")
    move_p.add_argument("target", help="File URL or id")
    move_p.add_argument("--folder", required=True, help="Destination folder id or URL")
    move_p.set_defaults(func=cmd_move)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

"""Command line: print the slug of every title in a list of titles.

Run as ``python -m slugkit`` with a file of titles, one per line. Blank lines
are skipped and one slug is printed per remaining line, in file order. With no
file argument, or with ``-``, titles are read from standard input.
"""

import argparse
import sys
from pathlib import Path

from .errors import SlugError
from .slug import slugify


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m slugkit",
        description="Print the slug of every non-blank line of a file of titles.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="file of titles, one per line ('-' or no argument: standard input)",
    )
    parser.add_argument(
        "--sep",
        default="-",
        help="separator between the words of each slug (default: '-')",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=None,
        metavar="N",
        help="cut each slug to at most N characters",
    )
    parser.add_argument(
        "--prefix",
        default="",
        metavar="PREFIX",
        help="text put in front of every printed slug",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Slug every non-blank line of the titles file and return the exit status."""
    parser = _parser()
    args = parser.parse_args(argv)
    if args.max_length is not None and args.max_length < 1:
        parser.error(f"--max-length must be at least 1, got {args.max_length}")
    try:
        if args.file == "-":
            titles = sys.stdin.read().splitlines()
        else:
            titles = Path(args.file).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"slugkit: {exc}", file=sys.stderr)
        return 1
    for title in titles:
        if not title.strip():
            continue
        try:
            slug = slugify(title, sep=args.sep, max_length=args.max_length)
        except SlugError as exc:
            print(f"slugkit: {exc}", file=sys.stderr)
            return 1
        print(f"{args.prefix}{slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

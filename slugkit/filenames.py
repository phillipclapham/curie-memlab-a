"""Build safe file names from document titles."""

import re

from .errors import SlugError
from .slug import slugify

__all__ = ["filename_slug"]

_EXT_PATTERN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def filename_slug(title: str, ext: str) -> str:
    """Return a safe file name built from a document ``title`` and ``ext``.

    The title is turned into a lowercase ASCII slug, at most 100 characters,
    with runs of anything that is not a letter or digit collapsed into one
    hyphen and leading and trailing hyphens removed. A title with no letters
    or digits gives the base name ``untitled``.

    ``ext`` may be given with or without a leading dot and is lowercased. It
    must contain only letters and digits after the optional dot; an empty
    extension or one with any other character is rejected.

    Raises ``SlugError`` if ``ext`` is invalid.
    """
    stripped = ext[1:] if ext.startswith(".") else ext
    if not stripped or not _EXT_PATTERN.fullmatch(stripped):
        raise SlugError(f"invalid extension: {ext!r}")
    base = slugify(title, max_length=100)
    if not base:
        base = "untitled"
    return f"{base}.{stripped.lower()}"

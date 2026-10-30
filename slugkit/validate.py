"""Check that a string is already a well-formed slug."""

import re
from collections.abc import Iterable

from .errors import SlugError

__all__ = ["validate_slug"]


def validate_slug(slug: str, sep: str = "-", reserved: Iterable[str] = ()) -> str:
    """Return ``slug`` unchanged if it is a well-formed slug, else raise ``SlugError``.

    A well-formed slug is one or more groups of lowercase ASCII letters and
    digits joined by single ``sep`` characters: no uppercase, no spaces or
    other characters, no empty groups, and no leading or trailing separator.
    ``reserved`` lists slugs that are refused even when well formed; they are
    compared exactly, so ``"Admin"`` does not match a reserved ``"admin"``
    (it fails the lowercase rule anyway).

    ``validate_slug("hello-world")`` is ``"hello-world"``; ``"Hello World"``,
    ``"-hello"`` and ``"a--b"`` are rejected.

    Raises ``SlugError`` if ``sep`` is empty or contains a letter or digit.
    """
    if not sep or any(char.isascii() and char.isalnum() for char in sep):
        raise SlugError(f"sep must be non-empty and free of letters and digits, got {sep!r}")
    pattern = re.compile(rf"[a-z0-9]+(?:{re.escape(sep)}[a-z0-9]+)*")
    if not pattern.fullmatch(slug):
        raise SlugError(f"not a well-formed slug: {slug!r}")
    if slug in set(reserved):
        raise SlugError(f"reserved slug: {slug!r}")
    return slug

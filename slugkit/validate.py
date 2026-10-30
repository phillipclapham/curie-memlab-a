"""Refuse slugs that are not safe to put in a URL."""

import re

from .errors import SlugError

__all__ = ["validate_slug"]

_PART = re.compile(r"[a-z0-9]+")


def validate_slug(slug: str, sep: str = "-", reserved=()) -> str:
    """Return ``slug`` if it is well formed and not reserved, else raise ``SlugError``.

    A well formed slug is one or more non-empty parts of ``a-z0-9`` joined by
    ``sep``, so it holds only ``a-z``, ``0-9`` and the separator, and the
    separator never leads, trails or doubles. ``validate_slug("hello-world")``
    is ``"hello-world"``; ``validate_slug("café")`` raises ``SlugError``.

    ``sep`` sets the separator, so ``validate_slug("hello_world", sep="_")``
    passes while ``validate_slug("hello-world", sep="_")`` is refused.

    ``reserved`` is a collection of slugs refused even when well formed,
    compared exactly: with ``reserved={"admin", "api"}``, ``"admin"`` is
    refused but ``"adminx"`` is not.

    Raises ``SlugError`` if ``slug`` is not well formed or is reserved.
    """
    parts = slug.split(sep) if sep else [slug]
    for part in parts:
        if not _PART.fullmatch(part):
            raise SlugError(f"{slug!r} is not a valid slug")
    if slug in reserved:
        raise SlugError(f"{slug!r} is reserved")
    return slug

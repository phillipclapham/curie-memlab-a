"""Turn arbitrary text into URL slugs."""

import re
import unicodedata

from .errors import SlugError

__all__ = ["slugify"]

_NON_WORD = re.compile(r"[^a-z0-9]+")


def _truncate(slug: str, sep: str, max_length: int) -> str:
    """Cut ``slug`` to ``max_length`` characters, preferring a separator boundary."""
    if len(slug) <= max_length:
        return slug
    cut = slug[:max_length]
    if not slug.startswith(sep, max_length):
        boundary = cut.rfind(sep) if sep else -1
        if boundary > 0:
            cut = cut[:boundary]
    return cut.strip(sep)


def slugify(text: str, sep: str = "-", max_length: int | None = None) -> str:
    """Return a lowercase ASCII slug for ``text``.

    Accented letters are folded to their ASCII base ("Café" -> "cafe").
    Runs of anything that is not a letter or digit become one ``sep``.
    Leading and trailing separators are removed.

    If ``max_length`` is given, a longer slug is cut to at most that many
    characters, at the last separator that fits so that no word is split
    (a single word longer than the limit is cut at the limit).

    Raises ``SlugError`` if ``max_length`` is less than 1.
    """
    if max_length is not None and max_length < 1:
        raise SlugError(f"max_length must be at least 1, got {max_length}")
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = _NON_WORD.sub(sep, folded.lower()).strip(sep)
    if max_length is not None:
        slug = _truncate(slug, sep, max_length)
    return slug

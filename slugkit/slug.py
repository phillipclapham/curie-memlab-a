"""Turn arbitrary text into URL slugs."""

import re
import unicodedata

from .errors import SlugError

__all__ = ["slugify"]

_NON_WORD = re.compile(r"[^a-z0-9]+")


def slugify(text: str, sep: str = "-", max_length: int | None = None) -> str:
    """Return a lowercase ASCII slug for ``text``.

    Accented letters are folded to their ASCII base ("Café" -> "cafe").
    Runs of anything that is not a letter or digit become one ``sep``.
    Leading and trailing separators are removed.

    When ``max_length`` is given, the slug is cut to at most that many
    characters: at the last ``sep`` that fits so no word is split, or, for
    a single word longer than the limit, exactly at ``max_length``. A cut
    slug never ends in ``sep``. ``max_length`` below 1 raises ``SlugError``.
    """
    if max_length is not None and max_length < 1:
        raise SlugError("max_length must be at least 1")
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = _NON_WORD.sub(sep, folded.lower())
    slug = slug.strip(sep)
    if max_length is not None:
        slug = _truncate(slug, sep, max_length)
    return slug


def _truncate(slug: str, sep: str, max_length: int) -> str:
    """Cut ``slug`` to at most ``max_length`` characters.

    Prefer cutting at the last ``sep`` that fits so no word is split;
    a single word longer than the limit is cut at the limit. The
    result never ends in ``sep``.
    """
    if len(slug) <= max_length:
        return slug
    cut = slug[:max_length]
    idx = cut.rfind(sep)
    if idx == -1:
        return cut
    return cut[:idx].rstrip(sep)

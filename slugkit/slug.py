"""Turn arbitrary text into URL slugs."""

import re
import unicodedata
from collections.abc import Collection

from .errors import SlugError

__all__ = ["slugify"]

_NON_WORD = re.compile(r"[^a-z0-9]+")

_BUILTIN_STOPWORDS = frozenset(
    {"a", "an", "and", "for", "in", "of", "on", "the", "to"}
)


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


def slugify(
    text: str,
    sep: str = "-",
    max_length: int | None = None,
    stopwords: bool | Collection[str] | None = None,
) -> str:
    """Return a lowercase ASCII slug for ``text``.

    Accented letters are folded to their ASCII base ("Café" -> "cafe").
    Runs of anything that is not a letter or digit become one ``sep``.
    Leading and trailing separators are removed.

    If ``max_length`` is given, a longer slug is cut to at most that many
    characters, at the last separator that fits so that no word is split
    (a single word longer than the limit is cut at the limit).

    ``stopwords`` drops filler words from the slug. ``True`` selects the
    built-in list (a, an, and, for, in, of, on, the, to); any other
    collection of words filters those words, matched ignoring case. Words
    are matched after lowercasing, so ``{"FOR"}`` drops "for". Text whose
    every word is a stopword keeps its words: ``slugify("The",
    stopwords=True)`` returns ``"the"``. ``False`` and ``None`` leave the
    slug untouched.

    Raises ``SlugError`` if ``max_length`` is less than 1, or if
    ``stopwords`` is a bare string (a string is a collection of characters,
    not words).
    """
    if max_length is not None and max_length < 1:
        raise SlugError(f"max_length must be at least 1, got {max_length}")
    if isinstance(stopwords, str):
        raise SlugError(
            "stopwords must be True, a collection of words, or None/False, "
            "not a bare string"
        )
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower()
    if stopwords is not None and stopwords is not False:
        if stopwords is True:
            stop = _BUILTIN_STOPWORDS
        else:
            stop = {w.lower() for w in stopwords}
        words = [w for w in _NON_WORD.split(lowered) if w and w not in stop]
        if words:
            slug = sep.join(words)
        else:
            slug = _NON_WORD.sub(sep, lowered).strip(sep)
    else:
        slug = _NON_WORD.sub(sep, lowered).strip(sep)
    if max_length is not None:
        slug = _truncate(slug, sep, max_length)
    return slug

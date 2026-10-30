"""Turn arbitrary text into URL slugs."""

import re
import unicodedata
from collections.abc import Iterable, Mapping

from .errors import SlugError

__all__ = ["slugify"]

_NON_WORD = re.compile(r"[^a-z0-9]+")

_BUILTIN_STOPWORDS = frozenset({"a", "an", "and", "for", "in", "of", "on", "the", "to"})


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


def _apply_aliases(text: str, aliases: Mapping[str, str]) -> str:
    """Replace each alias source in ``text`` with its replacement, longest source first."""
    lookup = {}
    for source, replacement in aliases.items():
        if not source:
            raise SlugError("an alias needs a non-empty source")
        lookup[source.lower()] = replacement
    pattern = re.compile("|".join(re.escape(s) for s in sorted(lookup, key=len, reverse=True)), re.IGNORECASE)
    return pattern.sub(lambda match: f" {lookup[match.group(0).lower()]} ", text)


def slugify(
    text: str,
    sep: str = "-",
    max_length: int | None = None,
    stopwords: bool | Iterable[str] | None = None,
    aliases: Mapping[str, str] | None = None,
) -> str:
    """Return a lowercase ASCII slug for ``text``.

    Accented letters are folded to their ASCII base ("Café" -> "cafe").
    Runs of anything that is not a letter or digit become one ``sep``.
    Leading and trailing separators are removed.

    If ``max_length`` is given, a longer slug is cut to at most that many
    characters, at the last separator that fits so that no word is split
    (a single word longer than the limit is cut at the limit).

    ``stopwords`` leaves filler words out of the slug. ``True`` uses the
    built-in list (a, an, and, for, in, of, on, the, to); any collection of
    words uses those instead, ignoring case. A text made only of stopwords
    keeps its words rather than becoming empty.

    ``aliases`` maps text to its spoken form before anything else happens
    (``{"c++": "cpp", "&": "and"}`` turns "C++ & Rust" into ``cpp-and-rust``).
    Sources match ignoring case and the longest source wins where they overlap.

    Raises ``SlugError`` if ``max_length`` is less than 1 or an alias has an
    empty source.
    """
    if max_length is not None and max_length < 1:
        raise SlugError(f"max_length must be at least 1, got {max_length}")
    if aliases:
        text = _apply_aliases(text, aliases)
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    words = [word for word in _NON_WORD.split(folded.lower()) if word]
    if stopwords:
        skip = _BUILTIN_STOPWORDS if stopwords is True else {word.lower() for word in stopwords}
        words = [word for word in words if word not in skip] or words
    slug = sep.join(words)
    if max_length is not None:
        slug = _truncate(slug, sep, max_length)
    return slug

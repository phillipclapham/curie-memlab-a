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

    ``aliases`` spells out symbols before slugifying: each source is replaced
    by its replacement wherever it appears in the text. Matching ignores
    case, and the longest source wins when sources overlap ("C++ & Rust"
    with ``{"c++": "cpp", "&": "and"}`` gives "cpp-and-rust").

    Raises ``SlugError`` if ``max_length`` is less than 1.
    """
    if max_length is not None and max_length < 1:
        raise SlugError(f"max_length must be at least 1, got {max_length}")
    lowered = text.lower()
    if aliases:
        replacements = {source.lower(): replacement for source, replacement in aliases.items()}
        pattern = re.compile(
            "|".join(re.escape(source) for source in sorted(replacements, key=len, reverse=True)),
            re.IGNORECASE,
        )
        lowered = pattern.sub(lambda match: replacements[match.group(0).lower()], lowered)
    folded = unicodedata.normalize("NFKD", lowered).encode("ascii", "ignore").decode("ascii")
    words = [word for word in _NON_WORD.split(folded.lower()) if word]
    if stopwords:
        skip = _BUILTIN_STOPWORDS if stopwords is True else {word.lower() for word in stopwords}
        words = [word for word in words if word not in skip] or words
    slug = sep.join(words)
    if max_length is not None:
        slug = _truncate(slug, sep, max_length)
    return slug

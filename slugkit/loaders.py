"""Read stopword lists from files."""

from .errors import SlugError

__all__ = ["load_stopwords"]


def load_stopwords(path) -> frozenset[str]:
    """Return a ``frozenset`` of the lowercased words in a stopword file.

    The file holds one word per line. Blank lines and lines that start
    with ``#`` are skipped. A line that holds more than one word is
    rejected with ``SlugError``.

    The returned set can be passed straight to ``slugify(stopwords=...)``.
    """
    words: set[str] = set()
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split()
            if len(parts) > 1:
                raise SlugError(
                    f"stopword file {path}: line holds more than one word: {stripped!r}"
                )
            words.add(parts[0].lower())
    return frozenset(words)

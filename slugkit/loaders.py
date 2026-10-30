"""Read word lists and rules from small text files."""

from pathlib import Path

from .errors import SlugError

__all__ = ["load_aliases", "load_stopwords"]


def _data_lines(path) -> list[tuple[int, str]]:
    """Return ``(line number, text)`` for each line that is not blank or a ``#`` comment.

    Raises ``OSError`` if the file cannot be read and ``SlugError`` if it is not UTF-8 text.
    """
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SlugError(f"{path}: not valid UTF-8 text") from exc
    lines = []
    for number, line in enumerate(raw.splitlines(), start=1):
        text = line.strip()
        if text and not text.startswith("#"):
            lines.append((number, text))
    return lines


def load_stopwords(path) -> frozenset[str]:
    """Return the lowercased words in a stopword file, one word per line.

    Blank lines and lines starting with ``#`` are skipped. The result can be
    passed to ``slugify(stopwords=...)``.

    Raises ``OSError`` if the file is missing or unreadable, and ``SlugError``
    if it is not UTF-8 text or a line holds more than one word.
    """
    words = set()
    for number, text in _data_lines(path):
        if len(text.split()) != 1:
            raise SlugError(f"{path}:{number}: expected one word per line, got {text!r}")
        words.add(text.lower())
    return frozenset(words)


def load_aliases(path) -> dict[str, str]:
    """Return the alias rules in an alias file, one ``source = replacement`` per line.

    Blank lines and lines starting with ``#`` are skipped. The source is
    trimmed and lowercased and the replacement is trimmed; everything after
    the first ``=`` is the replacement. The result can be passed to
    ``slugify(aliases=...)``.

    Raises ``OSError`` if the file is missing or unreadable, and ``SlugError``
    if it is not UTF-8 text, a line has no ``=``, or its source is empty.
    """
    aliases = {}
    for number, text in _data_lines(path):
        source, sep, replacement = text.partition("=")
        if not sep:
            raise SlugError(f"{path}:{number}: expected 'source = replacement', got {text!r}")
        source = source.strip().lower()
        if not source:
            raise SlugError(f"{path}:{number}: empty alias source in {text!r}")
        aliases[source] = replacement.strip()
    return aliases

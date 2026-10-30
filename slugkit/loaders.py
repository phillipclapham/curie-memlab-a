"""Read word lists and rules from small text files."""

import re
from pathlib import Path

from .errors import SlugError

__all__ = ["load_aliases", "load_redaction_patterns", "load_stopwords"]


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
    """Return the ``source = replacement`` rules in an alias file.

    One rule per line, split at the first ``=`` with the whitespace around
    each side trimmed; sources are lowercased, and a later rule for the same
    source replaces an earlier one. Blank lines and lines starting with ``#``
    are skipped. The result can be passed to ``slugify(aliases=...)``.

    Raises ``OSError`` if the file is missing or unreadable, and ``SlugError``
    if it is not UTF-8 text or a rule has no ``=`` or an empty source.
    """
    aliases = {}
    for number, text in _data_lines(path):
        source, equals, replacement = text.partition("=")
        source = source.strip().lower()
        if not equals or not source:
            raise SlugError(f"{path}:{number}: expected 'source = replacement', got {text!r}")
        aliases[source] = replacement.strip()
    return aliases


def load_redaction_patterns(path) -> list[str]:
    """Return the redaction patterns in a pattern file, one pattern per line.

    Whitespace around each line is trimmed; blank lines and lines starting
    with ``#`` are skipped. The result can be passed to
    ``slugify(redact=...)``.

    Raises ``OSError`` if the file is missing or unreadable, and ``SlugError``
    if it is not UTF-8 text or a line is not a valid regular expression.
    """
    patterns = []
    for number, text in _data_lines(path):
        try:
            re.compile(text)
        except re.error as exc:
            raise SlugError(f"{path}:{number}: not a valid regular expression: {text!r}") from exc
        patterns.append(text)
    return patterns

"""File names built from titles."""

from .errors import SlugError
from .slug import slugify

__all__ = ["filename_slug"]

_MAX_STEM_LENGTH = 100


def filename_slug(title: str, ext: str) -> str:
    """Return a file name for ``title`` with extension ``ext``.

    The name is the slug of the title, cut to 100 characters, followed by a dot
    and the lowercased extension; ``ext`` may be given with or without its
    leading dot. A title with no letters or digits becomes ``"untitled"``.
    Because the stem holds only lowercase ASCII letters, digits and ``-`` and
    the extension only letters and digits, the result never contains a path
    separator or a ``..`` component.

    ``filename_slug("Q3 Report: Final!", "PDF")`` is ``"q3-report-final.pdf"``.

    Raises ``SlugError`` if the extension is empty or holds anything other
    than ASCII letters and digits.
    """
    suffix = ext[1:] if ext.startswith(".") else ext
    if not (suffix.isascii() and suffix.isalnum()):
        raise SlugError(f"extension must be letters and digits only, got {ext!r}")
    stem = slugify(title, max_length=_MAX_STEM_LENGTH) or "untitled"
    return f"{stem}.{suffix.lower()}"

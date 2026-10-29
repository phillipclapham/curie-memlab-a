"""Remember the slugs a registry has handed out so none is issued twice."""

from .errors import SlugError
from .slug import slugify

__all__ = ["SlugRegistry"]


class SlugRegistry:
    """Hand out slugs and never return the same one twice.

    Two posts titled alike must not end up with the same URL, so every
    claim is compared by its slug: when a slug is already taken, the
    registry appends a counter (``2``, ``3``, ...) until it finds one that
    has never been handed out. Text that has no letters or digits has no
    slug and cannot be claimed.
    """

    def __init__(self, sep: str = "-"):
        self._sep = sep
        self._issued: set[str] = set()

    def claim(self, text: str) -> str:
        """Return a unique slug for ``text``, remembering it as taken.

        Text is compared by its slug, not as typed, so ``claim("Hello
        World")`` and ``claim("Hello, World!")`` share a base slug.

        Raises ``SlugError`` for text that has no letters or digits.
        """
        base = slugify(text, sep=self._sep)
        if not base:
            raise SlugError(
                f"cannot claim a slug for text without letters or digits: {text!r}"
            )
        candidate = base
        counter = 2
        while candidate in self._issued:
            candidate = f"{base}{self._sep}{counter}"
            counter += 1
        self._issued.add(candidate)
        return candidate

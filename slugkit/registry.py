"""Hand out slugs that are never repeated."""

from .errors import SlugError
from .slug import slugify

__all__ = ["SlugRegistry"]


class SlugRegistry:
    """Hand out unique slugs.

    The first claim for a slug returns it unchanged; later claims for the
    same slug get a numeric suffix (``hello-world``, ``hello-world-2``,
    ``hello-world-3``). A slug that has been handed out, suffixed or not, is
    never returned again.
    """

    def __init__(self, sep: str = "-") -> None:
        self._sep = sep
        self._used: set[str] = set()

    def claim(self, text: str) -> str:
        """Return a slug for ``text`` that this registry has not handed out before.

        Raises ``SlugError`` if ``text`` contains no letters or digits.
        """
        slug = slugify(text, sep=self._sep)
        if not slug:
            raise SlugError(f"cannot make a slug from {text!r}: it has no letters or digits")
        candidate, number = slug, 1
        while candidate in self._used:
            number += 1
            candidate = f"{slug}{self._sep}{number}"
        self._used.add(candidate)
        return candidate

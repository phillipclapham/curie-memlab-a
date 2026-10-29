"""Turn an email address into a slug for profile URLs."""

from .errors import SlugError
from .slug import slugify

__all__ = ["slug_from_email"]


def slug_from_email(address: str, sep: str = "-") -> str:
    """Return a slug built from the local part of ``address``.

    Everything before the ``@`` is turned into a slug the same way
    :func:`slugify` turns text into one, so ``"jane.doe@example.com"``
    becomes ``"jane-doe"``. A ``+tag`` suffix on the local part is dropped,
    so ``"Jane.Doe+news@example.com"`` also becomes ``"jane-doe"``. The
    domain is ignored.

    Raises ``SlugError`` if ``address`` is not of the form ``local@domain``
    (no ``@``, more than one ``@``, or an empty local part or domain), or if
    the local part turns into no slug at all (for example ``"+tag@example.com"``).
    """
    local, at, domain = address.rpartition("@")
    if not at or local == "" or domain == "" or "@" in local:
        raise SlugError(f"not a valid email address: {address!r}")
    slug = slugify(local.partition("+")[0], sep=sep)
    if not slug:
        raise SlugError(f"cannot make a slug from {address!r}: its local part has no letters or digits")
    return slug

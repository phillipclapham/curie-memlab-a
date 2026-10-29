"""Slugs derived from email addresses."""

from .errors import SlugError
from .slug import slugify

__all__ = ["slug_from_email"]


def slug_from_email(address: str, sep: str = "-") -> str:
    """Return a slug built from the local part of an email address.

    The part before the ``@`` is slugified, and a ``+tag`` suffix is dropped:
    ``slug_from_email("Jane.Doe+news@example.com")`` is ``"jane-doe"``.

    Raises ``SlugError`` if ``address`` is not of the form ``local@domain``
    (exactly one ``@``, with something on each side) or if nothing is left of
    the local part once the tag is dropped.
    """
    local, at, domain = address.partition("@")
    if not at or not local or not domain or "@" in domain:
        raise SlugError(f"not an email address of the form local@domain: {address!r}")
    slug = slugify(local.split("+", 1)[0], sep=sep)
    if not slug:
        raise SlugError(f"no usable name before the @ in {address!r}")
    return slug

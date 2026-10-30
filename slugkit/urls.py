"""Slugs derived from web addresses."""

from urllib.parse import urlsplit

from .errors import SlugError
from .slug import slugify

__all__ = ["slug_from_url"]


def slug_from_url(url: str, sep: str = "-") -> str:
    """Return a slug built from the host and path of an ``http`` or ``https`` URL.

    A leading ``www.`` on the host is dropped, and the port, query string and
    fragment are ignored:
    ``slug_from_url("https://www.example.com/blog/Hello_World/")`` is
    ``"example-com-blog-hello-world"``.

    Raises ``SlugError`` if the URL has no ``http`` or ``https`` scheme, has no
    host, cannot be parsed, or leaves nothing to build a slug from.
    """
    try:
        parts = urlsplit(url)
        host = parts.hostname
    except ValueError as exc:
        raise SlugError(f"not a valid URL: {url!r}") from exc
    if parts.scheme.lower() not in ("http", "https") or not host:
        raise SlugError(f"expected an http or https URL with a host, got {url!r}")
    if host.startswith("www."):
        host = host[len("www."):]
    slug = slugify(f"{host} {parts.path}", sep=sep)
    if not slug:
        raise SlugError(f"nothing to build a slug from in {url!r}")
    return slug

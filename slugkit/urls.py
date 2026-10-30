"""Slugs derived from URLs."""

from urllib.parse import urlsplit

from .errors import SlugError
from .slug import slugify

__all__ = ["slug_from_url"]


def slug_from_url(url: str, sep: str = "-") -> str:
    """Return a slug built from a URL's host and path.

    A leading ``www.`` on the host is dropped, and the port, the query
    string and the fragment are ignored:
    ``slug_from_url("https://www.example.com/blog/Hello_World/")`` is
    ``"example-com-blog-hello-world"``.

    Raises ``SlugError`` unless ``url`` is an ``http`` or ``https`` URL
    with a host.
    """
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise SlugError(f"not an http or https URL: {url!r}")
    host = parts.hostname
    if not host:
        raise SlugError(f"URL has no host: {url!r}")
    if host.startswith("www."):
        host = host[4:]
    slug = slugify(host + parts.path, sep=sep)
    if not slug:
        raise SlugError(f"no usable host or path in {url!r}")
    return slug

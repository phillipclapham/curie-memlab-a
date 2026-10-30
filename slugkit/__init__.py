from .addresses import slug_from_email
from .errors import SlugError
from .filenames import filename_slug
from .loaders import load_aliases, load_stopwords
from .registry import SlugRegistry
from .slug import slugify

__all__ = [
    "SlugError",
    "SlugRegistry",
    "filename_slug",
    "load_aliases",
    "load_stopwords",
    "slug_from_email",
    "slugify",
]

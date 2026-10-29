"""Errors raised by slugkit."""

__all__ = ["SlugError"]


class SlugError(ValueError):
    """Raised when slugkit is given input it cannot turn into a valid slug."""

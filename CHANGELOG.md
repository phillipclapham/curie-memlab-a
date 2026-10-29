# Changelog

## Unreleased

- Add `SlugError`, the library's own error type (a `ValueError` subclass).
- `slugify` takes `max_length` to cap the slug, cutting at a separator so no word is split; a limit below 1 raises `SlugError`.
- Add `SlugRegistry` (`slugkit/registry.py`), which hands out unique slugs by suffixing repeats with a counter; text with no letters or digits raises `SlugError`.
- Add `slug_from_email` (`slugkit/addresses.py`): the local part of an address as a slug, `+tag` dropped; a malformed address raises `SlugError`.

## 0.1.0

- Initial release: `slugify`.

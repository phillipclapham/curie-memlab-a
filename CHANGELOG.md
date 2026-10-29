# Changelog

## Unreleased

- Add `SlugError`, the library's own error type (a `ValueError` subclass).
- `slugify` takes `max_length` to cap the slug, cutting at a separator so no word is split; a limit below 1 raises `SlugError`.

## 0.1.0

- Initial release: `slugify`.

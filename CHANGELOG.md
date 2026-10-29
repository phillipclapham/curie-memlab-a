# Changelog

## Unreleased

- Add `SlugError`, the library's own error type (a `ValueError` subclass).
- Add a `max_length` option to `slugify`: caps the slug at the last separator that fits (or exactly at the limit for one long word); values below 1 raise `SlugError`.

## 0.1.0

- Initial release: `slugify`.

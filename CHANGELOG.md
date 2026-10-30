# Changelog

## Unreleased

- Add `SlugError`, the library's own error type (a `ValueError` subclass).
- `slugify` takes `max_length` to cap the slug, cutting at a separator so no word is split; a limit below 1 raises `SlugError`.
- Add `SlugRegistry` (`slugkit/registry.py`), which hands out unique slugs by suffixing repeats with a counter; text with no letters or digits raises `SlugError`.
- Add `slug_from_email` (`slugkit/addresses.py`): the local part of an address as a slug, `+tag` dropped; a malformed address raises `SlugError`.
- Add a `stopwords` option to `slugify`: `True` selects the built-in filler-word list (a, an, and, for, in, of, on, the, to), and any collection of words filters those words ignoring case; text made only of stopwords keeps its words, and a bare string raises `SlugError`.
- Add `load_stopwords` (`slugkit/loaders.py`): read a stopword file, one word per line, skipping blank lines and `#` lines; a line with more than one word raises `SlugError`, and the returned `frozenset` passes straight to `slugify(stopwords=...)`.

## 0.1.0

- Initial release: `slugify`.

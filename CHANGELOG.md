# Changelog

## Unreleased

- Add `SlugError`, the library's own error type (a `ValueError` subclass).
- `slugify` takes `max_length` to cap the slug, cutting at a separator so no word is split; a limit below 1 raises `SlugError`.
- Add `SlugRegistry` (`slugkit/registry.py`), which hands out unique slugs by suffixing repeats with a counter; text with no letters or digits raises `SlugError`.
- Add `slug_from_email` (`slugkit/addresses.py`): the local part of an address as a slug, `+tag` dropped; a malformed address raises `SlugError`.
- `slugify` takes `stopwords` to leave filler words out (`True` for the built-in list, or your own collection).
- Add `load_stopwords` (`slugkit/loaders.py`), which reads a stopword file; a missing file raises `OSError` and a malformed one raises `SlugError`.
- Add `filename_slug` (`slugkit/filenames.py`): a file name from a title and extension, stem cut to 100 characters, `untitled` for an empty title; an extension that is not letters and digits raises `SlugError`.
- `slugify` takes `aliases` to replace text such as `c++` with its spoken form before slugging (case-insensitive, longest source wins).
- Add `load_aliases` (`slugkit/loaders.py`), which reads `source = replacement` rules from a file; a missing file raises `OSError` and a malformed rule raises `SlugError`.
- Add `validate_slug` (`slugkit/validate.py`), which returns a well-formed slug and raises `SlugError` for a malformed or reserved one.
- `slugify` takes `redact`, a list of regular expressions; every match is replaced by the word `redacted` before the text is slugged (matched case-sensitively, applied in the order given).
- Add `load_redaction_patterns` (`slugkit/loaders.py`), which reads one pattern per line from a file; a missing file raises `OSError`, and a line that is not a valid regular expression raises `SlugError`.
- Add `slug_from_url` (`slugkit/urls.py`): a slug from the host and path of an `http` or `https` URL; any other URL raises `SlugError`.

## 0.1.0

- Initial release: `slugify`.

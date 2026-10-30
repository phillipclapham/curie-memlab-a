import tempfile
import unittest
from pathlib import Path

from slugkit import SlugError, slugify
from slugkit.loaders import load_aliases, load_redaction_patterns, load_stopwords


class LoadStopwordsTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.dir = Path(self._dir.name)

    def write(self, name, text, encoding="utf-8"):
        path = self.dir / name
        path.write_bytes(text.encode(encoding) if isinstance(text, str) else text)
        return path

    def test_valid_file_gives_lowercased_words(self):
        path = self.write("stop.txt", "# filler words\nThe\n\n  of  \nAND\n")
        self.assertEqual(load_stopwords(path), frozenset({"the", "of", "and"}))

    def test_result_feeds_slugify(self):
        path = self.write("stop.txt", "the\nof\n")
        self.assertEqual(slugify("The Lord of the Rings", stopwords=load_stopwords(path)), "lord-rings")

    def test_a_line_with_two_words_is_rejected(self):
        path = self.write("stop.txt", "the\nout of\n")
        with self.assertRaises(SlugError):
            load_stopwords(path)

    def test_missing_file_is_an_error_not_an_empty_set(self):
        with self.assertRaises(OSError):
            load_stopwords(self.dir / "missing.txt")

    def test_file_that_is_not_text_is_rejected(self):
        path = self.write("stop.txt", b"\xff\xfe\x00bad")
        with self.assertRaises(SlugError):
            load_stopwords(path)


class LoadAliasesTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.dir = Path(self._dir.name)

    def write(self, text):
        path = self.dir / "aliases.txt"
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def test_valid_file_gives_lowercased_sources(self):
        path = self.write("# spoken forms\nC++ = cpp\n\n&=and\n@ = at = home\n")
        self.assertEqual(load_aliases(path), {"c++": "cpp", "&": "and", "@": "at = home"})

    def test_later_rule_for_a_source_wins(self):
        path = self.write("c++ = cpp\nC++ = cxx\n")
        self.assertEqual(load_aliases(path), {"c++": "cxx"})

    def test_result_feeds_slugify(self):
        path = self.write("c++ = cpp\n& = and\n")
        self.assertEqual(slugify("C++ & Rust", aliases=load_aliases(path)), "cpp-and-rust")

    def test_malformed_rules_are_rejected(self):
        for bad in ("c++ cpp\n", " = cpp\n", "c++ = cpp\njust words\n"):
            with self.subTest(content=bad):
                with self.assertRaises(SlugError):
                    load_aliases(self.write(bad))

    def test_missing_file_is_an_error_not_an_empty_mapping(self):
        with self.assertRaises(OSError):
            load_aliases(self.dir / "missing.txt")

    def test_file_that_is_not_text_is_rejected(self):
        with self.assertRaises(SlugError):
            load_aliases(self.write(b"\xff\xfe\x00bad"))


class LoadRedactionPatternsTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.dir = Path(self._dir.name)

    def write(self, text):
        path = self.dir / "redact.txt"
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def test_valid_file_gives_patterns_in_order(self):
        path = self.write("# secrets\nEXAMPLE-KEY-[0-9]+\n\n  user@example\\.com  \n")
        self.assertEqual(load_redaction_patterns(path), ["EXAMPLE-KEY-[0-9]+", "user@example\\.com"])

    def test_result_feeds_slugify(self):
        path = self.write("EXAMPLE-KEY-[0-9]+\n")
        self.assertEqual(slugify("Key EXAMPLE-KEY-99 rotated", redact=load_redaction_patterns(path)), "key-redacted-rotated")

    def test_an_invalid_pattern_is_rejected(self):
        with self.assertRaises(SlugError):
            load_redaction_patterns(self.write("EXAMPLE-KEY-[0-9]+\n(unclosed\n"))

    def test_a_pattern_matching_nothing_at_all_is_rejected(self):
        with self.assertRaises(SlugError):
            load_redaction_patterns(self.write("x*\n"))

    def test_missing_file_is_an_error_not_an_empty_list(self):
        with self.assertRaises(OSError):
            load_redaction_patterns(self.dir / "missing.txt")

    def test_file_that_is_not_text_is_rejected(self):
        with self.assertRaises(SlugError):
            load_redaction_patterns(self.write(b"\xff\xfe\x00bad"))


if __name__ == "__main__":
    unittest.main()

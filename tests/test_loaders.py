import tempfile
import unittest
from pathlib import Path

from slugkit import SlugError, slugify
from slugkit.loaders import load_stopwords


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


if __name__ == "__main__":
    unittest.main()

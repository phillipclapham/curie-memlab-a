import tempfile
import unittest
from pathlib import Path

from slugkit import SlugError, load_stopwords, slugify


class LoadStopwordsTest(unittest.TestCase):
    def write_file(self, text: str) -> Path:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        ) as handle:
            handle.write(text)
            return Path(handle.name)

    def test_lowercased_words_skipping_blanks_and_comments(self):
        path = self.write_file("The\n\n# a comment\nOF\n# another comment\n  to  \n")
        stops = load_stopwords(path)
        self.assertEqual(stops, frozenset({"the", "of", "to"}))
        self.assertIsInstance(stops, frozenset)

    def test_rejects_a_line_with_more_than_one_word(self):
        path = self.write_file("the\nquick brown\n")
        with self.assertRaises(SlugError):
            load_stopwords(path)

    def test_result_passes_straight_to_slugify(self):
        path = self.write_file("# filler words\nThe\nOF\n")
        stops = load_stopwords(path)
        self.assertEqual(slugify("The Art of War", stopwords=stops), "art-war")


if __name__ == "__main__":
    unittest.main()

import unittest

from slugkit import SlugError, slugify


class SlugErrorTest(unittest.TestCase):
    def test_is_a_value_error(self):
        with self.assertRaises(ValueError):
            raise SlugError("bad input")


class SlugifyTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_accents_fold_to_ascii(self):
        self.assertEqual(slugify("Café déjà vu"), "cafe-deja-vu")

    def test_runs_collapse(self):
        self.assertEqual(slugify("a  --  b"), "a-b")

    def test_custom_separator(self):
        self.assertEqual(slugify("Hello World", sep="_"), "hello_world")

    def test_max_length_keeps_short_slug(self):
        self.assertEqual(slugify("hello world", max_length=20), "hello-world")

    def test_max_length_cuts_at_separator(self):
        self.assertEqual(slugify("the quick brown fox", max_length=12), "the-quick")

    def test_max_length_cuts_long_word(self):
        self.assertEqual(slugify("extraordinary", max_length=5), "extra")

    def test_max_length_no_trailing_separator(self):
        self.assertEqual(slugify("ab cd", max_length=3), "ab")

    def test_max_length_below_one_raises(self):
        for bad in (0, -1):
            with self.assertRaises(SlugError):
                slugify("hello world", max_length=bad)


if __name__ == "__main__":
    unittest.main()

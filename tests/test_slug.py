import unittest

from slugkit import SlugError, slugify
from slugkit.slug import _BUILTIN_STOPWORDS


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


class MaxLengthTest(unittest.TestCase):
    def test_short_slug_is_unchanged(self):
        self.assertEqual(slugify("hello world", max_length=20), "hello-world")

    def test_cut_at_the_last_separator_that_fits(self):
        self.assertEqual(slugify("the quick brown fox", max_length=12), "the-quick")

    def test_cut_exactly_before_a_separator_keeps_the_word(self):
        self.assertEqual(slugify("the quick brown fox", max_length=9), "the-quick")

    def test_single_long_word_is_cut_at_the_limit(self):
        self.assertEqual(slugify("extraordinary", max_length=5), "extra")

    def test_cut_slug_never_ends_in_a_separator(self):
        self.assertEqual(slugify("ab cd", max_length=3), "ab")
        self.assertEqual(slugify("the quick brown fox", max_length=10), "the-quick")

    def test_custom_separator_is_respected(self):
        self.assertEqual(slugify("the quick brown", sep="_", max_length=12), "the_quick")

    def test_rejects_a_limit_below_one(self):
        for bad in (0, -1, -50):
            with self.subTest(max_length=bad):
                with self.assertRaises(SlugError):
                    slugify("hello world", max_length=bad)

    def test_a_limit_of_one_is_accepted(self):
        self.assertEqual(slugify("hello world", max_length=1), "h")


class StopwordsTest(unittest.TestCase):
    def test_true_selects_the_builtin_list(self):
        self.assertEqual(
            _BUILTIN_STOPWORDS,
            frozenset({"a", "an", "and", "for", "in", "of", "on", "the", "to"}),
        )
        self.assertEqual(slugify("The Art of War", stopwords=True), "art-war")
        for word in sorted(_BUILTIN_STOPWORDS):
            with self.subTest(word=word):
                self.assertEqual(
                    slugify(f"alpha {word} omega", stopwords=True), "alpha-omega"
                )
        self.assertEqual(slugify("art", stopwords=True), "art")

    def test_collection_is_matched_ignoring_case(self):
        self.assertEqual(slugify("Tea for Two", stopwords={"FOR"}), "tea-two")
        self.assertEqual(slugify("Tea for Two", stopwords={"for"}), "tea-two")
        self.assertEqual(slugify("Tea FOR Two", stopwords={"for"}), "tea-two")

    def test_text_of_only_stopwords_keeps_its_words(self):
        self.assertEqual(slugify("The", stopwords=True), "the")
        self.assertEqual(
            slugify("The of and", stopwords={"the", "of", "and"}), "the-of-and"
        )

    def test_filtering_composes_with_max_length(self):
        self.assertEqual(slugify("The Art of War", stopwords=True, max_length=7), "art-war")
        self.assertEqual(slugify("The Art of War", stopwords=True, max_length=3), "art")

    def test_a_bare_string_is_rejected(self):
        with self.assertRaises(SlugError):
            slugify("hello world", stopwords="the")

    def test_false_and_none_keep_the_default_behavior(self):
        self.assertEqual(slugify("The Art of War", stopwords=None), "the-art-of-war")
        self.assertEqual(slugify("The Art of War", stopwords=False), "the-art-of-war")


if __name__ == "__main__":
    unittest.main()

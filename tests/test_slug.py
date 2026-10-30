import re
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
    def test_builtin_list(self):
        self.assertEqual(slugify("The Art of War", stopwords=True), "art-war")

    def test_builtin_list_covers_every_listed_word(self):
        self.assertEqual(slugify("a an and for in of on the to word", stopwords=True), "word")

    def test_custom_collection_ignores_case(self):
        self.assertEqual(slugify("Tea for Two", stopwords={"FOR"}), "tea-two")

    def test_text_of_only_stopwords_keeps_its_words(self):
        self.assertEqual(slugify("The", stopwords=True), "the")
        self.assertEqual(slugify("The of", stopwords=True), "the-of")

    def test_off_by_default(self):
        self.assertEqual(slugify("The Art of War"), "the-art-of-war")

    def test_combines_with_max_length_and_separator(self):
        self.assertEqual(slugify("The Art of War and Peace", sep="_", max_length=9, stopwords=True), "art_war")


class AliasesTest(unittest.TestCase):
    def test_aliases_replace_text_before_slugging(self):
        self.assertEqual(slugify("C++ & Rust", aliases={"c++": "cpp", "&": "and"}), "cpp-and-rust")

    def test_matching_ignores_case_in_text_and_sources(self):
        self.assertEqual(slugify("NODE.JS rocks", aliases={"Node.JS": "nodejs"}), "nodejs-rocks")

    def test_longest_source_wins_where_aliases_overlap(self):
        aliases = {"c++": "cpp", "c++11": "cxx11"}
        self.assertEqual(slugify("c++11", aliases=aliases), "cxx11")
        self.assertEqual(slugify("c++ and c++11", aliases=aliases), "cpp-and-cxx11")

    def test_replacements_are_not_rewritten_again(self):
        self.assertEqual(slugify("a", aliases={"a": "b", "b": "c"}), "b")

    def test_no_aliases_leaves_text_alone(self):
        self.assertEqual(slugify("C++ & Rust"), "c-rust")

    def test_empty_source_is_rejected(self):
        with self.assertRaises(SlugError):
            slugify("anything", aliases={"": "x"})


class RedactTest(unittest.TestCase):
    def test_matches_are_replaced_with_the_word_redacted(self):
        self.assertEqual(
            slugify("Key EXAMPLE-KEY-1234 rotated", redact=[r"EXAMPLE-KEY-\d+"]),
            "key-redacted-rotated",
        )

    def test_several_patterns_apply_in_order(self):
        text = "Login for user@example.com with TOKEN-AAA"
        patterns = [r"TOKEN-[A-Z]+", r"[a-z.]+@example\.com"]
        self.assertEqual(slugify(text, redact=patterns), "login-for-redacted-with-redacted")

    def test_matching_is_case_sensitive_as_written(self):
        self.assertEqual(slugify("token-aaa", redact=[r"TOKEN-[A-Z]+"]), "token-aaa")

    def test_compiled_patterns_are_accepted(self):
        self.assertEqual(slugify("see EXAMPLE-KEY-7", redact=[re.compile("EXAMPLE-KEY-[0-9]+")]), "see-redacted")

    def test_text_with_no_match_is_unchanged(self):
        self.assertEqual(slugify("Hello World", redact=[r"EXAMPLE-KEY-\d+"]), "hello-world")

    def test_invalid_patterns_are_rejected(self):
        with self.assertRaises(SlugError):
            slugify("anything", redact=["(unclosed"])

    def test_a_pattern_that_matches_the_empty_string_is_rejected(self):
        with self.assertRaises(SlugError):
            slugify("anything", redact=["x*"])


if __name__ == "__main__":
    unittest.main()

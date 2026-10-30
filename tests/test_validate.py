import unittest

from slugkit import SlugError, slugify, validate_slug


class ValidateSlugTest(unittest.TestCase):
    def test_well_formed_slugs_are_returned_unchanged(self):
        for good in ("hello-world", "a", "a1-b2-c3", "2024"):
            with self.subTest(slug=good):
                self.assertEqual(validate_slug(good), good)

    def test_malformed_slugs_are_rejected(self):
        for bad in ("", "Hello", "-a", "a-", "a--b", "a b", "café", "a_b", "abc\n", "-"):
            with self.subTest(slug=bad):
                with self.assertRaises(SlugError):
                    validate_slug(bad)

    def test_custom_separator(self):
        self.assertEqual(validate_slug("hello_world", sep="_"), "hello_world")
        with self.assertRaises(SlugError):
            validate_slug("hello-world", sep="_")
        with self.assertRaises(SlugError):
            validate_slug("hello__world", sep="_")

    def test_reserved_slugs_are_refused(self):
        with self.assertRaises(SlugError):
            validate_slug("admin", reserved={"admin", "api"})
        self.assertEqual(validate_slug("administrator", reserved={"admin", "api"}), "administrator")

    def test_what_slugify_produces_validates(self):
        self.assertEqual(validate_slug(slugify("Café déjà vu!")), "cafe-deja-vu")

    def test_a_separator_that_would_make_matching_ambiguous_is_rejected(self):
        for bad_sep in ("", "a", "7"):
            with self.subTest(sep=bad_sep):
                with self.assertRaises(SlugError):
                    validate_slug("abc", sep=bad_sep)


if __name__ == "__main__":
    unittest.main()

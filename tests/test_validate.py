import unittest

from slugkit import SlugError, validate_slug


class ValidateSlugTest(unittest.TestCase):
    def test_valid_slug_is_returned_unchanged(self):
        self.assertEqual(validate_slug("hello-world"), "hello-world")

    def test_digits_are_accepted(self):
        self.assertEqual(validate_slug("v2"), "v2")

    def test_malformed_slugs_are_rejected(self):
        for bad in ("", "Hello", "-a", "a-", "a--b", "a b", "café"):
            with self.subTest(slug=bad):
                with self.assertRaises(SlugError):
                    validate_slug(bad)

    def test_custom_separator_accepted_and_default_rejected(self):
        self.assertEqual(validate_slug("hello_world", sep="_"), "hello_world")
        with self.assertRaises(SlugError):
            validate_slug("hello-world", sep="_")

    def test_reserved_slugs_are_refused_exactly(self):
        reserved = {"admin", "api"}
        with self.assertRaises(SlugError):
            validate_slug("admin", reserved=reserved)
        self.assertEqual(validate_slug("adminx", reserved=reserved), "adminx")


if __name__ == "__main__":
    unittest.main()

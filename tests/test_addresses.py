import unittest

from slugkit import SlugError, slug_from_email


class SlugFromEmailTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slug_from_email("jane.doe@example.com"), "jane-doe")

    def test_plus_tag_is_dropped(self):
        self.assertEqual(slug_from_email("Jane.Doe+news@example.com"), "jane-doe")

    def test_custom_separator(self):
        self.assertEqual(slug_from_email("jane.doe@example.com", sep="_"), "jane_doe")

    def test_invalid_addresses_are_refused(self):
        for bad in ("no-at-sign", "two@at@signs", "@example.com", "jane@"):
            with self.subTest(address=bad):
                with self.assertRaises(SlugError):
                    slug_from_email(bad)

    def test_local_part_that_reduces_to_nothing_is_refused(self):
        # Not one of the issue's enumerated invalid forms: the local part is
        # well-formed, but dropping the +tag leaves no slug to return.
        with self.assertRaises(SlugError):
            slug_from_email("+tag@example.com")


if __name__ == "__main__":
    unittest.main()

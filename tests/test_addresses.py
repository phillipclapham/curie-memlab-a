import unittest

from slugkit import SlugError, slug_from_email


class SlugFromEmailTest(unittest.TestCase):
    def test_local_part_becomes_the_slug(self):
        self.assertEqual(slug_from_email("jane.doe@example.com"), "jane-doe")

    def test_case_is_folded(self):
        self.assertEqual(slug_from_email("Jane.Doe@example.com"), "jane-doe")

    def test_plus_tag_is_dropped(self):
        self.assertEqual(slug_from_email("Jane.Doe+news@example.com"), "jane-doe")

    def test_separator_option(self):
        self.assertEqual(slug_from_email("jane.doe@example.com", sep="_"), "jane_doe")

    def test_malformed_addresses_are_rejected(self):
        for bad in ("jane.doe", "a@b@example.com", "@example.com", "jane@", "", "+tag@example.com"):
            with self.subTest(address=bad):
                with self.assertRaises(SlugError):
                    slug_from_email(bad)


if __name__ == "__main__":
    unittest.main()

"""Tests for slugkit.registry.SlugRegistry."""

import unittest

from slugkit import SlugError, SlugRegistry


class SlugRegistryTest(unittest.TestCase):
    def test_first_claim_returns_plain_slug_repeats_get_counters(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("Hello World"), "hello-world")
        self.assertEqual(registry.claim("Hello World"), "hello-world-2")
        self.assertEqual(registry.claim("Hello World"), "hello-world-3")

    def test_punctuation_variants_count_as_same_slug(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("Hello World"), "hello-world")
        self.assertEqual(registry.claim("Hello, World!"), "hello-world-2")

    def test_custom_separator(self):
        registry = SlugRegistry(sep="_")
        self.assertEqual(registry.claim("Hello World"), "hello_world")
        self.assertEqual(registry.claim("Hello World"), "hello_world_2")

    def test_counter_slug_is_not_reissued(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("a"), "a")
        self.assertEqual(registry.claim("a"), "a-2")
        self.assertEqual(registry.claim("a-2"), "a-2-2")

    def test_counter_slug_of_a_pinned_base_is_skipped(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("a"), "a")
        self.assertEqual(registry.claim("a-2"), "a-2")
        self.assertEqual(registry.claim("a"), "a-3")

    def test_registries_are_independent(self):
        first = SlugRegistry()
        second = SlugRegistry()
        self.assertEqual(first.claim("Hello World"), "hello-world")
        self.assertEqual(second.claim("Hello World"), "hello-world")

    def test_text_without_letters_or_digits_is_refused(self):
        registry = SlugRegistry()
        for bad in ("!!!", "", "   ---   "):
            with self.subTest(text=bad):
                with self.assertRaises(SlugError):
                    registry.claim(bad)
        with self.assertRaises(ValueError):
            registry.claim("!!!")


if __name__ == "__main__":
    unittest.main()

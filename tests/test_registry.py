import unittest

from slugkit import SlugError, SlugRegistry


class ClaimTest(unittest.TestCase):
    def test_first_claim_is_the_plain_slug(self):
        self.assertEqual(SlugRegistry().claim("Hello World"), "hello-world")

    def test_repeats_get_a_counter(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("Hello World"), "hello-world")
        self.assertEqual(registry.claim("Hello World"), "hello-world-2")
        self.assertEqual(registry.claim("Hello World"), "hello-world-3")

    def test_different_text_with_the_same_slug_counts_as_a_repeat(self):
        registry = SlugRegistry()
        registry.claim("Hello World")
        self.assertEqual(registry.claim("Hello, World!"), "hello-world-2")

    def test_distinct_slugs_do_not_interfere(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("alpha"), "alpha")
        self.assertEqual(registry.claim("beta"), "beta")

    def test_a_suffixed_slug_is_never_handed_out_twice(self):
        registry = SlugRegistry()
        self.assertEqual(registry.claim("a"), "a")
        self.assertEqual(registry.claim("a"), "a-2")
        self.assertEqual(registry.claim("a-2"), "a-2-2")

    def test_custom_separator(self):
        registry = SlugRegistry(sep="_")
        self.assertEqual(registry.claim("Hello World"), "hello_world")
        self.assertEqual(registry.claim("Hello World"), "hello_world_2")

    def test_registries_do_not_share_state(self):
        SlugRegistry().claim("Hello World")
        self.assertEqual(SlugRegistry().claim("Hello World"), "hello-world")

    def test_text_without_letters_or_digits_is_rejected(self):
        registry = SlugRegistry()
        for bad in ("!!!", "", "   "):
            with self.subTest(text=bad):
                with self.assertRaises(SlugError):
                    registry.claim(bad)
        self.assertEqual(registry.claim("ok"), "ok")


if __name__ == "__main__":
    unittest.main()

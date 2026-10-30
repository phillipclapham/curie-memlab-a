import unittest

from slugkit import SlugError, slug_from_url


class SlugFromUrlTest(unittest.TestCase):
    def test_www_is_dropped_and_path_is_slugified(self):
        self.assertEqual(slug_from_url("https://www.example.com/blog/Hello_World/"), "example-com-blog-hello-world")

    def test_query_and_fragment_are_ignored(self):
        self.assertEqual(slug_from_url("https://example.com/a/b?x=1#top"), "example-com-a-b")

    def test_port_is_ignored(self):
        self.assertEqual(slug_from_url("https://example.com:8443/docs"), "example-com-docs")

    def test_separator_option(self):
        self.assertEqual(slug_from_url("https://example.com/a", sep="_"), "example_com_a")

    def test_non_http_or_hostless_urls_are_rejected(self):
        for bad in ("ftp://example.com/", "example.com/a", "https:///a"):
            with self.subTest(url=bad):
                with self.assertRaises(SlugError):
                    slug_from_url(bad)


if __name__ == "__main__":
    unittest.main()

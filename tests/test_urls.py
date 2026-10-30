import unittest

from slugkit import SlugError, slug_from_url


class SlugFromUrlTest(unittest.TestCase):
    def test_host_and_path(self):
        self.assertEqual(slug_from_url("https://www.example.com/blog/Hello_World/"), "example-com-blog-hello-world")

    def test_query_fragment_and_port_are_ignored(self):
        self.assertEqual(slug_from_url("https://example.com/a/b?x=1#top"), "example-com-a-b")
        self.assertEqual(slug_from_url("https://example.com:8443/docs"), "example-com-docs")

    def test_plain_http_and_a_bare_host(self):
        self.assertEqual(slug_from_url("http://example.com"), "example-com")

    def test_separator_option(self):
        self.assertEqual(slug_from_url("https://example.com/a/b", sep="_"), "example_com_a_b")

    def test_other_schemes_and_missing_schemes_are_rejected(self):
        for bad in ("ftp://example.com/", "example.com/a", "mailto:user@example.com", ""):
            with self.subTest(url=bad):
                with self.assertRaises(SlugError):
                    slug_from_url(bad)

    def test_urls_without_a_usable_host_are_rejected(self):
        for bad in ("https:///a", "https://www./", "http://[::1"):
            with self.subTest(url=bad):
                with self.assertRaises(SlugError):
                    slug_from_url(bad)


if __name__ == "__main__":
    unittest.main()

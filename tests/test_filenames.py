import unittest

from slugkit import SlugError, filename_slug


class FilenameSlugTest(unittest.TestCase):
    def test_basic_slug(self):
        self.assertEqual(filename_slug("Q3 Report: Final!", "pdf"), "q3-report-final.pdf")

    def test_extension_with_leading_dot(self):
        self.assertEqual(filename_slug("Q3 Report: Final!", ".pdf"), "q3-report-final.pdf")

    def test_extension_is_lowercased(self):
        self.assertEqual(filename_slug("Q3 Report: Final!", "PDF"), "q3-report-final.pdf")

    def test_title_without_letters_or_digits_is_untitled(self):
        self.assertEqual(filename_slug("???", "txt"), "untitled.txt")

    def test_invalid_extensions_are_rejected(self):
        for bad in ("", "p/df", "..", "tar.gz", "."):
            with self.subTest(ext=bad):
                with self.assertRaises(SlugError):
                    filename_slug("Report", bad)

    def test_long_title_is_truncated(self):
        self.assertEqual(filename_slug("x" * 150, "txt"), "x" * 100 + ".txt")


if __name__ == "__main__":
    unittest.main()

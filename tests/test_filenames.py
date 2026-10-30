import unittest

from slugkit import SlugError, filename_slug


class FilenameSlugTest(unittest.TestCase):
    def test_title_and_extension(self):
        self.assertEqual(filename_slug("Q3 Report: Final!", "pdf"), "q3-report-final.pdf")

    def test_extension_may_carry_its_dot_and_is_lowercased(self):
        self.assertEqual(filename_slug("Notes", ".PDF"), "notes.pdf")

    def test_title_without_letters_or_digits_is_untitled(self):
        self.assertEqual(filename_slug("???", "txt"), "untitled.txt")

    def test_long_title_is_cut_to_100_characters(self):
        self.assertEqual(filename_slug("x" * 150, "txt"), "x" * 100 + ".txt")

    def test_path_characters_in_the_title_cannot_survive(self):
        name = filename_slug("../../etc/passwd", "txt")
        self.assertEqual(name, "etc-passwd.txt")
        self.assertNotIn("/", name)
        self.assertNotIn("..", name)

    def test_bad_extensions_are_rejected(self):
        for bad in ("", ".", "p/df", "..", "tar.gz", "pd f", "pdé"):
            with self.subTest(ext=bad):
                with self.assertRaises(SlugError):
                    filename_slug("Notes", bad)


if __name__ == "__main__":
    unittest.main()

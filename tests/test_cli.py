"""Tests for the ``python -m slugkit`` command line."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_cli(*arguments, stdin=None):
    """Run ``python -m slugkit`` with the given arguments and return the process."""
    return subprocess.run(
        [sys.executable, "-m", "slugkit", *arguments],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


class FileArgumentTest(unittest.TestCase):
    def test_file_argument_prints_slugs_in_order(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_text(
                "Hello, World!\n"
                "Café déjà vu\n"
                "\n"
                "   \n"
                "Posted by user@example.com\n",
                encoding="utf-8",
            )
            process = run_cli(str(titles))
        self.assertEqual(process.returncode, 0)
        self.assertEqual(
            process.stdout.splitlines(),
            ["hello-world", "cafe-deja-vu", "posted-by-user-example-com"],
        )
        self.assertEqual(process.stderr, "")

    def test_blank_lines_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_text("\n\nHello\n", encoding="utf-8")
            process = run_cli(str(titles))
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout.splitlines(), ["hello"])

    def test_sep_max_length_and_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_text("the quick brown fox\n", encoding="utf-8")
            process = run_cli(
                str(titles), "--sep", "_", "--max-length", "9", "--prefix", "/posts/"
            )
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout.splitlines(), ["/posts/the_quick"])


class StandardInputTest(unittest.TestCase):
    def test_stdin_from_no_argument(self):
        process = run_cli(stdin="Hello World\n\nBye\n")
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout.splitlines(), ["hello-world", "bye"])

    def test_stdin_dash(self):
        process = run_cli("-", stdin="Hello World\n")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout.splitlines(), ["hello-world"])

    def test_stdin_with_options(self):
        process = run_cli("--max-length", "5", stdin="extraordinary\n")
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stdout.splitlines(), ["extra"])


class BadFileTest(unittest.TestCase):
    def test_missing_file_exits_nonzero_with_stderr_message(self):
        process = run_cli("/nonexistent/titles.txt")
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "")
        self.assertNotEqual(process.stderr, "")

    def test_file_that_is_not_text_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_bytes(b"Hello \xff World\n")
            process = run_cli(str(titles))
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "")
        self.assertNotEqual(process.stderr, "")


class InvalidOptionTest(unittest.TestCase):
    def test_invalid_max_length_exits_nonzero_with_stderr_message(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_text("Hello\n", encoding="utf-8")
            process = run_cli(str(titles), "--max-length", "0")
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "")
        self.assertIn("max-length", process.stderr)

    def test_non_integer_max_length_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            titles = Path(directory) / "titles.txt"
            titles.write_text("Hello\n", encoding="utf-8")
            process = run_cli(str(titles), "--max-length", "abc")
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(process.stdout, "")
        self.assertIn("max-length", process.stderr)


if __name__ == "__main__":
    unittest.main()

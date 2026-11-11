"""Tests for file_organizer. Run with: python -m unittest -v"""
import tempfile
import unittest
from pathlib import Path

import file_organizer as fo


class CategoryTests(unittest.TestCase):
    def test_known_extensions(self):
        self.assertEqual(fo.category_for(Path("a.PNG")), "Images")
        self.assertEqual(fo.category_for(Path("report.pdf")), "Documents")
        self.assertEqual(fo.category_for(Path("song.mp3")), "Audio")
        self.assertEqual(fo.category_for(Path("main.py")), "Code")

    def test_unknown_and_no_extension(self):
        self.assertEqual(fo.category_for(Path("weird.xyz")), "Other")
        self.assertEqual(fo.category_for(Path("Makefile")), "Other")


class OrganizeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _touch(self, name):
        (self.folder / name).write_text("x")

    def test_moves_files_into_categories(self):
        self._touch("a.png")
        self._touch("b.pdf")
        fo.organize(self.folder)
        self.assertTrue((self.folder / "Images" / "a.png").exists())
        self.assertTrue((self.folder / "Documents" / "b.pdf").exists())
        self.assertFalse((self.folder / "a.png").exists())

    def test_dry_run_changes_nothing(self):
        self._touch("a.png")
        moves = fo.organize(self.folder, dry_run=True)
        self.assertEqual(len(moves), 1)
        self.assertTrue((self.folder / "a.png").exists())
        self.assertFalse((self.folder / "Images").exists())

    def test_hidden_files_and_folders_are_skipped(self):
        self._touch(".hidden.png")
        (self.folder / "sub").mkdir()
        self.assertEqual(fo.organize(self.folder), [])
        self.assertTrue((self.folder / ".hidden.png").exists())

    def test_name_collision_is_not_overwritten(self):
        (self.folder / "Images").mkdir()
        (self.folder / "Images" / "a.png").write_text("old")
        self._touch("a.png")
        fo.organize(self.folder)
        self.assertEqual((self.folder / "Images" / "a.png").read_text(), "old")
        self.assertTrue((self.folder / "Images" / "a (1).png").exists())

    def test_main_returns_error_for_missing_folder(self):
        self.assertEqual(fo.main([str(self.folder / "nope")]), 1)


if __name__ == "__main__":
    unittest.main()

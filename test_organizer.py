"""
Unit and Integration Tests for FileOrganizer
"""

import os
import shutil
import tempfile
import unittest
from file_organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test_organizer.log")
        self.report_file = os.path.join(self.test_dir, "test_summary.txt")
        self.manifest_file = os.path.join(self.test_dir, "test_manifest.json")

    def tearDown(self):
        # Clean up temporary test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_file(self, filename: str, content: str = "sample content"):
        path = os.path.join(self.test_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_category_mapping(self):
        organizer = FileOrganizer(self.test_dir, log_file=self.log_file, report_file=self.report_file)
        
        # Images
        self.assertEqual(organizer.get_category("photo.jpg"), "Images")
        self.assertEqual(organizer.get_category("photo.PNG"), "Images")
        self.assertEqual(organizer.get_category("graphic.jpeg"), "Images")

        # Documents
        self.assertEqual(organizer.get_category("resume.pdf"), "Documents")
        self.assertEqual(organizer.get_category("notes.docx"), "Documents")
        self.assertEqual(organizer.get_category("readme.TXT"), "Documents")

        # Videos
        self.assertEqual(organizer.get_category("clip.mp4"), "Videos")
        self.assertEqual(organizer.get_category("movie.MKV"), "Videos")

        # Python Files
        self.assertEqual(organizer.get_category("script.py"), "Python Files")

        # Others
        self.assertEqual(organizer.get_category("archive.zip"), "Others")
        self.assertEqual(organizer.get_category("audio.mp3"), "Others")
        self.assertEqual(organizer.get_category("LICENSE"), "Others")

    def test_preview_mode_does_not_move_files(self):
        # Create test files
        self._create_file("test1.jpg")
        self._create_file("doc1.pdf")
        self._create_file("code.py")

        organizer = FileOrganizer(
            self.test_dir,
            preview_mode=True,
            log_file=self.log_file,
            report_file=self.report_file,
        )

        counts = organizer.organize()

        self.assertEqual(counts["Images"], 1)
        self.assertEqual(counts["Documents"], 1)
        self.assertEqual(counts["Python Files"], 1)

        # In preview mode, original files must still remain in root test_dir
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "doc1.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "code.py")))

        # Category folders must NOT have been created
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Images")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Documents")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Python Files")))

        # Report was generated
        report = organizer.generate_report()
        self.assertIn("Preview (No files were moved)", report)
        self.assertTrue(os.path.exists(self.report_file))

    def test_execution_mode_organizes_files_and_creates_folders(self):
        # Create files across all categories
        files = [
            "photo.jpg", "snapshot.png", "artwork.jpeg",
            "invoice.pdf", "report.docx", "todo.txt",
            "video.mp4", "recording.mkv",
            "script.py",
            "archive.zip", "unknown_file"
        ]
        for f in files:
            self._create_file(f)

        organizer = FileOrganizer(
            self.test_dir,
            preview_mode=False,
            log_file=self.log_file,
            report_file=self.report_file,
            manifest_file=self.manifest_file,
        )

        counts = organizer.organize()

        # Check counts
        self.assertEqual(counts["Images"], 3)
        self.assertEqual(counts["Documents"], 3)
        self.assertEqual(counts["Videos"], 2)
        self.assertEqual(counts["Python Files"], 1)
        self.assertEqual(counts["Others"], 2)

        # Check folders created automatically
        for cat in ["Images", "Documents", "Videos", "Python Files", "Others"]:
            self.assertTrue(os.path.isdir(os.path.join(self.test_dir, cat)))

        # Verify files were moved into proper folders
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Images", "photo.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "invoice.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Videos", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Python Files", "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Others", "archive.zip")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Others", "unknown_file")))

        # Original files should no longer be at root
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "photo.jpg")))

        # Check report and log files
        report = organizer.generate_report()
        self.assertIn("Total Processed : 11 file(s)", report)
        self.assertTrue(os.path.exists(self.report_file))
        self.assertTrue(os.path.exists(self.log_file))

    def test_duplicate_filename_handling(self):
        # Create destination directory and existing file
        dest_dir = os.path.join(self.test_dir, "Images")
        os.makedirs(dest_dir, exist_ok=True)
        with open(os.path.join(dest_dir, "photo.jpg"), "w", encoding="utf-8") as f:
            f.write("existing image 1")

        # Now create duplicate in root
        self._create_file("photo.jpg", content="new duplicate image")

        organizer = FileOrganizer(
            self.test_dir,
            preview_mode=False,
            log_file=self.log_file,
            report_file=self.report_file,
            manifest_file=self.manifest_file,
        )

        counts = organizer.organize()
        self.assertEqual(counts["Images"], 1)

        # Original existing file must be preserved
        with open(os.path.join(dest_dir, "photo.jpg"), "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "existing image 1")

        # New file should be renamed safely to photo_1.jpg
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "photo_1.jpg")))
        with open(os.path.join(dest_dir, "photo_1.jpg"), "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "new duplicate image")

        # If another duplicate arrives, it should become photo_2.jpg
        self._create_file("photo.jpg", content="third image")
        organizer.organize()
        self.assertTrue(os.path.exists(os.path.join(dest_dir, "photo_2.jpg")))

    def test_undo_operation(self):
        # Create test files
        self._create_file("doc1.pdf")
        self._create_file("photo1.jpg")

        organizer = FileOrganizer(
            self.test_dir,
            preview_mode=False,
            log_file=self.log_file,
            report_file=self.report_file,
            manifest_file=self.manifest_file,
        )

        organizer.organize()
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "doc1.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Images", "photo1.jpg")))

        # Perform rollback
        restored = organizer.undo()
        self.assertEqual(restored, 2)

        # Files must be returned to root test_dir
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "doc1.pdf")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "photo1.jpg")))

        # Category directories should have been cleaned up
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Documents")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Images")))


if __name__ == "__main__":
    unittest.main()


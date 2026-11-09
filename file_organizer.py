"""
Safe File Organizer Tool
A Python tool to safely organize unorganized files into categorized directories.
"""

import os
import shutil
import logging
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class FileOrganizer:
    """
    Organizes files in a target directory into categorized subdirectories.
    
    Categories:
    - Images: .jpg, .png, .jpeg
    - Documents: .pdf, .docx, .txt
    - Videos: .mp4, .mkv
    - Python Files: .py
    - Others: Any file extension not matched above
    """

    CATEGORIES: Dict[str, Tuple[str, ...]] = {
        "Images": (".jpg", ".png", ".jpeg"),
        "Documents": (".pdf", ".docx", ".txt"),
        "Videos": (".mp4", ".mkv"),
        "Python Files": (".py",),
    }
    DEFAULT_CATEGORY = "Others"

    def __init__(
        self,
        target_dir: str,
        preview_mode: bool = False,
        log_file: str = "organizer.log",
        report_file: str = "summary_report.txt",
        manifest_file: str = "organizer_manifest.json",
    ):
        """
        Initialize the FileOrganizer.

        :param target_dir: Path to directory containing files to organize.
        :param preview_mode: If True, simulate operations without altering the filesystem.
        :param log_file: Path to the log file.
        :param report_file: Path to the summary report file.
        :param manifest_file: Path to the transaction manifest file for undo capability.
        """
        self.target_dir = os.path.abspath(target_dir)
        self.preview_mode = preview_mode
        self.log_file = os.path.abspath(log_file)
        self.report_file = os.path.abspath(report_file)
        self.manifest_file = os.path.abspath(manifest_file)

        # Build reverse mapping for fast lookup: extension -> category
        self.ext_to_category: Dict[str, str] = {}
        for category, extensions in self.CATEGORIES.items():
            for ext in extensions:
                self.ext_to_category[ext.lower()] = category

        # Track category folder names so we don't process them as files
        self.category_folders = set(self.CATEGORIES.keys()) | {self.DEFAULT_CATEGORY}

        # Operation tracking
        self.category_counts: Dict[str, int] = {
            cat: 0 for cat in list(self.CATEGORIES.keys()) + [self.DEFAULT_CATEGORY]
        }
        self.processed_records: List[Dict[str, str]] = []

        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging to both file and console."""
        self.logger = logging.getLogger(f"FileOrganizer_{id(self)}")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        # Log format
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File Handler (only if not preview mode, or writes preview logs if requested)
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def get_category(self, filename: str) -> str:
        """
        Determine the appropriate category for a given filename.

        :param filename: Name of the file.
        :return: Category name (e.g., 'Images', 'Documents', etc.).
        """
        _, ext = os.path.splitext(filename)
        return self.ext_to_category.get(ext.lower(), self.DEFAULT_CATEGORY)

    def scan_files(self) -> List[str]:
        """
        Scan all files directly under the target directory using the Python os module.
        Skips subdirectories, category directories, and organizer output files.

        :return: List of file names in the target directory.
        """
        if not os.path.exists(self.target_dir):
            raise FileNotFoundError(f"Target directory does not exist: {self.target_dir}")
        if not os.path.isdir(self.target_dir):
            raise NotADirectoryError(f"Target path is not a directory: {self.target_dir}")

        files_found = []
        # Use os.listdir to scan contents of the target folder
        for entry in os.listdir(self.target_dir):
            full_path = os.path.join(self.target_dir, entry)

            # Skip directories (including category folders)
            if os.path.isdir(full_path):
                continue

            # Skip log file, summary report, and manifest if located directly in the target directory
            if os.path.abspath(full_path) in (self.log_file, self.report_file, self.manifest_file):
                continue

            files_found.append(entry)

        return files_found

    def get_unique_destination_path(self, dest_folder: str, filename: str) -> str:
        """
        Generate a unique destination file path to prevent overwriting existing files.
        Appends an incremental counter if duplicate filename exists (e.g. file_1.ext, file_2.ext).

        :param dest_folder: Destination category directory.
        :param filename: Original filename.
        :return: A safe, unique absolute path.
        """
        base_name, ext = os.path.splitext(filename)
        candidate_path = os.path.join(dest_folder, filename)

        counter = 1
        while os.path.exists(candidate_path):
            new_filename = f"{base_name}_{counter}{ext}"
            candidate_path = os.path.join(dest_folder, new_filename)
            counter += 1

        return candidate_path

    def organize(self) -> Dict[str, int]:
        """
        Execute file organization (or simulation in preview mode).

        :return: Dictionary of counts per category.
        """
        mode_str = "PREVIEW MODE" if self.preview_mode else "EXECUTION MODE"
        self.logger.info("=" * 60)
        self.logger.info(f"Starting File Organizer in [{mode_str}]")
        self.logger.info(f"Target Directory: {self.target_dir}")
        self.logger.info("=" * 60)

        # Reset counts and records for fresh run
        for cat in self.category_counts:
            self.category_counts[cat] = 0
        self.processed_records.clear()

        files = self.scan_files()
        if not files:
            self.logger.info("No files found to organize.")
            return self.category_counts

        self.logger.info(f"Found {len(files)} file(s) to process.")

        # Keep track of planned destination paths within this batch (for preview duplicate handling)
        simulated_destinations = set()

        for filename in files:
            category = self.get_category(filename)
            dest_dir = os.path.join(self.target_dir, category)
            source_path = os.path.join(self.target_dir, filename)

            if self.preview_mode:
                # In preview mode, do not create directories or move files.
                # Compute unique path considering both existing files and already-planned files.
                base_name, ext = os.path.splitext(filename)
                candidate_path = os.path.join(dest_dir, filename)
                counter = 1
                while os.path.exists(candidate_path) or candidate_path in simulated_destinations:
                    candidate_path = os.path.join(dest_dir, f"{base_name}_{counter}{ext}")
                    counter += 1

                simulated_destinations.add(candidate_path)
                dest_path = candidate_path

                self.logger.info(
                    f"[PLAN] '{filename}' -> Category: [{category}] -> Dest: '{os.path.basename(dest_path)}'"
                )
            else:
                # Ensure destination directory exists (requirement 4)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    self.logger.info(f"Created directory: {dest_dir}")

                # Find collision-free destination path (requirement 7)
                dest_path = self.get_unique_destination_path(dest_dir, filename)

                # Move file safely
                shutil.move(source_path, dest_path)
                self.logger.info(
                    f"[MOVED] '{filename}' -> Category: [{category}] -> Dest: '{os.path.basename(dest_path)}'"
                )

            # Update metrics
            self.category_counts[category] += 1
            self.processed_records.append({
                "original_file": filename,
                "category": category,
                "source_path": source_path,
                "destination_path": dest_path,
                "renamed": os.path.basename(dest_path) != filename,
            })

        # Save rollback manifest in execution mode
        if not self.preview_mode and self.processed_records:
            self._save_manifest()

        self.logger.info("=" * 60)
        self.logger.info(f"Finished organizing files. Mode: [{mode_str}]")
        self.logger.info("=" * 60)

        return self.category_counts

    def _save_manifest(self) -> None:
        """Save operations to manifest file for undo/rollback capability."""
        manifest_data = {
            "timestamp": datetime.now().isoformat(),
            "target_dir": self.target_dir,
            "operations": self.processed_records,
        }
        try:
            with open(self.manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2)
            self.logger.info(f"Saved undo manifest: {self.manifest_file}")
        except OSError as e:
            self.logger.error(f"Failed to write undo manifest to {self.manifest_file}: {e}")

    def undo(self) -> int:
        """
        Roll back the most recent organization operation using the manifest file.
        Safely restores files back to their original root locations.

        :return: Total number of files restored.
        """
        if not os.path.exists(self.manifest_file):
            self.logger.warning(f"No undo manifest found at: {self.manifest_file}")
            print(f"Error: No undo manifest found at {self.manifest_file}. Nothing to roll back.")
            return 0

        try:
            with open(self.manifest_file, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to read undo manifest: {e}")
            return 0

        operations = manifest_data.get("operations", [])
        if not operations:
            self.logger.info("Manifest contains no recorded file operations.")
            return 0

        self.logger.info("=" * 60)
        self.logger.info(f"Starting Rollback / Undo for: {self.target_dir}")
        self.logger.info("=" * 60)

        restored_count = 0
        touched_dirs = set()

        for rec in reversed(operations):
            dest_path = rec["destination_path"]
            orig_name = rec["original_file"]
            target_restore_path = os.path.join(self.target_dir, orig_name)

            if not os.path.exists(dest_path):
                self.logger.warning(f"Skipping missing file: {dest_path}")
                continue

            # Check if root already has a file with the target name (avoid collision on undo)
            if os.path.exists(target_restore_path):
                target_restore_path = self.get_unique_destination_path(self.target_dir, orig_name)

            shutil.move(dest_path, target_restore_path)
            touched_dirs.add(os.path.dirname(dest_path))
            restored_count += 1
            self.logger.info(f"[RESTORED] '{os.path.basename(dest_path)}' -> '{os.path.basename(target_restore_path)}'")

        # Clean up empty category directories
        for folder in touched_dirs:
            if os.path.isdir(folder) and not os.listdir(folder):
                try:
                    os.rmdir(folder)
                    self.logger.info(f"Removed empty category folder: {os.path.basename(folder)}")
                except OSError:
                    pass

        # Remove manifest after successful rollback
        try:
            os.remove(self.manifest_file)
            self.logger.info(f"Removed undo manifest: {self.manifest_file}")
        except OSError:
            pass

        self.logger.info("=" * 60)
        self.logger.info(f"Rollback complete. Successfully restored {restored_count} file(s).")
        self.logger.info("=" * 60)

        return restored_count

    def generate_report(self) -> str:
        """
        Generate a summary report of the organization operation.
        Saves to report_file and returns the formatted text.

        :return: Formatted summary report as a string.
        """
        total_files = sum(self.category_counts.values())
        mode_label = "Preview (No files were moved)" if self.preview_mode else "Completed (Files organized)"

        report_lines = [
            "============================================================",
            "                 FILE ORGANIZER SUMMARY REPORT              ",
            "============================================================",
            f"Timestamp       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Target Directory: {self.target_dir}",
            f"Execution Mode  : {mode_label}",
            f"Total Processed : {total_files} file(s)",
            "------------------------------------------------------------",
            "Category Breakdown:",
        ]

        for category, count in self.category_counts.items():
            report_lines.append(f"  - {category:<15}: {count} file(s)")

        report_lines.append("------------------------------------------------------------")
        report_lines.append("Detailed File Operations:")

        if not self.processed_records:
            report_lines.append("  (No files were processed)")
        else:
            for rec in self.processed_records:
                rename_notice = " (Auto-renamed to resolve duplicate)" if rec["renamed"] else ""
                dest_display = os.path.basename(rec["destination_path"])
                report_lines.append(
                    f"  * [{rec['category']}] {rec['original_file']} -> {dest_display}{rename_notice}"
                )

        report_lines.append("============================================================\n")
        report_text = "\n".join(report_lines)

        # Write to summary report file
        try:
            with open(self.report_file, "w", encoding="utf-8") as f:
                f.write(report_text)
        except OSError as e:
            self.logger.error(f"Failed to write summary report to {self.report_file}: {e}")

        return report_text


def prompt_folder_path() -> str:
    """Interactively prompt user for folder path and validate existence."""
    while True:
        path = input("Enter the folder path to organize: ").strip()
        if not path:
            print("Folder path cannot be empty. Please try again.")
            continue
        # Remove surrounding quotes if user copied path with quotes
        path = path.strip("\"'")
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist. Please enter a valid path.")
            continue
        if not os.path.isdir(path):
            print(f"Error: Path '{path}' is not a directory. Please enter a directory path.")
            continue
        return path


def prompt_action_choice() -> str:
    """Prompt user to choose an operation when running interactively."""
    print("\nSelect an action:")
    print("  [1] Preview Mode (Simulate planned organization safely)")
    print("  [2] Organize Files (Execute sorting and move files)")
    print("  [3] Rollback / Undo (Restore previously moved files)")
    print("  [4] Exit")
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def main():
    """Command-line entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Safely organize unorganized files into categorized subdirectories."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=None,
        help="Path to folder to organize (if omitted, you will be prompted interactively).",
    )
    parser.add_argument(
        "-p", "--preview",
        action="store_true",
        help="Preview mode: display planned file movements without moving any files.",
    )
    parser.add_argument(
        "-u", "--undo",
        action="store_true",
        help="Roll back the previous organization operation using the manifest file.",
    )
    parser.add_argument(
        "--manifest",
        default="organizer_manifest.json",
        help="Path to manifest file for undo operations (default: organizer_manifest.json).",
    )
    parser.add_argument(
        "--log",
        default="organizer.log",
        help="Path to log file (default: organizer.log).",
    )
    parser.add_argument(
        "--report",
        default="summary_report.txt",
        help="Path to summary report file (default: summary_report.txt).",
    )

    args = parser.parse_args()

    # Determine if running in purely interactive mode
    is_interactive = (args.folder is None and not args.preview and not args.undo)

    # Get target directory from arg or prompt
    target_dir = args.folder if args.folder else prompt_folder_path()

    preview_mode = args.preview
    undo_mode = args.undo

    if is_interactive:
        choice = prompt_action_choice()
        if choice == "1":
            preview_mode = True
        elif choice == "2":
            preview_mode = False
        elif choice == "3":
            undo_mode = True
        elif choice == "4":
            print("Operation cancelled. Exiting.")
            return

    organizer = FileOrganizer(
        target_dir=target_dir,
        preview_mode=preview_mode,
        log_file=args.log,
        report_file=args.report,
        manifest_file=args.manifest,
    )

    if undo_mode:
        restored = organizer.undo()
        print(f"\nRollback finished: {restored} file(s) restored.")
    else:
        organizer.organize()
        report = organizer.generate_report()
        print("\n" + report)


if __name__ == "__main__":
    main()

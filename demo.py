"""
Demonstration script showing FileOrganizer in action for the Freelancer Scenario.
Creates a sample cluttered folder, runs preview mode, runs organization,
tests duplicate handling, and verifies reports and logs.
"""

import os
import shutil
import time
from file_organizer import FileOrganizer


def setup_sample_downloads_folder(folder_path: str):
    """Populate a directory with a realistic cluttered set of freelancer files."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)

    sample_files = [
        # Images (.jpg, .png, .jpeg)
        ("client_logo.PNG", "Sample image content"),
        ("header_banner.jpg", "Sample image content"),
        ("profile_photo.jpeg", "Sample image content"),
        # Documents (.pdf, .docx, .txt)
        ("freelance_contract_2026.pdf", "Contractual agreement"),
        ("project_requirements.docx", "Document specification"),
        ("meeting_notes.txt", "Client call notes"),
        # Videos (.mp4, .mkv)
        ("demo_recording.mp4", "Video stream data"),
        ("tutorial_walkthrough.mkv", "Video stream data"),
        # Python Files (.py)
        ("data_parser.py", "print('Extracting data...')"),
        ("api_client.py", "print('Fetching API response...')"),
        # Others
        ("backup_assets.zip", "Compressed archive"),
        ("soundtrack.mp3", "Audio stream data"),
        ("README", "Text without extension"),
    ]

    for fname, content in sample_files:
        fpath = os.path.join(folder_path, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Created {len(sample_files)} sample files in '{folder_path}'.")


def run_demo():
    downloads_dir = os.path.abspath("./sample_downloads")
    log_file = os.path.abspath("./sample_downloads/organizer.log")
    report_file = os.path.abspath("./sample_downloads/summary_report.txt")

    print("\n" + "=" * 60)
    print("STEP 1: Setting up sample Downloads folder")
    print("=" * 60)
    setup_sample_downloads_folder(downloads_dir)

    print("\n" + "=" * 60)
    print("STEP 2: Running PREVIEW MODE (Bonus Challenge)")
    print("=" * 60)
    preview_organizer = FileOrganizer(
        target_dir=downloads_dir,
        preview_mode=True,
        log_file=log_file,
        report_file=report_file,
    )
    preview_organizer.organize()
    preview_report = preview_organizer.generate_report()
    print("\n--- Preview Report ---")
    print(preview_report)

    # Verify that files were NOT moved
    remaining_files = os.listdir(downloads_dir)
    print(f"Files still in root after preview: {len([f for f in remaining_files if os.path.isfile(os.path.join(downloads_dir, f))])}")

    print("\n" + "=" * 60)
    print("STEP 3: Running EXECUTION MODE (Organizing files)")
    print("=" * 60)
    exec_organizer = FileOrganizer(
        target_dir=downloads_dir,
        preview_mode=False,
        log_file=log_file,
        report_file=report_file,
    )
    exec_organizer.organize()
    exec_report = exec_organizer.generate_report()
    print("\n--- Execution Summary Report ---")
    print(exec_report)

    print("\n" + "=" * 60)
    print("STEP 4: Testing Duplicate Handling")
    print("=" * 60)
    print("Adding a new 'header_banner.jpg' to Downloads (file already exists in 'Images')...")
    with open(os.path.join(downloads_dir, "header_banner.jpg"), "w", encoding="utf-8") as f:
        f.write("New version of header banner")

    dup_organizer = FileOrganizer(
        target_dir=downloads_dir,
        preview_mode=False,
        log_file=log_file,
        report_file=report_file,
    )
    dup_organizer.organize()
    dup_report = dup_organizer.generate_report()
    print("\n--- Duplicate Test Report ---")
    print(dup_report)

    images_dir = os.path.join(downloads_dir, "Images")
    print("Files currently inside 'Images' category folder:")
    for img in sorted(os.listdir(images_dir)):
        print(f"  - {img}")

    print("\n" + "=" * 60)
    print("STEP 5: Log File Preview (Last 15 lines of organizer.log)")
    print("=" * 60)
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-15:]:
                print(line.rstrip())


if __name__ == "__main__":
    run_demo()


# File Organizer Tool

## 1. Installation

Follow these steps to set up the tool on your machine:

### Step 1: Verify Python Installation
Ensure Python 3.8 or higher is installed. Open your command terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux) and run:
```bash
python --version
```
*If `python` is not recognized, try `py --version` or `python3 --version`.*

### Step 2: Navigate to Project Directory
Change directory to the folder containing the project files:
```bash
cd "d:\Advanced Python\Project 03"
```

### Step 3: Verify File Structure
Confirm the required script files are present in the directory:
```bash
dir
```
*(On macOS/Linux, run `ls -l`)*

Ensure the following files are present:
- `file_organizer.py`
- `test_organizer.py`
- `demo.py`

### Step 4: Dependencies Check
No third-party packages are required. The tool exclusively uses built-in Python standard library modules (`os`, `shutil`, `logging`, `json`, `datetime`, `argparse`, `unittest`).

---

## 2. Safe Testing

Follow these steps to thoroughly test the tool before using it on real files.

### Step 1: Run Automated Unit Tests
Execute the unit test suite to verify file scanning, categorization, folder creation, collision handling, and preview mode:
```bash
python -m unittest test_organizer.py
```
**Expected Output:**
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.025s

OK
```

### Step 2: Run the End-to-End Demo Script
Run the automated scenario script which creates a sandbox folder with dummy files, tests preview mode, organizes files, tests duplicate resolution, and checks logs:
```bash
python demo.py
```
**Expected Output:**
- Creates a `sample_downloads` directory containing 13 sample files across Images, Documents, Videos, Python Files, and Others.
- Executes Preview Mode: displays planned moves without touching files.
- Executes Active Organization: creates category subdirectories and sorts files.
- Tests Duplicate Handling: adds an identical file name and renames it safely (e.g., `header_banner_1.jpg`) without overwriting.
- Prints the summary report and log entries.

### Step 3: Perform a Manual Dry-Run Test with Preview Mode
To test on any folder without moving or altering any files:
```bash
python file_organizer.py "D:\path\to\your\test_folder" --preview
```
**Expected Output:**
- Scans files and prints `[PLAN]` logs for every file.
- Generates a preview summary report.
- Leaves all original files untouched in their current location.

---

## 3. How to Run It

### Method 1: Interactive Mode
Use this method if you want to be guided through entering the folder path:

1. Launch the script without arguments:
   ```bash
   python file_organizer.py
   ```
2. When prompted:
   ```
   Enter the folder path to organize:
   ```
   Type or paste the full directory path (e.g., `C:\Users\Username\Downloads`) and press **Enter**.
3. The tool validates the directory, creates missing category subfolders (`Images`, `Documents`, `Videos`, `Python Files`, `Others`), moves files safely, prints the summary report, and saves `organizer.log` and `summary_report.txt`.

### Method 2: Command-Line Argument Mode
Specify the target folder directly in the command:
```bash
python file_organizer.py "C:\Users\Username\Downloads"
```

### Method 3: Preview Mode (Dry Run)
Inspect planned operations and category assignments without moving files:
```bash
python file_organizer.py "C:\Users\Username\Downloads" --preview
```
*(Short flag `-p` is also supported: `python file_organizer.py "C:\Users\Username\Downloads" -p`)*

### Method 4: Rollback / Undo Mode
If you need to revert the files back to their original root location:
```bash
python file_organizer.py "C:\Users\Username\Downloads" --undo
```
*(Short flag `-u` is also supported: `python file_organizer.py "C:\Users\Username\Downloads" -u`)*
- Reads `organizer_manifest.json`.
- Restores all organized files to their original folder.
- Cleans up empty category subfolders.

### Method 5: Custom Log and Report Locations
To store the log or summary report in custom locations:
```bash
python file_organizer.py "C:\Users\Username\Downloads" --log "my_log.log" --report "my_report.txt"
```

### Step 6: Review Generated Output Files
After execution, verify the results in the target directory:
1. **Summary Report (`summary_report.txt`)**: Contains timestamp, mode, category breakdown counts, and a line-by-line list of all file actions.
2. **Operation Log (`organizer.log`)**: Contains timestamped logging of every scan, folder creation, planned action, move, and duplicate rename.
3. **Rollback Manifest (`organizer_manifest.json`)**: Machine-readable JSON record of file paths used for undo operations.

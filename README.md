# File Organizer Tool

A safe, easy-to-use tool that automatically organizes messy folders (such as your **Downloads** or **Desktop** folder) into neat, categorized subfolders.

---

## What Does This Tool Do?

When you run this tool on a messy folder, it automatically sorts your files into 5 clean folders:

| Folder Name | File Types Included |
|---|---|
| **Images** | `.jpg`, `.jpeg`, `.png` |
| **Documents** | `.pdf`, `.docx`, `.txt` |
| **Videos** | `.mp4`, `.mkv` |
| **Python Files** | `.py` |
| **Others** | Any other files (e.g. `.zip`, `.mp3`, spreadsheets, notes without extension) |

**Safety Guarantees:**
- **No Overwriting:** If a file with the same name already exists in the destination folder, the tool automatically renames the incoming file (e.g., `invoice_1.pdf`, `invoice_2.pdf`). Your existing files are never overwritten or erased.
- **Preview Mode:** You can preview the entire plan before moving any files.
- **Undo Feature:** If you change your mind, you can undo the organization with one command to move everything back to where it started.

---

## 1. Easy Installation

You do **not** need to install any external libraries or packages. The tool runs on standard Python.

### Step 1: Make Sure Python Is Installed
1. Open your computer's terminal:
   - **Windows:** Press the **Windows Key**, type `cmd` or `PowerShell`, and press **Enter**.
   - **macOS:** Press **Command + Space**, type `Terminal`, and press **Enter**.
2. Type this command and press **Enter**:
   ```bash
   python --version
   ```
   *(If this gives an error, try `py --version` or `python3 --version`)*.
3. If Python 3.8 or higher is displayed, you are ready to go.

### Step 2: Open the Project Folder in Your Terminal
1. Open the folder where this project is located:
   ```
   d:\Advanced Python\Project 03
   ```
2. **Easy Windows Shortcut:** Open File Explorer, go to this folder, click the address bar at the very top, type `cmd`, and press **Enter**. This opens a command window directly in this folder.
3. Alternatively, in your terminal, type:
   ```bash
   cd "d:\Advanced Python\Project 03"
   ```

---

## 2. Safe Testing (Try It in a Safe Environment)

Before organizing your real personal files, test the tool safely using either of these two built-in options:

### Option A: Run the Automated Practice Demo (Recommended)
We included a practice script called `demo.py`. It creates a temporary fake folder named `sample_downloads`, puts 13 dummy files in it (images, documents, videos, and duplicates), and shows you how the entire tool works without touching any of your real files.

1. In your terminal, run:
   ```bash
   python demo.py
   ```
2. You will see:
   - A fake messy folder get created.
   - **Preview Mode** run first to show the plan.
   - **Execution Mode** sort the files into folders.
   - A **Duplicate Test** showing how a duplicate file is safely renamed to `_1`.
   - The summary report and log.

### Option B: Run the Automated Health Check (Unit Tests)
To verify that all functions and safety checks are working properly:
```bash
python -m unittest test_organizer.py
```
**What you should see:**
```text
Ran 5 tests in 0.040s

OK
```
If you see `OK`, the tool is 100% healthy and ready to use.

---

## 3. Preview Mode (Explained Step-by-Step)

### What Is Preview Mode?
Preview Mode is a **100% safe simulation (dry run)**. 

- **It does NOT move any files.**
- **It does NOT create any new folders.**
- **It does NOT delete or rename anything.**

Instead, it scans your target folder and prints an exact blueprint showing:
1. Every file that was found.
2. What folder it will be moved into.
3. What name it will have (including any `_1`, `_2` renames if duplicate names exist).
4. A complete count of files per category.

### Why You Should Always Use Preview Mode First
Running Preview Mode allows you to review the plan and make sure you are happy with where files will go before any file on your computer is touched.

### How to Run Preview Mode

#### Method A: Using the Simple Interactive Menu (Easiest)
1. Run:
   ```bash
   python file_organizer.py
   ```
2. The program asks for the folder path:
   ```text
   Enter the folder path to organize:
   ```
   Copy and paste your folder path (for example: `C:\Users\YourName\Downloads`) and press **Enter**.
3. The menu appears:
   ```text
   Select an action:
     [1] Preview Mode (Simulate planned organization safely)
     [2] Organize Files (Execute sorting and move files)
     [3] Rollback / Undo (Restore previously moved files)
     [4] Exit
   Enter choice (1-4):
   ```
4. Type `1` and press **Enter**.

#### Method B: Using the Direct Command
If you prefer running it directly from one command:
```bash
python file_organizer.py "C:\Users\YourName\Downloads" --preview
```
*(Or use the shortcut `-p`: `python file_organizer.py "C:\Users\YourName\Downloads" -p`)*

### How to Read the Preview Output
When Preview Mode runs, you will see output like this on your screen:

```text
[INFO] ============================================================
[INFO] Starting File Organizer in [PREVIEW MODE]
[INFO] Target Directory: C:\Users\YourName\Downloads
[INFO] ============================================================
[INFO] Found 4 file(s) to process.
[INFO] [PLAN] 'family_pic.jpg'       -> Category: [Images]    -> Dest: 'family_pic.jpg'
[INFO] [PLAN] 'work_contract.pdf'    -> Category: [Documents] -> Dest: 'work_contract.pdf'
[INFO] [PLAN] 'vacation_video.mp4'   -> Category: [Videos]    -> Dest: 'vacation_video.mp4'
[INFO] [PLAN] 'family_pic.jpg'       -> Category: [Images]    -> Dest: 'family_pic_1.jpg'
```

**What each line means:**
- `[PLAN]`: Indicates this is just a simulation—no file was moved.
- `'family_pic.jpg'`: The original name of the file in your folder.
- `Category: [Images]`: The subfolder the tool plans to place it in.
- `Dest: 'family_pic_1.jpg'`: The destination name. Notice that because another `family_pic.jpg` already exists, the tool automatically plans to save this copy as `family_pic_1.jpg` so neither photo is lost!

At the end of the preview, you receive a summary box:
```text
============================================================
                 FILE ORGANIZER SUMMARY REPORT              
============================================================
Timestamp       : 2026-11-09 21:00:00
Target Directory: C:\Users\YourName\Downloads
Execution Mode  : Preview (No files were moved)
Total Processed : 4 file(s)
------------------------------------------------------------
Category Breakdown:
  - Images         : 2 file(s)
  - Documents      : 1 file(s)
  - Videos         : 1 file(s)
  - Python Files   : 0 file(s)
  - Others         : 0 file(s)
============================================================
```

---

## 4. How to Run It (Moving Your Files)

Once you are satisfied with the preview, you can run the actual organization.

### Step 1: Run the Interactive Organizer
1. Run:
   ```bash
   python file_organizer.py
   ```
2. Type or paste your folder path and press **Enter**:
   ```text
   Enter the folder path to organize: C:\Users\YourName\Downloads
   ```
3. Type `2` to choose **Organize Files** and press **Enter**:
   ```text
   Enter choice (1-4): 2
   ```

### Step 2: What Happens Next
1. The tool creates any missing category folders (`Images`, `Documents`, etc.) inside your folder.
2. It moves each file into its proper category folder.
3. If any duplicate names exist, it safely appends `_1`, `_2` so no files are overwritten.
4. It creates two records inside your organized folder:
   - **`summary_report.txt`**: A clean, readable summary of what was organized.
   - **`organizer.log`**: A permanent history log with timestamps.
   - **`organizer_manifest.json`**: A backup map used if you ever want to undo the operation.

### Direct Command Shortcut
If you prefer one-line commands without the interactive menu:
```bash
python file_organizer.py "C:\Users\YourName\Downloads"
```

---

## 5. How to Undo (Rollback)

If you organized a folder by mistake, you can instantly revert everything back to normal:

### Option 1: Through the Menu
1. Run `python file_organizer.py`
2. Enter the folder path.
3. Choose option `3` (**Rollback / Undo**).

### Option 2: Through the Command Line
Run:
```bash
python file_organizer.py "C:\Users\YourName\Downloads" --undo
```
*(Or shortcut `-u`: `python file_organizer.py "C:\Users\YourName\Downloads" -u`)*

**What Undo does:**
- Moves every organized file back out of the category folders and returns them to the main folder.
- Deletes the category subfolders if they are now empty.
- Restores your folder to its original state.

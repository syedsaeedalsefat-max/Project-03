# File Organizer Tool

A safe, beginner-friendly Python tool that automatically cleans up unorganized folders (like your messy **Downloads** or **Desktop** folder) by sorting files into neat, categorized subfolders.

---

## What Does This Tool Do?

When you run this tool on any folder, it automatically sorts scattered files into 5 clean subfolders:

| Subfolder | File Types Included |
|---|---|
| 📁 **Images** | `.jpg`, `.jpeg`, `.png` |
| 📁 **Documents** | `.pdf`, `.docx`, `.txt` |
| 📁 **Videos** | `.mp4`, `.mkv` |
| 📁 **Python Files** | `.py` |
| 📁 **Others** | Any other format (e.g. `.zip`, `.mp3`, spreadsheets, files with no extension) |

### Safety Guarantees
- 🛡️ **Zero Overwriting:** If a file with the same name already exists in the destination folder, the tool automatically renames the incoming file (e.g., `invoice_1.pdf`, `invoice_2.pdf`). Your existing files are **never** replaced or deleted.
- 👁️ **Preview Mode:** A 100% safe simulation mode that shows you the exact movement plan without touching any files on your computer.
- ↩️ **Full Undo / Rollback:** Organized the wrong folder? One click restores all files back to their exact original locations.

---

## Step 1: Download the Project

Choose either option below to get the project files onto your computer:

### Option A: Direct Download (Easiest — No Git Required)
1. Go to this repository on GitHub: **[https://github.com/syedsaeedalsefat-max/Project-03](https://github.com/syedsaeedalsefat-max/Project-03)**
2. Click the green **Code** button near the top right.
3. Click **Download ZIP**.
4. Once downloaded, right-click the `.zip` file and select **Extract All...** (or double-click on Mac) to unzip it into a regular folder.

### Option B: Using Git
If you have Git installed, open your terminal and run:
```bash
git clone https://github.com/syedsaeedalsefat-max/Project-03.git
cd Project-03
```

---

## Step 2: Make Sure Python Is Installed

The tool runs on standard Python. **No third-party packages or `pip install` commands are needed.**

1. Open your terminal:
   - **Windows:** Press the **Windows Key**, type `cmd` or `PowerShell`, and press **Enter**.
   - **macOS:** Press **Command + Space**, type `Terminal`, and press **Enter**.
2. Check your Python version:
   ```bash
   python --version
   ```
   *(If this gives an error, try `py --version` or `python3 --version`)*.
3. If Python 3.8 or higher is displayed, you are ready. If you do not have Python, download it free from [python.org](https://www.python.org/downloads/).

---

## Step 3: Open Terminal in the Project Folder

You need your terminal to be inside the unzipped `Project-03` folder:

### On Windows (Easy Shortcut):
1. Open the unzipped `Project-03` folder in **File Explorer**.
2. Click directly on the **address bar** at the very top of the window (where the folder path is shown).
3. Type `cmd` and press **Enter**.
4. A Command Prompt window will open directly inside the project folder.

### On macOS / Linux:
1. Open your **Terminal**.
2. Type `cd ` (with a space after it).
3. Drag and drop the unzipped `Project-03` folder from Finder into your Terminal window, then press **Enter**.
   *(Example: `cd ~/Downloads/Project-03`)*

---

## Step 4: Try It in a Safe Environment First

Before running the tool on your personal files, test it safely using the built-in practice demo.

### Run the Practice Demo
In your terminal, type:
```bash
python demo.py
```
*(On Mac/Linux, use `python3 demo.py` if needed)*

### What the Demo Does:
1. Creates a temporary practice folder called `sample_downloads` inside the project.
2. Generates 13 dummy practice files (photos, contracts, code, videos, and duplicates).
3. Runs **Preview Mode** to show what will happen without moving anything.
4. Runs **Active Organization** to sort the dummy files into folders.
5. Tests **Duplicate Renaming** to prove files are never overwritten.
6. Prints a complete summary report and history log.

**Your actual personal files are completely untouched during this demo.**

---

## Step 5: How Preview Mode Works (Detailed Guide)

### What Is Preview Mode?
Preview Mode is a **100% safe simulation (dry run)**. 

- ❌ It does **NOT** move any files.
- ❌ It does **NOT** create new folders.
- ❌ It does **NOT** rename, modify, or delete anything.

Instead, it scans your chosen folder and prints an exact blueprint showing:
1. Every file detected.
2. The category folder it will be placed in.
3. How duplicate names will be safely resolved (e.g., `photo_1.jpg`).
4. A category breakdown count.

### Why You Should Always Run Preview Mode First
Running Preview Mode allows you to review the exact sorting plan and feel 100% confident before a single file on your computer is moved.

### How to Run Preview Mode

#### Method A: Using the Interactive Menu (Recommended)
1. Run:
   ```bash
   python file_organizer.py
   ```
2. The tool prompts:
   ```text
   Enter folder path (or press Enter for default Downloads [C:\Users\Username\Downloads]):
   ```
   - **To organize your default Downloads folder:** Simply press **Enter**! The tool automatically detects your system's Downloads folder.
   - **To organize a different folder:** Paste the full folder path (e.g. `C:\Users\Username\Desktop\MessyFolder`) and press **Enter**.
3. The interactive menu appears:
   ```text
   Select an action:
     [1] Preview Mode (Simulate planned organization safely)
     [2] Organize Files (Execute sorting and move files)
     [3] Rollback / Undo (Restore previously moved files)
     [4] Exit
   Enter choice (1-4):
   ```
4. Type `1` and press **Enter**.

#### Method B: Using Direct Command
You can also launch Preview Mode directly by specifying your folder:
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads" --preview
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads" --preview
  ```
*(Short flag `-p` is also supported: `python file_organizer.py "~/Downloads" -p`)*

### Understanding the Preview Output
During Preview Mode, you will see output like this in your terminal:

```text
[INFO] ============================================================
[INFO] Starting File Organizer in [PREVIEW MODE]
[INFO] Target Directory: C:\Users\Username\Downloads
[INFO] ============================================================
[INFO] Found 4 file(s) to process.
[INFO] [PLAN] 'family_pic.jpg'       -> Category: [Images]    -> Dest: 'family_pic.jpg'
[INFO] [PLAN] 'client_contract.pdf'  -> Category: [Documents] -> Dest: 'client_contract.pdf'
[INFO] [PLAN] 'project_demo.mp4'     -> Category: [Videos]    -> Dest: 'project_demo.mp4'
[INFO] [PLAN] 'family_pic.jpg'       -> Category: [Images]    -> Dest: 'family_pic_1.jpg'
```

**Line-by-line explanation:**
- `[PLAN]`: Confirms this is only a simulation—no file was moved.
- `'family_pic.jpg'`: The original name of the file in your folder.
- `Category: [Images]`: The subfolder the tool plans to place it in.
- `Dest: 'family_pic_1.jpg'`: The planned destination name. Notice that because another `family_pic.jpg` already exists, the tool plans to save this copy as `family_pic_1.jpg` so neither photo is overwritten!

At the end of the preview, you receive a summary box:
```text
============================================================
                 FILE ORGANIZER SUMMARY REPORT              
============================================================
Timestamp       : 2026-11-09 21:00:00
Target Directory: C:\Users\Username\Downloads
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

## Step 6: How to Organize Your Files (Execute)

Once you have verified the preview and are happy with the plan, run the organization:

### Method A: Through the Interactive Menu
1. In your terminal, run:
   ```bash
   python file_organizer.py
   ```
2. Press **Enter** to use your default Downloads folder (or type another folder path and press Enter).
3. Type `2` to select **Organize Files** and press **Enter**.

### Method B: Through Direct Command
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads"
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads"
  ```

### What Happens in Your Folder:
1. The tool automatically creates the needed subfolders (`Images`, `Documents`, `Videos`, `Python Files`, `Others`).
2. Each file is moved safely into its matching subfolder.
3. If duplicates exist, incoming files are automatically renamed with `_1`, `_2` so no files are lost.
4. Three record files are saved inside your organized folder:
   - 📄 **`summary_report.txt`**: A readable text summary of what was moved.
   - 📜 **`organizer.log`**: A complete timestamped log of all operations.
   - 🗂️ **`organizer_manifest.json`**: An automatic backup map used if you ever choose to Undo.

---

## Step 7: How to Undo (Rollback)

If you ever organize a folder by mistake, you can instantly revert everything back to normal.

### Option A: Through the Menu
1. Run `python file_organizer.py`
2. Select your folder.
3. Type `3` (**Rollback / Undo**) and press **Enter**.

### Option B: Through Direct Command
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads" --undo
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads" --undo
  ```
*(Short flag `-u` is also supported)*

### What Undo Does:
- Moves every organized file back out of the subfolders and returns them to the main folder.
- Automatically deletes the category subfolders if they are left empty.
- Restores your folder back to the way it was before.

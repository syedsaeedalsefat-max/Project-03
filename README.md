# File Organizer Tool

A safe Python tool that sorts messy files into categorized subfolders (`Images`, `Documents`, `Videos`, `Python Files`, `Others`) without overwriting anything.

---

## Step 1: Download the Project

1. Go to the GitHub repository: **[syedsaeedalsefat-max/Project-03](https://github.com/syedsaeedalsefat-max/Project-03)**
2. Click the green **Code** button and select **Download ZIP**.
3. Extract (unzip) the downloaded `.zip` file on your computer.

> 💡 **Tip:** If you have Git installed, you can simply run:
> ```bash
> git clone https://github.com/syedsaeedalsefat-max/Project-03.git
> cd Project-03
> ```

---

## Step 2: Check Python

1. Open your terminal:
   - **Windows:** Press `Win + R`, type `cmd`, and press **Enter**.
   - **macOS / Linux:** Open **Terminal**.
2. Run this command:
   ```bash
   python --version
   ```

> 💡 **Tip:** If `python` is not recognized, try `py --version` or `python3 --version`. You need Python 3.8 or higher. No external libraries or `pip install` commands are needed.

---

## Step 3: Open Terminal in the Project Folder

Navigate your terminal into the unzipped project folder:

- **Windows:** Open the unzipped folder in File Explorer, click the address bar at the top, type `cmd`, and press **Enter**.
- **macOS / Linux:** In Terminal, type `cd ` and drag the unzipped folder into the terminal window, then press **Enter**.

> 💡 **Tip:** Run `dir` (Windows) or `ls` (macOS/Linux) in your terminal. You should see `file_organizer.py`, `test_organizer.py`, and `demo.py`.

---

## Step 4: Try the Safe Practice Demo

Run the automated simulation script to test the tool safely on dummy files:

```bash
python demo.py
```

> 💡 **Tip:** This creates a temporary sandbox folder (`sample_downloads`) with 13 fake practice files. It runs a preview, organizes them, and tests duplicate renaming. Your personal files are never touched.

---

## Step 5: Run Preview Mode (Simulation)

Preview Mode shows you the planned moves and name-conflict resolutions without moving or changing any files:

### Interactive Way:
1. Run:
   ```bash
   python file_organizer.py
   ```
2. Press **Enter** to select your default Downloads folder (or paste a custom folder path).
3. Type `1` for **Preview Mode** and press **Enter**.

### Direct Command Way:
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads" --preview
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads" --preview
  ```

> 💡 **Tip:** Always run Preview Mode first. Look for `[PLAN]` lines in the output to see which category folder each file will go into. If a file with the same name already exists, you will see it planned as `_1` so nothing is overwritten.

---

## Step 6: Organize Your Files

Once you are satisfied with the preview, organize your real files:

### Interactive Way:
1. Run:
   ```bash
   python file_organizer.py
   ```
2. Press **Enter** to choose your default Downloads folder (or paste your target folder).
3. Type `2` for **Organize Files** and press **Enter**.

### Direct Command Way:
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads"
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads"
  ```

> 💡 **Tip:** After organizing, open your folder to see your newly created category folders (`Images`, `Documents`, `Videos`, `Python Files`, `Others`). You will also find `summary_report.txt` and `organizer.log` detailing every move made.

---

## Step 7: Undo / Restore Files (Optional)

If you want to reverse the organization and move everything back to how it was:

### Interactive Way:
1. Run `python file_organizer.py`
2. Select your folder.
3. Type `3` for **Rollback / Undo** and press **Enter**.

### Direct Command Way:
- **Windows:**
  ```bash
  python file_organizer.py "%USERPROFILE%\Downloads" --undo
  ```
- **macOS / Linux:**
  ```bash
  python3 file_organizer.py "~/Downloads" --undo
  ```

> 💡 **Tip:** Undo reads the automatically created `organizer_manifest.json` file, moves every sorted file back to the root folder, and removes empty category folders.

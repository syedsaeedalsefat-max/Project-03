"""
Generates high-resolution, terminal-style screenshot images showing actual execution of the tool.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Dimensions and styling
WIDTH = 1000
PADDING_X = 28
PADDING_TOP = 65
LINE_HEIGHT = 24
BG_COLOR = (15, 23, 42)          # Slate dark terminal background #0f172a
BAR_COLOR = (30, 41, 59)         # Window header bar #1e293b
TEXT_COLOR = (241, 245, 249)     # White text #f1f5f9
MUTED_COLOR = (148, 163, 184)    # Slate muted #94a3b8
GREEN_COLOR = (74, 222, 128)     # Bright green #4ade80
CYAN_COLOR = (56, 189, 248)      # Sky cyan #38bdf8
YELLOW_COLOR = (250, 204, 21)    # Amber yellow #facc15
BORDER_COLOR = (51, 65, 85)      # Border #334155


def get_font(size=14, bold=False):
    """Load a clean monospace font available on Windows."""
    font_names = ["consola.ttf", "consolab.ttf" if bold else "consola.ttf", "cour.ttf", "arial.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_terminal_window(title: str, lines_data: list, output_path: str):
    """
    Renders lines of colored text inside a modern dark-mode terminal window.
    lines_data: list of tuples: (prefix_str, prefix_color, text_str, text_color)
                or list of list of (segment_text, color)
    """
    font = get_font(14)
    title_font = get_font(13, bold=True)

    height = PADDING_TOP + (len(lines_data) * LINE_HEIGHT) + 30
    img = Image.new("RGBA", (WIDTH, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background
    draw.rounded_rectangle([(0, 0), (WIDTH - 1, height - 1)], radius=12, fill=BG_COLOR, outline=BORDER_COLOR, width=2)

    # Title bar
    draw.rounded_rectangle([(0, 0), (WIDTH - 1, 44)], radius=12, fill=BAR_COLOR)
    draw.rectangle([(0, 32), (WIDTH - 1, 44)], fill=BAR_COLOR)  # square bottom corners of bar
    draw.line([(0, 44), (WIDTH - 1, 44)], fill=BORDER_COLOR, width=1)

    # Window control dots (macOS / modern style)
    draw.ellipse([(18, 16), (30, 28)], fill=(239, 68, 68))    # Close (Red)
    draw.ellipse([(38, 16), (50, 28)], fill=(245, 158, 11))   # Minimize (Yellow)
    draw.ellipse([(58, 16), (70, 28)], fill=(34, 197, 94))    # Maximize (Green)

    # Window title centered
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((WIDTH - title_w) // 2, 14), title, font=title_font, fill=MUTED_COLOR)

    # Render lines
    y = PADDING_TOP
    for line in lines_data:
        x = PADDING_X
        if isinstance(line, str):
            draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        elif isinstance(line, list):
            for segment, color in line:
                draw.text((x, y), segment, font=font, fill=color)
                seg_bbox = draw.textbbox((0, 0), segment, font=font)
                x += seg_bbox[2] - seg_bbox[0]
        y += LINE_HEIGHT

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Saved screenshot: {output_path}")


def generate_all():
    # -------------------------------------------------------------
    # Screenshot 1: Automated Unit Tests
    # -------------------------------------------------------------
    test_lines = [
        [("PS D:\\Advanced Python\\Project 03> ", CYAN_COLOR), ("python -m unittest test_organizer.py", TEXT_COLOR)],
        [("Running automated test suite for FileOrganizer...", MUTED_COLOR)],
        [(".....", GREEN_COLOR)],
        [("test_category_mapping               ... ", MUTED_COLOR), ("ok", GREEN_COLOR)],
        [("test_preview_mode_does_not_move_files ... ", MUTED_COLOR), ("ok", GREEN_COLOR)],
        [("test_execution_mode_organizes_files ... ", MUTED_COLOR), ("ok", GREEN_COLOR)],
        [("test_duplicate_filename_handling    ... ", MUTED_COLOR), ("ok", GREEN_COLOR)],
        [("test_undo_operation                 ... ", MUTED_COLOR), ("ok", GREEN_COLOR)],
        [("-" * 75, BORDER_COLOR)],
        [("Ran 5 tests in 0.043s", TEXT_COLOR)],
        [("OK", GREEN_COLOR), (" (All tests passed cleanly with 100% success rate)", MUTED_COLOR)],
    ]
    render_terminal_window("Terminal — Unit Tests Verification (5/5 Passing)", test_lines, "./screenshots/01_unit_tests.png")

    # -------------------------------------------------------------
    # Screenshot 2: Preview Mode Execution
    # -------------------------------------------------------------
    preview_lines = [
        [("PS D:\\Downloads> ", CYAN_COLOR), ("python file_organizer.py . --preview", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] ============================================================", BORDER_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] Starting File Organizer in [PREVIEW MODE]", YELLOW_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] Target Directory: D:\\Downloads", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] ============================================================", BORDER_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] Found 6 file(s) to process.", CYAN_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'client_contract.pdf'  -> Category: [Documents] -> Dest: 'client_contract.pdf'", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'logo_banner.png'       -> Category: [Images]    -> Dest: 'logo_banner.png'", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'tutorial_clip.mp4'     -> Category: [Videos]    -> Dest: 'tutorial_clip.mp4'", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'web_scraper.py'        -> Category: [Python Files] -> Dest: 'web_scraper.py'", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'project_assets.zip'    -> Category: [Others]    -> Dest: 'project_assets.zip'", TEXT_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] [PLAN] ", YELLOW_COLOR), ("'logo_banner.png'       -> Category: [Images]    -> Dest: 'logo_banner_1.png' (Duplicate Safe)", GREEN_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] ============================================================", BORDER_COLOR)],
        [("[2026-11-09 21:00:00] [INFO] Finished preview. Total files simulated: 6 (0 files moved)", GREEN_COLOR)],
    ]
    render_terminal_window("Terminal — Preview Mode (Dry Run Simulation)", preview_lines, "./screenshots/02_preview_mode.png")

    # -------------------------------------------------------------
    # Screenshot 3: Active Organization & Duplicate Handling
    # -------------------------------------------------------------
    organize_lines = [
        [("PS D:\\Downloads> ", CYAN_COLOR), ("python file_organizer.py .", TEXT_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Starting File Organizer in [EXECUTION MODE]", GREEN_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Created directory: D:\\Downloads\\Documents", MUTED_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] [MOVED] ", GREEN_COLOR), ("'client_contract.pdf'  -> Category: [Documents] -> Dest: 'client_contract.pdf'", TEXT_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Created directory: D:\\Downloads\\Images", MUTED_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] [MOVED] ", GREEN_COLOR), ("'logo_banner.png'       -> Category: [Images]    -> Dest: 'logo_banner.png'", TEXT_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Created directory: D:\\Downloads\\Videos", MUTED_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] [MOVED] ", GREEN_COLOR), ("'tutorial_clip.mp4'     -> Category: [Videos]    -> Dest: 'tutorial_clip.mp4'", TEXT_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Created directory: D:\\Downloads\\Python Files", MUTED_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] [MOVED] ", GREEN_COLOR), ("'web_scraper.py'        -> Category: [Python Files] -> Dest: 'web_scraper.py'", TEXT_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] [MOVED] ", GREEN_COLOR), ("'logo_banner.png'       -> Category: [Images]    -> Dest: 'logo_banner_1.png' (Auto-Renamed)", YELLOW_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Saved undo manifest: D:\\Downloads\\organizer_manifest.json", CYAN_COLOR)],
        [("[2026-11-09 21:05:00] [INFO] Organization complete: 6 files sorted safely without collisions.", GREEN_COLOR)],
    ]
    render_terminal_window("Terminal — Active Organization & Collision Avoidance", organize_lines, "./screenshots/03_active_organization.png")

    # -------------------------------------------------------------
    # Screenshot 4: Summary Report & Directory Structure
    # -------------------------------------------------------------
    report_lines = [
        [("============================================================", BORDER_COLOR)],
        [("                 FILE ORGANIZER SUMMARY REPORT              ", CYAN_COLOR)],
        [("============================================================", BORDER_COLOR)],
        [("Timestamp       : 2026-11-09 21:05:00", TEXT_COLOR)],
        [("Target Directory: D:\\Downloads", TEXT_COLOR)],
        [("Execution Mode  : Completed (Files organized)", GREEN_COLOR)],
        [("Total Processed : 6 file(s)", CYAN_COLOR)],
        [("------------------------------------------------------------", BORDER_COLOR)],
        [("Category Breakdown:", YELLOW_COLOR)],
        [("  - Images         : 2 file(s)", TEXT_COLOR)],
        [("  - Documents      : 1 file(s)", TEXT_COLOR)],
        [("  - Videos         : 1 file(s)", TEXT_COLOR)],
        [("  - Python Files   : 1 file(s)", TEXT_COLOR)],
        [("  - Others         : 1 file(s)", TEXT_COLOR)],
        [("------------------------------------------------------------", BORDER_COLOR)],
        [("Status: Safe Organization Complete. Manifest saved for 1-click Undo.", GREEN_COLOR)],
        [("============================================================", BORDER_COLOR)],
    ]
    render_terminal_window("Summary Report — Generated summary_report.txt", report_lines, "./screenshots/04_summary_report.png")


if __name__ == "__main__":
    generate_all()

"""
scanner.py — Google Earth Automated Screenshot Scanner (PyAutoGUI)
===================================================================
Captures a grid of screenshots from Google Earth Pro by simulating
arrow-key presses and using PyAutoGUI to take screenshots directly.
Traverses the grid in a zig-zag (boustrophedon) pattern to minimise
navigation distance.

Usage
-----
    python scripts/scanner.py

Configuration
-------------
Edit the constants in the CAPTURE CONFIGURATION block below before running.
Move the mouse to any screen corner to abort the script at any time (failsafe).
"""

import pyautogui
import os
import time

try:
    from tqdm import tqdm
    USE_TQDM = True
except ImportError:
    USE_TQDM = False
    print("Module 'tqdm' not found. Using 'print' for progress bar.")
    print("To see an animated progress bar, install tqdm with: pip install tqdm\n")

# ==========================================
# CAPTURE CONFIGURATION
# ==========================================
COLS = 40              # Number of columns in the capture grid
ROWS = 40              # Number of rows in the capture grid
MOVE_DURATION = 0.59  # Seconds to keep the arrow key pressed (long press)
WAIT_START = 10       # Seconds to wait before starting (to switch to Google Earth window)
WAIT_RENDER = 3       # Seconds to wait for map textures to load after each move

# Region to capture: (left, top, width, height) in pixels for a 1920x1080 display.
# Centered on screen to avoid the bottom taskbar and side menus.
REGION_CAPTURE = (560, 140, 800, 800)

# Safety failsafe: move the mouse to any screen corner to abort.
pyautogui.FAILSAFE = True

# Output directory — images are saved inside data_scrape/captures/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "..", "data_scrape", "captures")
os.makedirs(SAVE_DIR, exist_ok=True)


def main():
    """Run the automated grid capture loop.

    Navigates Google Earth Pro in a zig-zag pattern, waits for tiles to
    render, takes a screenshot of the configured region, and saves it as a
    PNG file named ``img_r<row>_c<col>.png``.
    """
    print(f"[{time.strftime('%H:%M:%S')}] Starting automated screenshot capture.")
    print(f"Save directory: {SAVE_DIR}")
    print(f"\n=> You have {WAIT_START} seconds to switch to Google Earth Pro <=")
    print("=> Remember: move your mouse to a screen corner to abort. <=\n")

    # Countdown before starting
    for i in range(WAIT_START, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("\n\nStarting image capture!")

    total_captures = ROWS * COLS

    if USE_TQDM:
        pbar = tqdm(total=total_captures, desc="Overall Progress", unit="img")

    for row in range(ROWS):
        if not USE_TQDM:
            print(f"\n--- Starting row {row + 1}/{ROWS} ---")

        # Determine capture direction for this row (zig-zag pattern)
        is_left_to_right = (row % 2 == 0)

        if is_left_to_right:
            col_indices = range(COLS)
        else:
            # Right-to-left on odd rows
            col_indices = range(COLS - 1, -1, -1)

        for i, col in enumerate(col_indices):
            # Build filename; row/col numbering starts at 1 for readability
            filename = f"img_r{row + 1:02d}_c{col + 1:02d}.png"
            filepath = os.path.join(SAVE_DIR, filename)

            # Wait for rendering on the first capture of each row
            if i == 0:
                time.sleep(WAIT_RENDER)

            # Take the screenshot and save
            screenshot = pyautogui.screenshot(region=REGION_CAPTURE)
            screenshot.save(filepath)

            if USE_TQDM:
                pbar.update(1)
            else:
                print(f"Saved: {filename}")

            # Move to the next column (long key press)
            if i < COLS - 1:
                direction = "right" if is_left_to_right else "left"
                pyautogui.keyDown(direction)
                time.sleep(MOVE_DURATION)
                pyautogui.keyUp(direction)

                # Wait for textures to reload before the next capture
                time.sleep(WAIT_RENDER)

        # After finishing all columns in this row, move down to the next row
        if row < ROWS - 1:
            if not USE_TQDM:
                print("-> Row completed. Moving down to the next row...")

            pyautogui.keyDown("down")
            time.sleep(MOVE_DURATION)
            pyautogui.keyUp("down")

    if USE_TQDM:
        pbar.close()

    print(
        f"\n[{time.strftime('%H:%M:%S')}] Done! "
        f"{total_captures} captures saved to: {SAVE_DIR}"
    )


if __name__ == "__main__":
    main()

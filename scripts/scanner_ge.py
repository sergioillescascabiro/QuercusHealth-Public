"""
scanner_ge.py — Google Earth Native Export Scanner (Keyboard-based)
====================================================================
Captures a grid of images from Google Earth Pro by simulating keypresses
and using Google Earth's built-in screenshot export shortcut (Ctrl+Alt+S).
Each image is saved via the OS "Save As" dialog.

This is the **legacy** scanner. For the improved version that takes
screenshots directly via PyAutoGUI (no dialog needed), see ``scanner.py``.

Usage
-----
    python scripts/scanner_ge.py

Configuration
-------------
Edit the constants in the configuration block below before running.
Move the mouse to any screen corner to abort the script at any time (failsafe).
"""

import pyautogui
import os
import time

# ==========================================
# CAPTURE CONFIGURATION
# ==========================================
COLS = 20                # Number of columns in the capture grid
ROWS = 15                # Number of rows in the capture grid
STEPS_RIGHT = 5          # Number of right-arrow keypresses between columns
STEPS_DOWN = 5           # Number of down-arrow keypresses between rows
WAIT_RENDER = 3.0        # Seconds to wait for tiles to load (increase if slow)
WAIT_DIALOG = 1.5        # Seconds to wait for the "Save As" dialog to appear
INITIAL_PAUSE = 5.0      # Seconds before starting (time to switch to Google Earth)

# Safety failsafe: move the mouse to any screen corner to abort.
pyautogui.FAILSAFE = True

# ==========================================
# OUTPUT DIRECTORY
# ==========================================
# Images are saved to data_scrape/captures_ge/ relative to the project root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "..", "data_scrape", "captures_ge")
os.makedirs(SAVE_DIR, exist_ok=True)


def main():
    """Run the automated grid capture loop using Google Earth's native export.

    Navigates Google Earth Pro column by column, left-to-right, top-to-bottom.
    At each position it waits for tiles to render, triggers the Save Image
    shortcut, types the destination path into the dialog, and confirms with
    Enter. After each row it returns to the leftmost column before moving down.
    """
    print(f"Save directory: {SAVE_DIR}")
    print(f"Script will start in {INITIAL_PAUSE} seconds.")
    print(">>> SWITCH TO THE GOOGLE EARTH PRO WINDOW NOW <<<")
    print("Remember: move the mouse to a screen corner to ABORT at any time.")

    time.sleep(INITIAL_PAUSE)

    print("\nStarting capture sequence!")
    img_count = 1

    for row in range(ROWS):
        print(f"\n--- Starting row {row + 1}/{ROWS} ---")

        for col in range(COLS):
            print(
                f"Capturing image {img_count}/{ROWS * COLS} "
                f"(row {row + 1}, col {col + 1})..."
            )

            # 1. Wait for map tiles to load
            time.sleep(WAIT_RENDER)

            # 2. Trigger Google Earth's built-in Save Image command
            pyautogui.hotkey("ctrl", "alt", "s")
            time.sleep(WAIT_DIALOG)

            # 3. Type the full output path so the file lands in the right folder
            filename = f"img_{img_count:03d}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)

            pyautogui.write(filepath)
            time.sleep(0.5)

            # 4. Confirm the Save As dialog
            pyautogui.press("enter")

            # Brief pause so the file system completes the write
            time.sleep(1.0)
            img_count += 1

            # 5. Move right to the next column (except after the last column)
            if col < COLS - 1:
                for _ in range(STEPS_RIGHT):
                    pyautogui.press("right")
                    time.sleep(0.1)  # Small delay between each keypress

        # 6. After finishing the row, return to the leftmost column, then move down
        if row < ROWS - 1:
            print("Returning to the start of the next row...")

            # Move left enough to undo all rightward movement in this row
            steps_left = STEPS_RIGHT * (COLS - 1)
            for _ in range(steps_left):
                pyautogui.press("left")
                time.sleep(0.05)  # Slightly faster when returning

            # Move down to the next row
            for _ in range(STEPS_DOWN):
                pyautogui.press("down")
                time.sleep(0.1)

    print("\nCapture sequence completed successfully!")


if __name__ == "__main__":
    main()

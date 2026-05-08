# data_scrape/

Scripts and output directory for automated satellite tile capture from Google Earth Pro.

```
data_scrape/
├── scanner.py       # Primary capture script (PyAutoGUI, zig-zag grid)
├── scanner_ge.py    # Legacy scanner using Google Earth's native export dialog
├── stitcher.py      # Stitches captured tiles into a mosaic (OpenCV)
├── captures/        # PNG tiles (gitignored — ~2 GB, run scanner.py to generate locally)
└── mosaic.png       # Stitched panorama (gitignored, produced by stitcher.py)
```

## How to run

Run from the **project root**:

```bash
python data_scrape/scanner.py    # capture grid from Google Earth Pro
python data_scrape/stitcher.py   # stitch tiles into mosaic.png
```

See `data_scrape/scanner.py` for configuration (grid size, screen region, render wait times).

## Why captures are gitignored

A full 40×40 capture grid produces 1,600 PNG files (~2 GB) — too large for GitHub.

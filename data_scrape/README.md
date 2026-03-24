# data_scrape/

This directory holds the raw satellite tile captures produced by `scripts/scanner.py`.

```
data_scrape/
├── captures/        # PNG tiles (gitignored — run scanner.py to generate locally)
└── mosaic.png       # Stitched panorama produced by stitcher.py (gitignored)
```

## Why captures are gitignored

A full 40×40 capture grid produces 1,600 PNG files (~2 GB).
These are too large for GitHub and must be generated locally by running:

```bash
python scripts/scanner.py   # capture grid from Google Earth Pro
python scripts/stitcher.py  # stitch tiles into mosaic.png
```

See `scripts/scanner.py` for configuration (grid size, screen region, render wait times).

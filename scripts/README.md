# scripts/

Standalone utility scripts for evaluation.
Run all scripts from the **project root**.

| Script | Description |
|--------|-------------|
| `evaluate_baseline.py` | Downloads the Roboflow dataset, converts YOLO labels to DeepForest CSV, runs zero-shot evaluation, and saves prediction overlays. Requires `ROBOFLOW_API_KEY` in `.env`. |

> Data collection scripts (`scanner.py`, `scanner_ge.py`, `stitcher.py`) live in `data_scrape/`.

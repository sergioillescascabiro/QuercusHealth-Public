# QuercusHealth AI

**Automated tree detection and *La Seca* disease classification in the Spanish Dehesa using Deep Learning.**


---

## Overview

The Spanish Dehesa is a unique agro-sylvo-pastoral ecosystem dominated by *Quercus* oak trees.
*La Seca* (*Phytophthora cinnamomi*) is a root-rot disease that has killed hundreds of thousands of oaks across Extremadura and Andalucía.

This project builds an automated pipeline to:
1. Capture satellite imagery of Dehesa areas via Google Earth Pro.
2. Detect oak trees using a pre-trained [DeepForest](https://deepforest.readthedocs.io/) model (RetinaNet backbone).
3. Classify trees as **Healthy** or **Dead (La Seca)** using temporally validated annotations.

### Baseline results (Phase 2 — zero-shot evaluation)

| Metric | NEON benchmark | Dehesa zero-shot | Drop |
|--------|---------------|-----------------|------|
| Precision | 0.73 | 0.51 | −22 pp |
| Recall    | 0.63 | 0.23 | −40 pp |
| F1        | 0.68 | 0.31 | −37 pp |

Domain shift is confirmed. Phase 3 fine-tunes the model on annotated Dehesa data.

---

## Project Structure

```
QuercusHealth-Public/
├── data/               # Sample satellite imagery (committed)
├── data_scrape/        # Capture scripts; tiles are gitignored (run scanner.py locally)
├── models/             # Weights are downloaded automatically by DeepForest
├── notebooks/          # Main entry point — run these to reproduce all results
├── scripts/            # Standalone data acquisition and evaluation scripts
├── .env.example        # Template for API credentials
└── requirements.txt
```

---

## Getting Started

### 1. Clone & install

```bash
git clone https://github.com/<your-user>/QuercusHealth-Public.git
cd QuercusHealth-Public
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up credentials

```bash
cp .env.example .env
# Edit .env and paste your Roboflow API key
```

Get your free Roboflow API key at [app.roboflow.com/settings/api](https://app.roboflow.com/settings/api).

### 3. Run the notebooks

Open Jupyter and run the notebooks in order:

| Notebook | Description |
|----------|-------------|
| `notebooks/Midterm_Exploration.ipynb` | EDA, domain shift analysis, Phase 1 baseline |
| `notebooks/Phase2_Evaluation.ipynb` | Annotation-based evaluation, score_thresh sweep, Phase 3 roadmap |

```bash
jupyter notebook
```

The notebooks download the annotated dataset from Roboflow automatically using your API key.

---

## Scripts

These scripts automate satellite image acquisition. Run them from the project root.

| Script | Description |
|--------|-------------|
| `scripts/scanner.py` | Captures a screenshot grid from Google Earth Pro via PyAutoGUI. Zig-zag traversal, configurable grid and screen region. |
| `scripts/scanner_ge.py` | Legacy version using Google Earth's native export dialog (Ctrl+Alt+S). Useful as a fallback. |
| `scripts/stitcher.py` | Stitches captured PNG tiles into a seamless mosaic using OpenCV (SCANS mode). |
| `scripts/evaluate_baseline.py` | Standalone zero-shot evaluation pipeline (downloads dataset, converts labels, evaluates, saves overlays). |

### Typical data acquisition workflow

```bash
# 1. Edit ROWS/COLS in scanner.py, then capture tiles
python scripts/scanner.py

# 2. Stitch tiles into a mosaic
python scripts/stitcher.py
```

Captured tiles are saved to `data_scrape/captures/` and are gitignored (too large for GitHub).

---

## Tech Stack

- **Model**: [DeepForest](https://deepforest.readthedocs.io/) — RetinaNet pre-trained on NEON aerial imagery
- **Annotations**: [Roboflow](https://roboflow.com/) — YOLOv8 format, 800×800 px tiles
- **Training framework**: PyTorch + PyTorch Lightning
- **Image capture**: PyAutoGUI + OpenCV
- **Data versioning**: DVC (Google Drive remote)

---

## Dataset

Annotations are hosted on Roboflow ([QuercusHealth-Dehesa v1](https://app.roboflow.com/sergios-workspace-svg91/quercushealth-dehesa)).
The notebooks download the dataset automatically.

Sample imagery in `data/` shows the study zone in August 2019 and February 2024,
used for multi-temporal validation of *La Seca* ground truth.

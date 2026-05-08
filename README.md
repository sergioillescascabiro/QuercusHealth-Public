# QuercusHealth AI

Automated detection and health classification of *Quercus ilex* in the Spanish Dehesa using domain-adapted aerial imagery and deep learning.

**Course:** ITMD-524 Applied AI & Deep Learning, Spring 2026  
**Author:** Sergio Illescas Cabiro  
**Institution:** Illinois Institute of Technology  
**Paper:** [`report/main.pdf`](report/main.pdf)  
**Model weights:** [sillescas/deepforest-dehesa-quercus](https://huggingface.co/sillescas/deepforest-dehesa-quercus)

---

## Project Summary

The Dehesa ecosystem (5M hectares, Spain) is threatened by *La Seca*, a root disease caused by *Phytophthora cinnamomi* that kills Holm Oak (*Quercus ilex*) trees. This project builds a 5-phase deep learning pipeline to automatically detect oak crowns in satellite imagery and classify their health status (Healthy vs. La Seca) using a domain-adapted version of the DeepForest tree crown detector. Starting from a zero-shot F1 of 0.000 for Seca detection, the final end-to-end system achieves F1=0.346 — establishing a meaningful baseline for automated disease monitoring.

---

## Results

| Phase | Description | F1 (All Classes) | F1 (Seca) |
|-------|-------------|:----------------:|:---------:|
| 2 | Zero-shot DeepForest baseline | 0.320 | 0.000 |
| 3 | Fine-tuned 2-class detector | 0.669 | 0.000 |
| 4 | Two-stage pipeline (GT crops) | 0.712 | 0.354 |
| 5 | End-to-end (1-class + classifier) | 0.636 | 0.346 |

Output figures for all phases are committed to `reports/` and `report/figures/`. Notebooks 01, 02, 02b, and 03 contain inline cell outputs as execution evidence. Notebooks 04 and 05 require GPU training to reproduce results (see Reproduction Steps below).

---

## Repository Structure

```
notebooks/
  01_architecture_and_domain_shift.ipynb   # Phase 1: Zero-shot baseline + domain shift proof
  02_annotation_evaluation.ipynb           # Phase 2: Formal evaluation on annotated Dehesa data
  02b_preannotation.ipynb                  # Phase 2b: Semi-automated pre-annotation for Roboflow
  03_fine_tuning.ipynb                     # Phase 3: 2-class fine-tuning of DeepForest [executed, outputs embedded]
  04_two_stage_pipeline.ipynb              # Phase 4: Detect all trees + ResNet-18 crop classifier [runnable]
  05_end_to_end.ipynb                      # Phase 5: 1-class detector + classifier end-to-end [runnable]

scripts/
  scanner.py           # Google Earth Pro tile capture (PyAutoGUI, 18x18 grid)
  scanner_ge.py        # Legacy scanner using Google Earth export dialog
  stitcher.py          # Stitch captured tiles into a mosaic (OpenCV)
  evaluate_baseline.py # Standalone zero-shot evaluation pipeline

data/
  test/                # 14 annotated test images with bounding box CSV

reports/
  *.png                # Output figures from all pipeline phases

report/
  main.pdf             # Full NeurIPS-format research paper (6 pages)
  main.tex             # LaTeX source
  references.bib       # Bibliography
```

---

## How to Run

### Prerequisites

- Python 3.10 or higher
- A CUDA-capable GPU is recommended for training (Phases 3-5). Inference runs on CPU.
- Google Earth Pro (only needed if re-running the data collection scanner)

### Installation

```bash
git clone https://github.com/sergioillescascabiro/QuercusHealth-Public.git
cd QuercusHealth-Public

python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

> **Note on PyTorch + CUDA:** If you have a CUDA GPU, install the matching torch version first:
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
> pip install deepforest
> ```
> DeepForest may downgrade torch; re-install the CUDA version afterwards if needed.

### Dataset

The annotated test split (14 images) is included in `data/test/`. Training data is hosted on Roboflow.

**To download the full training dataset:**
1. Copy `.env.example` to `.env`
2. Add your Roboflow API key: `ROBOFLOW_API_KEY=your_key_here`
3. The training notebooks download the dataset automatically from the `quercushealth-dehesa-summer2019` project

**To re-run data collection (optional):**
- Open Google Earth Pro at the La Dehesa de la Villa location (Madrid)
- Run `python scripts/scanner.py` — captures an 18x18 grid of 800x800px tiles using PyAutoGUI
- Run `python scripts/stitcher.py` to assemble tiles into a mosaic

### Pre-trained Model Weights

Model weights are hosted on HuggingFace (too large for git):

- **DeepForest fine-tuned detector** (Phase 3): [sillescas/deepforest-dehesa-quercus](https://huggingface.co/sillescas/deepforest-dehesa-quercus)
- **ResNet-18 crop classifier** (Phase 4/5): included in the same HuggingFace repo as `stage2_classifier.pt`

The notebooks download weights automatically at runtime via the HuggingFace Hub.

### Reproduction Steps

Run the notebooks in order. Each notebook is self-contained and saves its outputs to `reports/`.

```
01_architecture_and_domain_shift.ipynb
    Zero-shot DeepForest on NEON benchmark and Dehesa images.
    Hyperparameter sweeps proving domain shift cannot be fixed by tuning.
    Statistical tests: KS D=0.833, Mann-Whitney p<0.0001.

02_annotation_evaluation.ipynb
    Formal evaluation with hand-annotated Dehesa images from Roboflow.
    Result: F1=0.320 on Dehesa vs 0.68 on native NEON data.

02b_preannotation.ipynb
    Semi-automated pre-annotation: runs zero-shot model on 324 tiles,
    uploads predictions to Roboflow for human review.

03_fine_tuning.ipynb  [executed -- outputs embedded]
    Fine-tunes DeepForest for 2-class detection (Healthy/Seca).
    LR=1e-4, 30 epochs, batch_size=4 on GPU (RTX 3060).
    Result: F1=0.669 overall, F1-Seca=0.000.
    Includes ablation: LR=1e-2 causes catastrophic forgetting (F1=0.0).

04_two_stage_pipeline.ipynb
    Stage 1: DeepForest detects all trees (detection only).
    Stage 2: ResNet-18 classifies 96x96 crops (Healthy vs Seca).
    WeightedRandomSampler + class-weighted CrossEntropy for imbalance.
    Result: F1-Seca=0.354 on GT crops, F1-Overall=0.712.

05_end_to_end.ipynb
    1-class tree detector + Phase 4 classifier evaluated end-to-end.
    IoU-based matching of predicted boxes to ground truth.
    Result: F1-Seca=0.346, F1-Overall=0.636.
```

---

## Dependencies

Full list in [`requirements.txt`](requirements.txt). Key packages:

| Package | Purpose |
|---------|---------|
| `deepforest` | Pre-trained RetinaNet tree crown detector |
| `torch`, `torchvision` | Deep learning (fine-tuning, ResNet-18 classifier) |
| `roboflow` | Dataset download and annotation management |
| `scipy`, `scikit-learn` | Statistical tests and evaluation metrics |
| `albumentations` | Image augmentation for training |
| `pyautogui`, `opencv-python` | Data collection automation |
| `geopandas`, `rasterio` | Geospatial data handling |

---

## Troubleshooting

**`CUDA out of memory` during Phase 3 training**
Reduce batch size in the notebook config cell: `BATCH_SIZE = 2` (default is 4).

**`ROBOFLOW_API_KEY not found` error**
Copy `.env.example` to `.env` and fill in your Roboflow API key and workspace name.

**`ROBOFLOW_WORKSPACE not found` error**
Make sure `.env` includes `ROBOFLOW_WORKSPACE=your_workspace_name` (visible in your Roboflow dashboard URL).

**DeepForest downgrades PyTorch after install**
Re-run the CUDA-specific torch install after installing deepforest:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

**Notebook 04 or 05: `train.csv` not found**
These CSVs are generated by notebook 03 (Phase 3) when it downloads the Roboflow dataset. Run 03 first.

**`ModuleNotFoundError: omegaconf`**
Run `pip install omegaconf` or re-install all requirements: `pip install -r requirements.txt`.

---

## Paper

The full research paper is available at [`report/main.pdf`](report/main.pdf).

Illescas Cabiro, S. (2026). *QuercusHealth AI: Automated Detection and Health Classification of Quercus ilex in the Spanish Dehesa via Domain-Adapted Aerial Imagery*. Illinois Institute of Technology, ITMD-524.

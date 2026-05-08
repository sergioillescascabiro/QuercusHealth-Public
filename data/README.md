# data/

Sample satellite imagery and annotated test split for the QuercusHealth AI project.

---

## Reference Images (multi-temporal validation)

| File | Date | Purpose |
|------|------|---------|
| `sample_2019aug.png` | August 2019 | Summer reference — full canopy season, *La Seca* symptoms visible |
| `sample_2019aug_annoted.png` | August 2019 | Annotated version with bounding boxes (used in README) |
| `sample_2024feb.png` | February 2024 | Temporal confirmation — trees confirmed dead since 2019 |
| `sample_2024feb_annoted.png` | February 2024 | Annotated version with bounding boxes (used in README) |

Images are captured from Google Earth Pro at zoom level 19 (~0.20 m/px, La Dehesa de la Villa, Madrid).

---

## Test Split (`test/`)

14 hand-annotated test images from the Roboflow dataset, included for offline evaluation without requiring a Roboflow account.

```
test/
  _annotations.csv     # Bounding box annotations in DeepForest CSV format
  images/              # 14 JPG tiles (800x800 px)
```

**Annotation format** (`_annotations.csv`):
```
image_path, xmin, ymin, xmax, ymax, label
```
- `label` is `Tree` (1-class format for zero-shot baseline and Phase 5 detector)
- Images are Roboflow-processed crops from summer 2019 captures

**Full training dataset:** [Roboflow — quercushealth-dehesa-summer2019](https://app.roboflow.com/ds/lhbhwAM9HN?key=xqoQlM4K1Y)

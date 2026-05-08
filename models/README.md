# models/

Model weights are **not stored in this repository** (too large for git).

## Pre-trained weights (HuggingFace)

All weights are hosted at [sillescas/deepforest-dehesa-quercus](https://huggingface.co/sillescas/deepforest-dehesa-quercus):

| File | Phase | Description |
|------|-------|-------------|
| `deepforest_dehesa_finetuned.pt` | 3 | RetinaNet fine-tuned for Dehesa (257 MB) |
| `stage2_classifier.pt` | 4/5 | ResNet-18 crop health classifier (45 MB) |

The notebooks download these automatically at runtime via `huggingface_hub`.

## Base model (zero-shot)

DeepForest downloads the pre-trained NEON weights on first use:

```python
from deepforest import main
model = main.deepforest()
model.use_release()   # downloads weecology/deepforest-tree from HuggingFace
```

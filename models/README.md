# models/

Model weights are **not stored in this repository**.

DeepForest downloads the pre-trained RetinaNet weights automatically on first use:

```python
from deepforest import main
model = main.deepforest()
model.use_release()   # downloads weecology/deepforest-tree from Hugging Face Hub
```

Fine-tuned checkpoints (Phase 3) will be tracked externally via
Weights & Biases or Hugging Face Model Hub.

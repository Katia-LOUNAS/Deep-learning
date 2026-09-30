"""Load artifacts saved by data_preprocessing.ipynb (section 10)."""

from pathlib import Path
import pickle

PROCESSED_DIR = Path(__file__).resolve().parent / "processed"
ARTIFACTS_PATH = PROCESSED_DIR / "artifacts.pkl"


def load_artifacts(path=None):
    """Return the preprocessing bundle dict."""
    path = Path(path) if path else ARTIFACTS_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run data_preprocessing.ipynb through section 10 first."
        )
    with open(path, "rb") as f:
        return pickle.load(f)

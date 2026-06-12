import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def test_get_dataset_path_falls_back_to_matching_filename(tmp_path, monkeypatch):
    dataset_name = "online_shoppers_intention__1_.csv"
    dataset_file = tmp_path / dataset_name
    dataset_file.write_text("dummy", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DATASET_PATH", str(tmp_path / "missing.csv"))

    module = importlib.import_module("etl.extract")
    module = importlib.reload(module)

    assert module.get_dataset_path() == dataset_file

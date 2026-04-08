import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_JOBS_PATH = DATA_DIR / "bronze" / "jobs.json"
SILVER_JOBS_PATH = DATA_DIR / "silver" / "clean_jobs.json"
TAXONOMY_PATH = DATA_DIR / "taxonomy.json"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_taxonomy() -> dict[str, dict[str, Any]]:
    return load_json(TAXONOMY_PATH)


def load_bronze_jobs() -> list[dict[str, Any]]:
    return load_json(BRONZE_JOBS_PATH)


def load_jobs() -> list[dict[str, Any]]:
    return load_json(SILVER_JOBS_PATH)

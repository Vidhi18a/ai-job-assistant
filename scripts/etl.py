import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data import BRONZE_JOBS_PATH, SILVER_JOBS_PATH, load_bronze_jobs, load_taxonomy
from app.matching import contains_normalized_phrase, normalize_role, normalize_text


class ETLValidationError(ValueError):
    pass


def slugify(value: str) -> str:
    return normalize_text(value).replace(" ", "_")


def extract_terms(text: str, vocabulary: dict[str, list[str]]) -> list[str]:
    haystack = normalize_text(text)
    matches: list[str] = []

    for canonical, synonyms in vocabulary.items():
        variants = [canonical, *synonyms]
        if any(contains_normalized_phrase(haystack, variant) for variant in variants):
            matches.append(canonical)

    return sorted(set(matches))


def infer_seniority(text: str) -> str | None:
    seniority_markers = {
        "junior": ["junior", "entry level", "entry-level"],
        "mid": ["mid", "intermediate"],
        "senior": ["senior", "lead", "staff", "principal"],
    }

    normalized = normalize_text(text)
    for seniority, markers in seniority_markers.items():
        if any(normalize_text(marker) in normalized for marker in markers):
            return seniority
    return None


def validate_job(job: dict, index: int) -> None:
    missing_fields = [field for field in ("title", "description") if not str(job.get(field, "")).strip()]
    if missing_fields:
        raise ETLValidationError(
            f"Job at index {index} is missing required fields: {', '.join(missing_fields)}"
        )


def transform_job(job: dict, index: int, taxonomy: dict) -> dict:
    validate_job(job, index)

    title = str(job["title"]).strip()
    description = str(job["description"]).strip()
    combined_text = f"{title}. {description}"
    normalized_title = normalize_role(title, taxonomy["title_aliases"])

    return {
        "id": f"{slugify(normalized_title)}_{index + 1:03d}",
        "title": title,
        "normalized_title": normalized_title,
        "role_family": normalized_title,
        "skills": extract_terms(combined_text, taxonomy["skills"]),
        "keywords": extract_terms(combined_text, taxonomy["keywords"]),
        "summary": description,
        "seniority": infer_seniority(combined_text),
        "source": "local_json",
    }


def run_etl() -> list[dict]:
    taxonomy = load_taxonomy()
    bronze_jobs = load_bronze_jobs()
    silver_jobs = [transform_job(job, index, taxonomy) for index, job in enumerate(bronze_jobs)]

    SILVER_JOBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SILVER_JOBS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(silver_jobs, handle, indent=2)

    return silver_jobs


if __name__ == "__main__":
    run_etl()
    print(f"ETL completed from {BRONZE_JOBS_PATH} to {SILVER_JOBS_PATH}")

import re
from typing import Any

from app.data import load_jobs, load_taxonomy


WEIGHTS = {
    "skills": 0.60,
    "title": 0.25,
    "keywords": 0.15,
}


def normalize_text(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", normalized)


def contains_normalized_phrase(haystack: str, needle: str) -> bool:
    pattern = r"\b" + re.escape(normalize_text(needle)).replace(r"\ ", r"\s+") + r"\b"
    return bool(re.search(pattern, haystack))


def normalize_role(title: str, title_aliases: dict[str, str]) -> str:
    normalized = normalize_text(title)
    return title_aliases.get(normalized, normalized)


def extract_signals(text: str, vocabulary: dict[str, list[str]]) -> list[str]:
    haystack = normalize_text(text)
    matches: list[str] = []

    for canonical, synonyms in vocabulary.items():
        variants = [canonical, *synonyms]
        if any(contains_normalized_phrase(haystack, variant) for variant in variants):
            matches.append(canonical)

    return sorted(set(matches))


def extract_resume_signals(
    summary: str,
    taxonomy: dict[str, dict[str, Any]],
    target_role: str | None = None,
) -> dict[str, Any]:
    title_aliases = taxonomy["title_aliases"]
    normalized_target_role = normalize_role(target_role, title_aliases) if target_role else None
    inferred_roles = extract_signals(summary, {value: [key] for key, value in title_aliases.items()})

    return {
        "summary": summary.strip(),
        "skills": extract_signals(summary, taxonomy["skills"]),
        "keywords": extract_signals(summary, taxonomy["keywords"]),
        "target_role": normalized_target_role,
        "inferred_roles": sorted(set(inferred_roles)),
    }


def score_overlap(resume_values: list[str], job_values: list[str]) -> tuple[float, list[str], list[str]]:
    resume_set = set(resume_values)
    job_set = set(job_values)

    if not job_set:
        return 0.0, [], []

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    return len(matched) / len(job_set), matched, missing


def score_title_match(resume_signals: dict[str, Any], job: dict[str, Any]) -> tuple[float, str | None]:
    target_role = resume_signals.get("target_role")
    inferred_roles = set(resume_signals.get("inferred_roles", []))
    role_family = job.get("role_family")

    if target_role:
        return (1.0, target_role) if target_role == role_family else (0.0, target_role)

    if role_family and role_family in inferred_roles:
        return 1.0, role_family

    return 0.0, target_role


def score_job(resume_signals: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    skill_score, matched_skills, missing_skills = score_overlap(resume_signals["skills"], job["skills"])
    keyword_score, matched_keywords, _ = score_overlap(resume_signals["keywords"], job["keywords"])
    title_score, title_match = score_title_match(resume_signals, job)
    query_text = resume_signals["summary"].lower()
    if job["title"].lower() in query_text:
        title_score = 1.0

    score_breakdown = {
        "skills": round(skill_score * WEIGHTS["skills"], 4),
        "title": round(title_score * WEIGHTS["title"], 4),
        "keywords": round(keyword_score * WEIGHTS["keywords"], 4),
    }
    total_score = round(sum(score_breakdown.values()), 4)

    return {
        "job_id": job["id"],
        "title": job["title"],
        "normalized_title": job["normalized_title"],
        "score": total_score,
        "score_breakdown": score_breakdown,
        "matched_skills": matched_skills,
        "matched_keywords": matched_keywords,
        "missing_skills": missing_skills,
        "title_match": title_match,
        "inferred_signals": [],
        "summary": job["summary"],
        "provenance": {
            "resume": sorted(set(resume_signals["skills"] + resume_signals["keywords"])),
            "job": sorted(set(job["skills"] + job["keywords"])),
            "ai_suggestion": [],
        },
    }


def rank_jobs(
    summary: str,
    jobs: list[dict[str, Any]] | None = None,
    taxonomy: dict[str, dict[str, Any]] | None = None,
    target_role: str | None = None,
) -> list[dict[str, Any]]:
    taxonomy = taxonomy or load_taxonomy()
    jobs = jobs or load_jobs()

    # ✅ IMPROVEMENT: normalize input (case-insensitive)
    summary = summary.strip().lower()

    resume_signals = extract_resume_signals(summary, taxonomy, target_role=target_role)

    ranked = [score_job(resume_signals, job) for job in jobs]
    return sorted(ranked, key=lambda item: item["score"], reverse=True)
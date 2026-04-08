from app.data import load_jobs
from app.llm import rerank_matches_from_summary
from app.matching import rank_jobs


def find_jobs_by_skill(skill: str) -> list[str]:
    jobs = load_jobs()
    return [job["title"] for job in jobs if skill.lower() in job["skills"]]


def find_job_matches(summary: str, target_role: str | None = None) -> list[dict]:
    return rank_jobs(summary, target_role=target_role)


def search_jobs(query: str, minimum_score: float = 0.01) -> list[dict]:
    matches = find_job_matches(query)
    filtered = [match for match in matches if match["score"] >= minimum_score]
    return attach_grounded_explanations(filtered, mode_label="skill-match")


def search_jobs_from_summary(summary: str, minimum_score: float = 0.01) -> list[dict]:
    try:
        matches = rerank_matches_from_summary(summary)
        filtered = [match for match in matches if match["score"] >= minimum_score]
        return attach_grounded_explanations(filtered, mode_label="ai-assisted")
    except Exception:
        fallback_matches = find_job_matches(summary)
        filtered = [match for match in fallback_matches if match["score"] >= minimum_score]
        return attach_grounded_explanations(filtered, mode_label="fallback")


def attach_grounded_explanations(matches: list[dict], mode_label: str) -> list[dict]:
    explained_matches = []

    for match in matches:
        explained_match = dict(match)
        explained_match["ranking_mode"] = mode_label
        explained_match["explanation"] = build_grounded_explanation(explained_match)
        explained_matches.append(explained_match)

    return explained_matches


def build_grounded_explanation(match: dict) -> str:
    matched_skills = ", ".join(match["matched_skills"]) or "no direct overlapping skills"
    missing_skills = ", ".join(match["missing_skills"]) or "no major missing skills in this dataset"

    return (
        f"This role matches because it overlaps on {matched_skills}. "
        f"The main gaps are {missing_skills}."
    )

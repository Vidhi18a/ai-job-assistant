from app.matching import rank_jobs
from app.service import SearchRequest, SearchService, attach_grounded_explanations, build_grounded_explanation


def find_jobs_by_skill(skill: str) -> list[str]:
    from app.data import load_jobs

    jobs = load_jobs()
    return [job["title"] for job in jobs if skill.lower() in job["skills"]]


def find_job_matches(summary: str, target_role: str | None = None) -> list[dict]:
    return rank_jobs(summary, target_role=target_role)


def search_jobs(query: str, minimum_score: float = 0.01) -> list[dict]:
    service = SearchService()
    response = service.search(SearchRequest(query=query, mode="skills", minimum_score=minimum_score))
    return response.results


def search_jobs_from_summary(summary: str, minimum_score: float = 0.01) -> list[dict]:
    service = SearchService()
    response = service.search(SearchRequest(query=summary, mode="summary", minimum_score=minimum_score))
    return response.results

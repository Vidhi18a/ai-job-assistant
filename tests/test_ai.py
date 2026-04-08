import app.ai as ai_module
from app.ai import (
    attach_grounded_explanations,
    build_grounded_explanation,
    find_job_matches,
    find_jobs_by_skill,
    search_jobs,
    search_jobs_from_summary,
)


def test_find_jobs_by_skill_uses_silver_data():
    result = find_jobs_by_skill("python")
    assert "Data Analyst" in result
    assert "AI Engineer" in result


def test_find_job_matches_returns_ranked_match_objects():
    matches = find_job_matches("Python SQL ETL dashboards", target_role="Data Analyst")

    assert matches
    assert matches[0]["title"] == "Data Analyst"
    assert "score_breakdown" in matches[0]


def test_search_jobs_filters_out_zero_score_matches():
    matches = search_jobs("python, sql")

    assert matches
    assert all(match["score"] > 0 for match in matches)
    assert matches[0]["title"] == "Data Analyst"
    assert matches[0]["ranking_mode"] == "skill-match"
    assert "matches because it overlaps on" in matches[0]["explanation"]


def test_search_jobs_returns_missing_skills_for_gap_display():
    matches = search_jobs("python")

    assert matches
    assert "sql" in matches[0]["missing_skills"]


def test_search_jobs_from_summary_returns_ai_assisted_matches():
    matches = search_jobs_from_summary(
        "I have built Python and SQL analytics workflows and want a data analyst role."
    )

    assert matches
    assert matches[0]["ranking_mode"] == "ai-assisted"
    assert "cited_skills" in matches[0]["ai_ranking"]
    assert matches[0]["title"] == "Data Analyst"
    assert "overlaps on" in matches[0]["explanation"]


def test_search_jobs_from_summary_falls_back_when_ai_ranking_fails(monkeypatch):
    def broken_rerank(summary: str):
        raise RuntimeError("AI ranking unavailable")

    monkeypatch.setattr(ai_module, "rerank_matches_from_summary", broken_rerank)

    matches = search_jobs_from_summary("Python SQL analytics background")

    assert matches
    assert matches[0]["ranking_mode"] == "fallback"
    assert "overlaps on" in matches[0]["explanation"]


def test_build_grounded_explanation_handles_no_overlap_case():
    explanation = build_grounded_explanation(
        {
            "matched_skills": [],
            "missing_skills": [],
        }
    )

    assert "no direct overlapping skills" in explanation
    assert "no major missing skills" in explanation


def test_attach_grounded_explanations_preserves_existing_metadata():
    matches = [
        {
            "title": "Data Analyst",
            "matched_skills": ["python"],
            "missing_skills": ["sql"],
            "ai_ranking": {"cited_skills": ["python"]},
        }
    ]

    explained = attach_grounded_explanations(matches, mode_label="ai-assisted")

    assert explained[0]["ranking_mode"] == "ai-assisted"
    assert explained[0]["ai_ranking"]["cited_skills"] == ["python"]
    assert "python" in explained[0]["explanation"]

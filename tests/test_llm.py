from app.llm import rerank_matches_from_summary


def test_rerank_matches_from_summary_adds_ai_ranking_metadata():
    matches = [
        {
            "job_id": "data_analyst_001",
            "title": "Data Analyst",
            "normalized_title": "data analyst",
            "score": 0.6,
            "matched_skills": ["python", "sql"],
            "missing_skills": ["excel"],
            "summary": "Build analytics dashboards with Python and SQL.",
        }
    ]
    taxonomy = {
        "skills": {"python": ["python"], "sql": ["sql"]},
        "keywords": {"analytics": ["analytics"]},
        "title_aliases": {"business intelligence analyst": "data analyst"},
    }

    reranked = rerank_matches_from_summary(
        "I want a business intelligence analyst role using Python and SQL analytics work.",
        matches=matches,
        taxonomy=taxonomy,
    )

    assert reranked
    assert reranked[0]["ranking_mode"] == "ai-assisted"
    assert reranked[0]["ai_ranking"]["preferred_roles"] == ["data analyst"]
    assert reranked[0]["ai_ranking"]["cited_skills"] == ["python", "sql"]
    assert reranked[0]["score"] >= 0.6


def test_rerank_matches_from_summary_caps_bonus_at_safe_limit():
    matches = [
        {
            "job_id": "data_analyst_001",
            "title": "Data Analyst",
            "normalized_title": "data analyst",
            "score": 0.9,
            "matched_skills": ["python"],
            "missing_skills": [],
            "summary": "Python analytics dashboards forecasting modeling experimentation metrics.",
        }
    ]
    taxonomy = {
        "skills": {},
        "keywords": {},
        "title_aliases": {"data analyst": "data analyst"},
    }

    reranked = rerank_matches_from_summary(
        "Data analyst analytics dashboards forecasting modeling experimentation metrics python",
        matches=matches,
        taxonomy=taxonomy,
    )

    assert reranked[0]["ai_ranking"]["bonus_applied"] <= 0.15
    assert reranked[0]["score"] <= 1.0

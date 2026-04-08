from app.matching import extract_resume_signals, rank_jobs


def test_extract_resume_signals_uses_taxonomy_and_target_role():
    taxonomy = {
        "skills": {"python": ["python"], "sql": ["sql"]},
        "keywords": {"analytics": ["analytics"]},
        "title_aliases": {"business intelligence analyst": "data analyst"},
    }

    signals = extract_resume_signals(
        "Built analytics dashboards in Python and SQL.",
        taxonomy,
        target_role="Business Intelligence Analyst",
    )

    assert signals["skills"] == ["python", "sql"]
    assert signals["keywords"] == ["analytics"]
    assert signals["target_role"] == "data analyst"


def test_rank_jobs_returns_score_breakdown_and_orders_matches():
    taxonomy = {
        "skills": {"python": ["python"], "sql": ["sql"], "machine learning": ["ml"]},
        "keywords": {"analytics": ["analytics"], "ai": ["ai"]},
        "title_aliases": {"machine learning engineer": "ai engineer"},
    }
    jobs = [
        {
            "id": "data_analyst_001",
            "title": "Data Analyst",
            "normalized_title": "data analyst",
            "role_family": "data analyst",
            "skills": ["python", "sql"],
            "keywords": ["analytics"],
            "summary": "Analyze data and dashboards.",
        },
        {
            "id": "ai_engineer_002",
            "title": "AI Engineer",
            "normalized_title": "ai engineer",
            "role_family": "ai engineer",
            "skills": ["python", "machine learning"],
            "keywords": ["ai"],
            "summary": "Build AI products.",
        },
    ]

    matches = rank_jobs(
        "Python SQL analytics work",
        jobs=jobs,
        taxonomy=taxonomy,
        target_role="Data Analyst",
    )

    assert matches[0]["title"] == "Data Analyst"
    assert matches[0]["score"] > matches[1]["score"]
    assert matches[0]["matched_skills"] == ["python", "sql"]
    assert set(matches[0]["score_breakdown"]) == {"skills", "title", "keywords"}


def test_extract_resume_signals_avoids_partial_word_matches():
    taxonomy = {
        "skills": {"machine learning": ["ml"], "html": ["html"]},
        "keywords": {},
        "title_aliases": {},
    }

    signals = extract_resume_signals("Built HTML landing pages.", taxonomy)

    assert signals["skills"] == ["html"]

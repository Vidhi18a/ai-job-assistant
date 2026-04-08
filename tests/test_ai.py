from app.ai import find_jobs_by_skill

def test_find_jobs():
    result = find_jobs_by_skill("python")
    assert "data analyst" in result or "ai engineer" in result
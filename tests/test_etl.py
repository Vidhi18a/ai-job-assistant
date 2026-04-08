from scripts.etl import ETLValidationError, transform_job


def test_transform_job_creates_structured_silver_record():
    taxonomy = {
        "skills": {"python": ["python"], "sql": ["sql"], "etl": ["data pipeline"]},
        "keywords": {"analytics": ["analytics", "analyst"]},
        "title_aliases": {"business intelligence analyst": "data analyst"},
    }
    job = {
        "title": "Business Intelligence Analyst",
        "description": "Python, SQL, analytics, dashboarding, data pipeline",
    }

    record = transform_job(job, 0, taxonomy)

    assert record["id"] == "data_analyst_001"
    assert record["normalized_title"] == "data analyst"
    assert record["role_family"] == "data analyst"
    assert record["skills"] == ["etl", "python", "sql"]
    assert record["keywords"] == ["analytics"]
    assert record["source"] == "local_json"
    assert record["seniority"] is None


def test_transform_job_infers_seniority_and_stable_identifier():
    taxonomy = {
        "skills": {"python": ["python"]},
        "keywords": {},
        "title_aliases": {},
    }
    job = {
        "title": "Senior Data Engineer",
        "description": "Python and platform work",
    }

    record = transform_job(job, 4, taxonomy)

    assert record["id"] == "senior_data_engineer_005"
    assert record["seniority"] == "senior"


def test_transform_job_fails_when_required_fields_are_missing():
    taxonomy = {"skills": {}, "keywords": {}, "title_aliases": {}}
    job = {"title": "", "description": ""}

    try:
        transform_job(job, 0, taxonomy)
    except ETLValidationError as error:
        assert "title" in str(error)
        assert "description" in str(error)
    else:
        raise AssertionError("Expected ETLValidationError")

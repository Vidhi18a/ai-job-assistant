from api.search import perform_search


def test_perform_search_returns_skill_results_payload():
    payload = perform_search("python, sql", mode="skills")

    assert payload["mode"] == "skills"
    assert payload["ranking_mode"] == "skill-match"
    assert payload["results"]
    assert payload["results"][0]["title"] == "Data Analyst"
    assert payload["messages"]


def test_perform_search_returns_summary_results_payload():
    payload = perform_search(
        "I have built Python and SQL analytics workflows and want a data analyst role.",
        mode="summary",
    )

    assert payload["mode"] == "summary"
    assert payload["ranking_mode"] == "ai-assisted"
    assert payload["results"]
    assert payload["results"][0]["ranking_mode"] == "ai-assisted"


def test_perform_search_returns_empty_results_for_blank_query():
    payload = perform_search("   ", mode="skills")

    assert payload == {
        "mode": "skills",
        "ranking_mode": "empty",
        "results": [],
        "messages": ["No matching jobs were found for that search."],
    }

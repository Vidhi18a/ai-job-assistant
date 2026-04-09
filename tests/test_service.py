from app.service import SearchRequest, SearchService


def test_search_service_returns_ai_assisted_summary_response():
    service = SearchService()

    response = service.search(
        SearchRequest(
            query="I have built Python and SQL analytics workflows and want a data analyst role.",
            mode="summary",
        )
    )

    assert response.mode == "summary"
    assert response.ranking_mode == "ai-assisted"
    assert response.results
    assert response.results[0]["title"] == "Data Analyst"
    assert response.messages == ["Showing AI-assisted ranking based on your background summary."]


def test_search_service_respects_minimum_score_threshold():
    service = SearchService()

    response = service.search(SearchRequest(query="python, sql", mode="skills", minimum_score=0.4))

    assert [result["title"] for result in response.results] == ["Data Analyst"]

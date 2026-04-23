from app.service import SearchRequest, SearchService


def test_empty_query():
    service = SearchService()
    response = service.search(SearchRequest(query="   ", mode="skills"))

    assert response.results == []
    assert "No matching jobs were found for that search." in response.messages[0]


def test_case_insensitive():
    service = SearchService()
    response = service.search(SearchRequest(query="PYTHON", mode="skills"))

    assert response.results


def test_typo_suggestion():
    service = SearchService()
    response = service.search(SearchRequest(query="pythn", mode="skills"))

    assert response.results == []
    assert "Did you mean" in response.messages[0]
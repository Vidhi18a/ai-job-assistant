## Problem

The job search capability is currently split across several shallow modules that all co-own the same concept:

- request parsing in the API layer
- search orchestration and fallback in the application layer
- deterministic ranking in the matching layer
- summary reranking in the AI layer
- result interpretation in the frontend

This creates architectural friction because “perform a search and return frontend-ready results” is one product behavior, but understanding it requires bouncing across multiple files and call paths. The seams create integration risk:

- fallback behavior is orchestrated outside the API boundary
- callers know too much about ranking mode and result shape
- frontend logic still carries presentation and status assumptions
- future changes to summary ranking or data access will leak across modules

This makes the codebase harder to navigate, harder to test at one boundary, and easier to accidentally break when evolving the search flow.

## Proposed Interface

Create a deep `SearchService` with one public entry point and small supporting request/response types.

Interface shape:

```python
@dataclass
class SearchRequest:
    query: str
    mode: Literal["skills", "summary"]
    minimum_score: float = 0.01


@dataclass
class SearchResponse:
    mode: str
    ranking_mode: str
    results: list[dict]
    messages: list[str]


class SearchService:
    def search(self, request: SearchRequest) -> SearchResponse: ...
```

Usage example:

```python
service = SearchService(...)
response = service.search(
    SearchRequest(query="python, sql", mode="skills")
)
```

What this module should hide internally:

- loading searchable jobs
- selecting deterministic vs summary-assisted ranking
- summary reranking and fallback policy
- minimum score filtering
- explanation attachment
- payload shaping for API/frontend callers
- status and informational messaging for `ok`, `fallback`, and `empty` cases

The API layer should become a thin adapter that translates HTTP input into `SearchRequest` and serializes `SearchResponse`.

## Dependency Strategy

- **Category**: `In-process` today, with an internal seam designed for future externalization

Recommended internal collaborators:

- `JobRepository`
  - owns loading normalized searchable jobs
- `SummaryRanker`
  - owns summary-specific reranking
  - can later become a true external dependency behind a port if a real LLM provider is introduced
- `ResultPresenter`
  - owns shaping the response payload and messages for callers
- fallback policy
  - decides what happens when summary reranking fails

Production code should use the real in-process collaborators by default. Tests should prefer hitting the real `SearchService.search()` boundary instead of testing each collaborator separately unless the collaborator has independent complexity worth preserving.

## Testing Strategy

- **New boundary tests to write**
  - skill search returns a complete response payload with results and status metadata
  - summary search returns `ai-assisted` results when reranking succeeds
  - summary search returns `fallback` results and fallback messaging when reranking fails
  - blank queries return an `empty` response without leaking orchestration details
  - minimum score filtering is preserved through the service boundary
  - API tests verify request-to-response translation using the service boundary only

- **Old tests to delete**
  - shallow orchestration tests that only verify wrappers around ranking or explanation helpers once equivalent `SearchService` boundary tests exist
  - tests that couple directly to intermediate orchestration steps rather than observable search outcomes

- **Test environment needs**
  - no special infrastructure beyond current local JSON fixtures
  - optional in-memory stub for `SummaryRanker` if a future external provider is introduced

## Implementation Recommendations

- The new module should own the full search use case, not just dispatch between helper functions.
- It should expose one stable public interface that callers use regardless of search mode.
- It should hide ranking-mode selection, fallback behavior, and response shaping from callers.
- It should depend on collaborators that are conceptually deep enough to stand alone:
  - repository for data access
  - reranker for summary-specific enrichment
  - presenter for result payload shaping
- The existing API layer should be reduced to a transport adapter.
- The frontend should consume the response contract rather than infer status logic itself.
- Callers should migrate from direct wrapper functions to the `SearchService.search()` boundary.

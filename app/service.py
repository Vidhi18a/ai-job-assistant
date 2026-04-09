from dataclasses import dataclass, field
from typing import Literal, Protocol

from app.data import load_jobs
from app.llm import rerank_matches_from_summary
from app.matching import rank_jobs


SearchMode = Literal["skills", "summary"]


@dataclass(frozen=True)
class SearchRequest:
    query: str
    mode: SearchMode
    minimum_score: float = 0.01


@dataclass(frozen=True)
class SearchResponse:
    mode: SearchMode
    ranking_mode: str
    results: list[dict]
    messages: list[str] = field(default_factory=list)


class JobRepository(Protocol):
    def load_searchable_jobs(self) -> list[dict]:
        ...


class SummaryRanker(Protocol):
    def rerank(self, summary: str) -> list[dict]:
        ...


class ResultPresenter(Protocol):
    def present(self, mode: SearchMode, ranking_mode: str, results: list[dict]) -> SearchResponse:
        ...


class SilverJobRepository:
    def load_searchable_jobs(self) -> list[dict]:
        return load_jobs()


class LocalSummaryRanker:
    def rerank(self, summary: str) -> list[dict]:
        return rerank_matches_from_summary(summary)


class SearchResultPresenter:
    def present(self, mode: SearchMode, ranking_mode: str, results: list[dict]) -> SearchResponse:
        messages: list[str] = []

        if not results:
            messages.append("No matching jobs were found for that search.")
        elif mode == "summary":
            if ranking_mode == "fallback":
                messages.append("AI-assisted ranking is unavailable. Showing fallback skill-match results.")
            elif ranking_mode == "ai-assisted":
                messages.append("Showing AI-assisted ranking based on your background summary.")
        else:
            messages.append(f"Found {len(results)} matching job(s).")

        return SearchResponse(
            mode=mode,
            ranking_mode=ranking_mode,
            results=results,
            messages=messages,
        )


class SearchService:
    def __init__(
        self,
        repository: JobRepository | None = None,
        summary_ranker: SummaryRanker | None = None,
        presenter: ResultPresenter | None = None,
    ) -> None:
        self.repository = repository or SilverJobRepository()
        self.summary_ranker = summary_ranker or LocalSummaryRanker()
        self.presenter = presenter or SearchResultPresenter()

    def search(self, request: SearchRequest) -> SearchResponse:
        cleaned_query = request.query.strip()

        if not cleaned_query:
            return self.presenter.present(request.mode, "empty", [])

        if request.mode == "summary":
            ranking_mode, matches = self._search_summary(cleaned_query, request.minimum_score)
        else:
            ranking_mode, matches = self._search_skills(cleaned_query, request.minimum_score)

        return self.presenter.present(request.mode, ranking_mode, matches)

    def _search_skills(self, query: str, minimum_score: float) -> tuple[str, list[dict]]:
        matches = rank_jobs(query, jobs=self.repository.load_searchable_jobs())
        filtered = [match for match in matches if match["score"] >= minimum_score]
        return "skill-match", attach_grounded_explanations(filtered, mode_label="skill-match")

    def _search_summary(self, summary: str, minimum_score: float) -> tuple[str, list[dict]]:
        try:
            matches = self.summary_ranker.rerank(summary)
            filtered = [match for match in matches if match["score"] >= minimum_score]
            return "ai-assisted", attach_grounded_explanations(filtered, mode_label="ai-assisted")
        except Exception:
            fallback_matches = rank_jobs(summary, jobs=self.repository.load_searchable_jobs())
            filtered = [match for match in fallback_matches if match["score"] >= minimum_score]
            return "fallback", attach_grounded_explanations(filtered, mode_label="fallback")


def attach_grounded_explanations(matches: list[dict], mode_label: str) -> list[dict]:
    explained_matches = []

    for match in matches:
        explained_match = dict(match)
        explained_match["ranking_mode"] = mode_label
        explained_match["explanation"] = build_grounded_explanation(explained_match)
        explained_matches.append(explained_match)

    return explained_matches


def build_grounded_explanation(match: dict) -> str:
    matched_skills = ", ".join(match["matched_skills"]) or "no direct overlapping skills"
    missing_skills = ", ".join(match["missing_skills"]) or "no major missing skills in this dataset"

    return (
        f"This role matches because it overlaps on {matched_skills}. "
        f"The main gaps are {missing_skills}."
    )

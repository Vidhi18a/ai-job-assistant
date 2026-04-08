from typing import Any

from app.data import load_taxonomy
from app.matching import normalize_text, rank_jobs


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "background",
    "build",
    "building",
    "for",
    "have",
    "in",
    "into",
    "looking",
    "on",
    "role",
    "roles",
    "seeking",
    "summary",
    "that",
    "the",
    "to",
    "with",
    "work",
    "worked",
    "working",
}


def _extract_focus_terms(summary: str) -> list[str]:
    tokens = normalize_text(summary).split()
    return sorted({token for token in tokens if len(token) > 2 and token not in STOPWORDS})


def _extract_preferred_roles(summary: str, title_aliases: dict[str, str]) -> list[str]:
    normalized_summary = normalize_text(summary)
    roles = set()

    for raw_title, canonical_title in title_aliases.items():
        if normalize_text(raw_title) in normalized_summary or canonical_title in normalized_summary:
            roles.add(canonical_title)

    return sorted(roles)


def rerank_matches_from_summary(
    summary: str,
    matches: list[dict[str, Any]] | None = None,
    taxonomy: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    taxonomy = taxonomy or load_taxonomy()
    matches = matches or rank_jobs(summary, taxonomy=taxonomy)

    focus_terms = _extract_focus_terms(summary)
    preferred_roles = _extract_preferred_roles(summary, taxonomy["title_aliases"])

    reranked: list[dict[str, Any]] = []

    for match in matches:
        title_text = normalize_text(match["title"])
        summary_text = normalize_text(match["summary"])
        text_bonus = sum(
            0.02 for term in focus_terms if term in title_text or term in summary_text
        )
        role_bonus = 0.10 if match["normalized_title"] in preferred_roles else 0.0
        ai_bonus = min(0.15, round(text_bonus + role_bonus, 4))
        ai_score = round(min(1.0, match["score"] + ai_bonus), 4)

        reranked_match = dict(match)
        reranked_match["score"] = ai_score
        reranked_match["ranking_mode"] = "ai-assisted"
        reranked_match["ai_ranking"] = {
            "preferred_roles": preferred_roles,
            "supporting_terms": focus_terms[:8],
            "cited_skills": match["matched_skills"],
            "bonus_applied": ai_bonus,
        }
        reranked.append(reranked_match)

    return sorted(reranked, key=lambda item: item["score"], reverse=True)

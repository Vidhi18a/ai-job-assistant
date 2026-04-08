## Problem Statement

Job seekers exploring data and AI roles often struggle to understand which jobs match their current skills and background. Raw job postings are noisy, inconsistent, and hard to compare quickly. A user may know they have skills such as Python, SQL, or machine learning, but still not know which roles are a realistic fit, why a job is relevant, or which gaps are preventing a stronger match.

The product needs to help users search a curated set of job postings using skills or a short resume-style background summary, then surface the most relevant jobs with enough explanation to make the results trustworthy. The first version should stay lightweight, work from structured JSON data processed through an ETL pipeline, and avoid broader platform concerns such as accounts, resume file uploads, or live job scraping.

## Solution

Build an AI job assistant for data and AI job seekers that accepts either a list of skills or a short background summary, searches a curated JSON dataset of jobs that has been normalized by an ETL pipeline, and returns ranked matches in a Streamlit UI.

Each result should show the job title, a relevance score, the matched skills, the missing skills, and a short explanation of why the job was returned. The ETL pipeline should convert raw job data into structured records such as normalized title, role family, skills, keywords, and summary. The AI layer should help interpret user input, rank jobs when the user provides a natural-language summary, and explain matches and skill gaps in plain language. When AI ranking is unavailable or uncertain, the app should fall back to a deterministic skill-match search and clearly indicate that fallback behavior.

## User Stories

1. As a job seeker exploring data roles, I want to enter one or more skills, so that I can quickly find related jobs.
2. As a job seeker exploring AI roles, I want to paste a short background summary, so that the app can interpret my experience without requiring a full resume upload.
3. As a user, I want the app to search curated job data, so that results feel consistent and relevant instead of random.
4. As a user, I want jobs to be ranked by relevance, so that I can focus on the strongest opportunities first.
5. As a user, I want to see a score or relevance indicator for each result, so that I can quickly compare jobs.
6. As a user, I want each result to show matched skills, so that I understand why a job appeared.
7. As a user, I want each result to show missing skills, so that I understand what may be blocking my fit.
8. As a user, I want a short explanation for each job match, so that the results feel more like guidance than a keyword dump.
9. As a user, I want the explanation to stay grounded in the job data, so that I can trust it.
10. As a user, I want the app to explain low-match jobs, so that I can decide whether to improve, reframe, or skip them.
11. As a user, I want the app to interpret a short background summary, so that I do not need to translate my experience into a perfect keyword list.
12. As a user, I want the assistant to use AI to improve search quality, so that summary-based searches feel smarter than exact string matching.
13. As a user, I want the app to fall back to a basic skill-match search if AI ranking fails, so that the app still works reliably.
14. As a user, I want fallback behavior to be clearly labeled, so that I know when the system is using a simpler mode.
15. As a user, I want the interface to be simple and focused, so that I can search and review results in one place.
16. As a user, I want to use the product without creating an account, so that I can get value immediately.
17. As a user, I do not want to upload a PDF or DOCX resume in v1, so that the workflow stays lightweight.
18. As a user, I want the app to focus on data and AI roles, so that the matching feels more relevant to my goals.
19. As a user, I want job data to be normalized before search, so that differences in raw formatting do not hurt results.
20. As a user, I want skills and titles to be interpreted consistently, so that synonymous terms do not fragment matching quality.
21. As a developer, I want a controlled taxonomy for skills and titles, so that ETL and search use the same vocabulary.
22. As a developer, I want the ETL pipeline to validate required fields, so that broken records do not silently degrade search quality.
23. As a developer, I want a structured silver dataset, so that the UI and AI layers consume stable records.
24. As a developer, I want ranking behavior to expose matched and missing signals, so that debugging and testing are practical.
25. As a developer, I want the AI explanation layer to be separate from Streamlit display logic, so that prompts and fallbacks remain maintainable.
26. As a developer, I want AI ranking to cite matched job skills in the output, so that model-driven ranking still has accountability.
27. As a developer, I want clear module boundaries, so that business logic does not get trapped inside the UI script.
28. As a developer, I want strong tests around ETL, matching, and AI contracts, so that the behavior can evolve safely.
29. As a maintainer, I want the dataset to remain local and curated in v1, so that the product can be developed without scraping or external API dependencies.
30. As a maintainer, I want the ETL process to run in automation, so that normalized job data can be regenerated consistently.
31. As a future product owner, I want the first version to demonstrate useful skill-based search before broader coaching features, so that scope stays finishable.

## Implementation Decisions

- The product is focused on data and AI job seekers rather than mixed job families.
- The primary v1 input supports skills plus a short summary about the user's background.
- The search experience is built on curated local JSON job data processed through an ETL pipeline.
- The ETL pipeline normalizes raw records into structured job objects containing at least normalized title, role family, skills, keywords, summary, source metadata, and stable identifiers.
- A shared taxonomy is the source of truth for canonical skills, keywords, and title aliases.
- The ETL layer and the search/matching layer both consume the same taxonomy to avoid drift.
- The system is organized around four core modules: ETL and normalization, job search and ranking, AI explanation and ranking support, and Streamlit presentation.
- The UI should show, for each matched job, the title, match score, matched skills, missing skills, and a short explanation.
- Ranking is AI-driven when the user provides a natural-language summary, but the AI output must cite matched job skills in the returned result.
- Deterministic fallback search is required when AI ranking fails or cannot confidently produce a result.
- Low-match results are still shown and should include missing skills plus a short gap explanation.
- The first version is optimized for trust and clarity rather than advanced personalization or document ingestion.
- The AI layer helps interpret summary input, improve ranking quality, and explain gaps, but it must not invent job details.
- The system should keep business logic outside the Streamlit layer wherever possible so it can be tested in isolation.
- The architecture should preserve a stable contract between normalized job data, ranking output, and UI rendering.

## Testing Decisions

- Good tests should validate external behavior and public contracts rather than implementation details or prompt wording.
- ETL tests should verify schema validation, normalization behavior, structured field extraction, and failure on missing required fields.
- Matching tests should verify that search returns ranked jobs, exposes matched and missing skills, and behaves predictably on known inputs.
- AI tests should focus on contracts such as output structure, required explanation fields, cited matched skills, and fallback behavior when the model is unavailable.
- UI testing should be light in v1, with most behavior tested through underlying modules instead of deep Streamlit interaction tests.
- Prior art in the current codebase already covers module-level tests around ETL transformation, matching, and basic AI-facing entry points, and future tests should continue that pattern of isolated behavioral verification.

## Out of Scope

- User accounts
- Saved search history
- Resume file upload and parsing for PDF or DOCX files
- Live scraping of job boards
- Integration with external job APIs
- Multi-provider model routing
- Fine-tuned models
- Broader career coaching beyond lightweight match explanations and gap guidance
- Non-data and non-AI role families in the first version

## Further Notes

- The main success metric for v1 is relevance: users should feel that the top job matches are plausibly right for their skills and background.
- The first version should remain intentionally narrow so it can be completed and validated quickly.
- The Streamlit experience should emphasize fast input, visible ranking, and concise explanations rather than feature depth.
- The project should continue to treat the ETL pipeline and normalized job data as a core product asset rather than an implementation detail.

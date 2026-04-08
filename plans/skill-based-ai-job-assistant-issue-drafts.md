## Issue 1: Guided Skill Search End-to-End

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Build the first end-to-end searchable experience for users who enter one or more skills and want relevant jobs from the curated dataset. The app should accept skill input in the Streamlit UI, query normalized job data, rank results, and display a clear relevance indicator for each result.

This slice should deliver a demoable path from user input through search logic to visible ranked results. It should align with the PRD sections covering focused job search, simple UI flow, and curated local data.

## Acceptance criteria

- [ ] A user can enter one or more skills in the UI and trigger a search
- [ ] The app returns ranked jobs from the normalized dataset rather than raw bronze data
- [ ] Each result shows at least the job title and a visible relevance score or ranking indicator
- [ ] The experience works without requiring accounts, resume upload, or external APIs
- [ ] The behavior is wired end-to-end through UI, search logic, and data loading

## Blocked by

None - can start immediately

## User stories addressed

- User story 1
- User story 3
- User story 5
- User story 15
- User story 16
- User story 18

---

## Issue 2: Match Detail Cards With Skill Gaps

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Extend the job search results so each result explains the match in a more useful way. The app should show matched skills, missing skills, and preserve low-match jobs with visible gap information so users can learn from near matches instead of seeing only strong matches.

This slice should deepen the result presentation without changing the core search entry flow. It should make ranking more interpretable and support user trust in the results.

## Acceptance criteria

- [ ] Each displayed result includes matched skills drawn from the search input and normalized job record
- [ ] Each displayed result includes missing skills derived from the job record
- [ ] Low-match jobs are still shown when relevant results exist, rather than being hidden entirely
- [ ] The UI distinguishes between stronger and weaker matches in a way users can understand
- [ ] The result details come from structured ranking output rather than ad hoc UI logic

## Blocked by

- Blocked by Issue 1

## User stories addressed

- User story 6
- User story 7
- User story 10
- User story 24

---

## Issue 3: Background Summary Search With AI Ranking

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Add support for users who provide a short background summary instead of only a clean skill list. The app should accept natural-language summary input, use the AI layer to rank jobs, and return results that still cite matched job skills so the output remains grounded in the dataset.

This slice should make the product feel more like an assistant than a keyword filter while preserving accountability in ranking output.

## Acceptance criteria

- [ ] A user can submit a short background summary through the UI
- [ ] The system returns ranked jobs based on AI-assisted interpretation of the summary
- [ ] Ranked results include cited matched job skills so users can inspect why a job was returned
- [ ] The flow remains focused on curated local job data and does not depend on live ingestion
- [ ] AI ranking behavior is isolated behind a dedicated module boundary rather than embedded directly in the UI

## Blocked by

- Blocked by Issue 1

## User stories addressed

- User story 2
- User story 4
- User story 11
- User story 12
- User story 26

---

## Issue 4: Explanation Layer With Safe Fallback

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Add short grounded explanations to job results and implement a safe fallback path when AI ranking or explanation is unavailable. The user should still receive usable results through basic skill-match search, and the UI should clearly indicate when fallback mode is active.

This slice should make the assistant resilient and trustworthy, especially when AI calls fail or return low-confidence output.

## Acceptance criteria

- [ ] Results include a short explanation that stays grounded in the normalized job data
- [ ] The app falls back to basic skill-match search if AI ranking or explanation is unavailable
- [ ] Fallback mode is clearly labeled in the UI
- [ ] The fallback experience still shows useful ranked jobs instead of only an error state
- [ ] Explanation and fallback behavior are implemented outside the Streamlit layer where possible

## Blocked by

- Blocked by Issue 2
- Blocked by Issue 3

## User stories addressed

- User story 8
- User story 9
- User story 13
- User story 14
- User story 25

---

## Issue 5: Curated Data Quality and ETL Automation

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Harden the curated data pipeline so normalized job data remains a reliable product asset. The ETL process should validate required fields, normalize titles and skill-related fields through the shared taxonomy, generate structured silver records, and run consistently in automation.

This slice should ensure that search and AI features are powered by trustworthy structured data instead of brittle raw records.

## Acceptance criteria

- [ ] The ETL process validates required fields and fails clearly on invalid raw records
- [ ] The pipeline produces normalized silver job records with stable identifiers and structured fields
- [ ] A shared taxonomy is used consistently across normalization and search-related logic
- [ ] Automated workflow execution regenerates or validates the normalized data path
- [ ] The dataset remains local and curated, with no reliance on scraping or external job APIs

## Blocked by

None - can start immediately

## User stories addressed

- User story 19
- User story 20
- User story 21
- User story 22
- User story 23
- User story 29
- User story 30

---

## Issue 6: Contract Test Coverage for Search and AI

## Parent PRD

PRD: skill-based AI job assistant

## What to build

Add and stabilize contract-level tests for the core product behavior across ETL, search, ranking, explanation, and fallback behavior. Tests should focus on externally visible behavior and protect the system from regressions as the app evolves.

This slice should lock in the expected contracts for the search experience without overfitting to implementation details or prompt wording.

## Acceptance criteria

- [ ] ETL tests cover schema validation, normalization behavior, and structured output contracts
- [ ] Search and ranking tests cover known inputs, ordering behavior, and match detail outputs
- [ ] AI-facing tests cover explanation structure, cited matched skills, and fallback behavior
- [ ] Tests focus on public behavior rather than internal implementation details
- [ ] The suite can run in automation as part of the project workflow

## Blocked by

- Blocked by Issue 1
- Blocked by Issue 2
- Blocked by Issue 3
- Blocked by Issue 4
- Blocked by Issue 5

## User stories addressed

- User story 24
- User story 25
- User story 28
- User story 31

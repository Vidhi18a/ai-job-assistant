import streamlit as st

from app.ai import search_jobs, search_jobs_from_summary


def format_percent(score: float) -> str:
    return f"{round(score * 100)}%"


def match_strength(score: float) -> str:
    if score >= 0.5:
        return "Strong match"
    if score >= 0.2:
        return "Moderate match"
    return "Low match"


st.title("AI Job Assistant")
st.write("Search curated data and AI roles using skills or a short background summary.")

search_mode = st.radio(
    "Choose search mode",
    ("Skills", "Background summary"),
    horizontal=True,
)

skill_query = ""
summary_query = ""

if search_mode == "Skills":
    skill_query = st.text_input(
        "Enter skills separated by commas",
        placeholder="python, sql, machine learning",
    )
else:
    summary_query = st.text_area(
        "Describe your background in a few sentences",
        placeholder="I have worked with Python, SQL, dashboards, and ETL workflows for analytics teams.",
        height=120,
    )

if st.button("Search"):
    query = skill_query if search_mode == "Skills" else summary_query

    if not query.strip():
        st.error("Please enter a search query.")
    else:
        matches = search_jobs(query) if search_mode == "Skills" else search_jobs_from_summary(query)

        if not matches:
            st.warning("No matching jobs were found for that search.")
        else:
            st.success(f"Found {len(matches)} matching job(s).")
            if search_mode == "Background summary":
                mode_label = matches[0]["ranking_mode"]
                if mode_label == "fallback":
                    st.info("AI-assisted ranking is unavailable. Showing fallback skill-match results.")
                else:
                    st.info("Showing AI-assisted ranking based on your background summary.")

            for match in matches:
                st.subheader(match["title"])
                st.caption(
                    f"{match_strength(match['score'])} - Relevance: {format_percent(match['score'])}"
                )
                st.write(f"Matched skills: {', '.join(match['matched_skills']) or 'None'}")
                st.write(f"Missing skills: {', '.join(match['missing_skills']) or 'None'}")
                st.write(f"Explanation: {match['explanation']}")
                if search_mode == "Background summary":
                    st.write(
                        "Cited matched skills: "
                        + (
                            ", ".join(match.get("ai_ranking", {}).get("cited_skills", match["matched_skills"]))
                            or "None"
                        )
                    )

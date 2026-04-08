import streamlit as st
from ai import find_jobs_by_skill

st.title("AI Job Assistant 💼")

st.write("Find jobs based on your skills")

skill = st.text_input("Enter a skill (e.g., python, react):")

if st.button("Search"):
    if skill:
        jobs = find_jobs_by_skill(skill)
        
        if jobs:
            st.success("Jobs found:")
            for job in jobs:
                st.write("•", job)
        else:
            st.warning("No jobs found for this skill")
    else:
        st.error("Please enter a skill")
        # UI improvement
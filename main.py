import streamlit as st
from resume_parser import extract_text, extract_entities
from job_matcher import compute_similarity
from ranker import rank_candidates
from database import insert_candidate, get_all_candidates, init_db
from jd_scraper import extract_job_description_from_url

#Initialize database
init_db()

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("AI Resume Screener")

# --- Job Description Input ---
job_url = st.text_input("Paste a job description URL:")
job_desc = st.text_area("Paste the job description here (or leave blank to use URL):")

if not job_desc and job_url:
    with st.spinner("Fetching job description from URL..."):
        try:
            job_desc = extract_job_description_from_url(job_url)
            st.success("Job description loaded from URL.")
            st.text_area("Fetched Job Description:", value=job_desc, height=250)
        except Exception as e:
            st.error(f"Error fetching from URL: {e}")

# --- Resume Upload ---
uploaded_files = st.file_uploader("Upload resume PDFs", type=["pdf"], accept_multiple_files=True)

# --- Analysis ---
if st.button("Analyze", key="analyze_button") and job_desc:
    candidates = []

    for file in uploaded_files:
        try:
            text = extract_text(file)
            ents = extract_entities(text)
            score = compute_similarity(text, job_desc)
            insert_candidate(file.name, ents, score)
            candidates.append((file.name, ents, score))
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    ranked = rank_candidates(candidates)

    st.subheader("📊 Ranked Candidates")
    for name, ents, score in ranked:
        percentage_score = round(score * 100)
        st.markdown(f"**{name}** — Match Score: {percentage_score}%")
        st.json(ents)

elif st.button("Analyze", key="analyze_button_disabled") and not job_desc:
    st.warning("Please enter or load a job description first.")
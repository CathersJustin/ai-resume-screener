import streamlit as st
from resume_parser import extract_text, extract_entities
from job_matcher import compute_similarity
from ranker import rank_candidates
from database import insert_candidate, get_all_candidates
from jd_scraper import extract_job_description_from_url

st.title("AI Resume Screener")

job_url = st.text_input("Or paste a job description URL:")
job_desc = st.text_area("Paste the job description here (or leave blank to use URL):")

if not job_desc and job_url:
    with st.spinner("Fetching job description..."):
        try:
            job_desc = extract_job_description_from_url(job_url)
            st.success("Job description loaded from URL.")
            st.text_area("Fetched Job Description:", value=job_desc, height=250)
        except Exception as e:
            st.error(f"Could not extract job description from URL: {e}")

uploaded_files = st.file_uploader("Upload resume PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("Analyze") and job_desc:
    candidates = []

    for file in uploaded_files:
        text = extract_text(file)
        ents = extract_entities(text)
        score = compute_similarity(text, job_desc)
        insert_candidate(file.name, ents, score)
        candidates.append((file.name, ents, score))

    ranked = rank_candidates(candidates)

    st.subheader("Ranked Candidates")
    for name, ents, score in ranked:
        st.markdown(f"**{name}** — Score: {score:.2f}")
        st.json(ents)
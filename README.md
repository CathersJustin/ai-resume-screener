# ai-resume-screener
AI resume screener project

A smart resume screening tool that uses NLP to extract resume details and compare them against a job description (manual or via job URL). It ranks candidates based on similarity and provides a streamlined evaluation interface.

## Features
- Extracts skills and organizations from resumes
- Accepts job description input via text or URL (LinkedIn/Indeed)
- Ranks candidates by semantic similarity
- Stores data in SQLite

## How to Run
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run main.py
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_entities(text):
    doc = nlp(text)
    return {
        "PERSON": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "ORG": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "EDUCATION": [ent.text for ent in doc.ents if ent.label_ == "EDUCATION"],
        "SKILLS": list(set(token.text.lower() for token in doc if token.pos_ == "NOUN" and len(token.text) > 3))
    }
import pdfplumber
import spacy
import re

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# --- Keyword lists ---
KNOWN_SKILLS = {
    "python", "pandas", "numpy", "sql", "mysql", "postgresql", "mongodb",
    "tensorflow", "keras", "pytorch", "scikit-learn", "matplotlib", "seaborn",
    "power bi", "tableau", "excel", "git", "github", "azure", "aws",
    "linux", "visual studio", "jupyter", "spark", "hadoop", "xgboost",
    "nlp", "ml", "machine learning", "data science", "javascript", "java",
    "html", "css", "php", "r", "bash", "xampp", "netbeans", "vmware"
}

DEGREE_KEYWORDS = [
    "b.s.", "bachelor", "m.s.", "master", "ph.d", "degree", "nanodegree",
    "computer science", "data science", "biology", "chemistry", "engineering",
    "artificial intelligence", "ai", "udacity", "eku", "college", "university"
]

def extract_text(file):
    """Extract full text from a PDF file using pdfplumber."""
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])


def extract_entities(text):
    """Extract PERSON, TECH_SKILLS, and DEGREES from resume text."""
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "TECH_SKILLS": [],
        "DEGREES": []
    }

    # --- PERSON ---
    top_lines = text.strip().split('\n')[:5]
    for line in top_lines:
        line_clean = line.strip()
        if "Justin Cathers" in line_clean:
            entities["PERSON"].append("Justin Cathers")
            break
        match = re.fullmatch(r"[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}", line_clean)
        if match:
            entities["PERSON"].append(match.group())
            break

    if not entities["PERSON"]:
        if "justin cathers" in text.lower() or "justincathers" in text.lower():
            entities["PERSON"].append("Justin Cathers")

    # --- TECH_SKILLS ---
    text_lower = text.lower()
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            entities["TECH_SKILLS"].append(skill.title())

    # --- DEGREES ---
    for line in text.split('\n'):
        line_strip = line.strip()
        line_lower = line_strip.lower()

        if (
            any(deg in line_lower for deg in DEGREE_KEYWORDS) and
            any(term in line_lower for term in ["b.s", "bachelor", "m.s", "master", "ph.d", "nanodegree", "college", "university", "eku", "udacity"]) and
            not any(bad in line_lower for bad in ["@", "|", "present", "ongoing", "project", "summary", "experience", "technician"]) and
            not line_strip.startswith(("•", "-")) and
            4 <= len(line_strip.split()) <= 15
        ):
            entities["DEGREES"].append(line_strip)

    # --- Deduplicate and sort ---
    for key in entities:
        entities[key] = sorted(list(set(entities[key])))

    return entities
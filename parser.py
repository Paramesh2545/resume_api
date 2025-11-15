import re
import spacy
nlp = spacy.load("en_core_web_sm")
from typing import Optional
# ------- SKILLS DICTIONARY -------
TECH_SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "react", "node", "express", "nextjs", "django", "flask", "fastapi",
    "html", "css", "tailwind", "bootstrap",
    "sql", "mysql", "postgres", "mongodb",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "time management", "public speaking", "critical thinking"
]

SECTION_HEADERS = {
    "education": ["education", "academic background", "academics"],
    "experience": ["experience", "work experience", "employment", "professional experience"],
    "projects": ["projects", "personal projects", "academic projects"],
    "skills": ["skills", "technical skills", "core skills"],
    "certifications": ["certifications", "licenses"],
    "achievements": ["achievements", "accomplishments", "awards"],
    "summary": ["summary", "objective", "profile"]
}

#--------detect section----------

def detect_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = None

    for line in lines:
        line_clean = line.strip().lower()

        # Check if this line is a header
        for section_name, keywords in SECTION_HEADERS.items():
            if any(keyword in line_clean for keyword in keywords):
                current_section = section_name
                sections[current_section] = []
                break

        # If inside a section, add lines
        if current_section and line.strip() != "":
            sections[current_section].append(line.strip())

    return sections


# -------- EXTRACT EMAIL --------
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


# -------- EXTRACT PHONE --------
def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,15}", text)
    return match.group(0) if match else None


# -------- EXTRACT NAME (VERY BASIC) --------
import re

def extract_name(raw_text: str) -> Optional[str]:
    # Split into lines and keep only non-empty ones
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if not lines:
        return None

    # Take only the top few lines (header area)
    header_lines = lines[:5]

    # Stop at the line where contact info starts (email, phone, links)
    name_candidates = []
    for line in header_lines:
        lower = line.lower()
        if (
            "@" in lower or
            "linkedin.com" in lower or
            "github.com" in lower or
            "http://" in lower or
            "https://" in lower or
            "+91" in lower or
            "phone" in lower or
            "mobile" in lower
        ):
            break
        name_candidates.append(line)

    # If nothing was captured before contact info, just fall back to the first line
    if not name_candidates:
        name_line = header_lines[0]
    else:
        # Usually name is in the first line of the header
        name_line = name_candidates[0]

    # Normalize spaces (but don't remove them!)
    name_line = re.sub(r"\s+", " ", name_line).strip()

    return name_line if name_line else None


# -------- EXTRACT EDUCATION --------
education_keywords = [
    "B.Tech", "B.E", "Bachelor", "BSc", "M.Tech", "M.E", "Master",
    "MBA", "10th", "12th", "Intermediate", "High School"
]

def extract_education(text):
    lines = text.split("\n")
    edu_lines = [line.strip() for line in lines 
                 if any(k.lower() in line.lower() for k in education_keywords)]
    return edu_lines


# -------- EXTRACT EXPERIENCE --------
experience_keywords = [
    "experience", "intern", "developer", "engineer", 
    "project", "worked", "company", "role"
]

def extract_experience(text):
    lines = text.split("\n")
    exp_lines = [line.strip() for line in lines
                 if any(k.lower() in line.lower() for k in experience_keywords)]
    return exp_lines
 

#----Extract skills----------
def extract_skills(text):
    text_lower = text.lower()
    print("hello this is extract skills function")
    detected_tech = [skill for skill in TECH_SKILLS if skill in text_lower]
    detected_soft = [skill for skill in SOFT_SKILLS if skill in text_lower]

    return {
        "technical_skills": detected_tech,
        "soft_skills": detected_soft
    }



def extract_using_spacy(text):
    doc = nlp(text)
    names = []
    orgs = []
    dates = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)
        elif ent.label_ == "DATE":
            dates.append(ent.text)

    return {
        "spacy_names": names[:3],      # top 3 names from resume
        "spacy_organizations": orgs,   # colleges, companies
        "spacy_dates": dates
    }



def parse_resume_text(text):
    # -------- BASIC PARSER --------
    basic_details = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }

    # -------- AI PARSER --------
    ai_details = extract_using_spacy(text)

    # -------- SKILLS --------
    skill_details = extract_skills(text)

    # -------- SECTION DETECTION --------
    section_details = detect_sections(text)

    # -------- MERGE EVERYTHING --------
    final_output = {
        "sections": section_details,
        "basic_extraction": basic_details,
        "ai_extraction": ai_details,
        "skills_extraction": skill_details,
        "combined_best_guess": {
            "name": ai_details["spacy_names"][0] if ai_details["spacy_names"] else basic_details["name"],
            "email": basic_details["email"],
            "phone": basic_details["phone"],
            "skills": {
                "technical": skill_details["technical_skills"],
                "soft": skill_details["soft_skills"]
            },
            "education": section_details.get("education", basic_details["education"]),
            "experience": section_details.get("experience", basic_details["experience"]),
            "projects": section_details.get("projects", []),
            "certifications": section_details.get("certifications", []),
            "achievements": section_details.get("achievements", []),
            "summary": section_details.get("summary", [])
        }
    }

    return final_output

import re
import numpy as np
from scipy.sparse import hstack
from model_loader import model_loader

COMMON_SKILLS = [
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "node", "django", "flask",
    "spring", "machine learning", "deep learning", "nlp", "computer vision",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd", "jenkins",
    "agile", "scrum", "project management", "leadership", "communication",
    "linux", "bash", "powershell", "excel", "powerbi", "tableau", "cfa", "cpa",
    "marketing", "sales", "seo", "sem", "content creation", "design", "ui/ux",
    "photoshop", "illustrator", "figma", "sketch", "invision", "autocad",
    "solidworks", "matlab", "r", "sas", "spss", "stata", "econometrics",
    "financial modeling", "accounting", "audit", "tax", "legal", "hr",
    "recruiting", "training", "customer service", "operations", "logistics",
    "supply chain", "manufacturing", "nursing", "patient care", "emr", "epic",
    "cerner", "meditech", "allscripts", "cpr", "bls", "acls", "pals", "nrp",
    "teaching", "curriculum development", "lesson planning", "classroom management",
    "special education", "esl", "bilingual", "translation", "interpretation",
    "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "hadoop", "spark", "kafka", "elasticsearch"
]

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skill_count(text):
    text_lower = text.lower()
    count = 0
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            count += 1
    return count

def extract_word_count(text):
    return len(text.split())

def extract_experience_years(text):
    text_lower = text.lower()
    patterns = [
        r'(\d+)\+?\s*(?:-\s*\d+\s*)?years?(?:\s+of)?\s+experience',
        r'(\d+)\+?\s*(?:-\s*\d+\s*)?yrs?(?:\s+of)?\s+exp',
        r'experience.*?:.*?(?:over\s+)?(\d+)\s+years?'
    ]
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            try:
                years = int(match)
                if years > max_years and years < 50:
                    max_years = years
            except ValueError:
                pass
    return max_years

def get_prediction_results(resume_text):
    model = model_loader.model
    vectorizer = model_loader.vectorizer

    if model is None or vectorizer is None:
        return {"error": "Model not loaded"}

    cleaned = clean_text(resume_text)
    skill_count = extract_skill_count(cleaned)
    word_count = extract_word_count(cleaned)
    experience_years = extract_experience_years(cleaned)
    skill_exp_ratio = skill_count / max(experience_years, 1)

    num_features = np.array([[skill_count, word_count, experience_years, skill_exp_ratio]])
    tfidf_features = vectorizer.transform([cleaned])
    X = hstack([tfidf_features, num_features])

    prediction_code = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    confidence = float(proba[prediction_code])

    prediction_label = "Genuine" if prediction_code == 0 else "Fake"
    
    # Suspicious logic
    if 0.45 < confidence < 0.65:
        prediction_label = "Suspicious"

    # Issues analysis
    issues = []
    if skill_count > 15:
        issues.append("Unusually high number of technologies listed")
    if skill_exp_ratio > 7:
        issues.append("Extremely high skill-to-experience ratio")
    if word_count < 50:
        issues.append("Resume text is very short")
    if experience_years > 40:
        issues.append("Claimed experience exceeds realistic career timeline")
    if experience_years == 0 and skill_count > 5:
        issues.append("High skill count for zero mentioned years of experience")

    return {
        "prediction": prediction_label,
        "confidence": confidence,
        "issues": issues,
        "details": {
            "skill_count": skill_count,
            "word_count": word_count,
            "experience_years": experience_years,
            "skill_experience_ratio": round(skill_exp_ratio, 2)
        }
    }

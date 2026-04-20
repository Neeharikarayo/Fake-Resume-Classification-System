import numpy as np
from scipy.sparse import hstack, csr_matrix
from app.model_loader import model_loader
import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year

COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php",
    "go", "rust", "kotlin", "swift", "scala", "perl", "r", "matlab",
    "html", "css", "react", "angular", "vue", "svelte", "next", "nuxt",
    "bootstrap", "tailwind", "graphql", "rest", "jquery",
    "node", "django", "flask", "fastapi", "spring", "express", "rails", "laravel",
    "asp net", "grpc", "sql", "nosql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
    "oracle", "sqlite", "dynamodb", "elasticsearch", "neo4j", "bigquery",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "circleci", "helm", "prometheus", "grafana",
    "machine learning", "deep learning", "nlp", "computer vision", "data science",
    "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "huggingface", "transformers", "xgboost", "lightgbm",
    "hadoop", "spark", "kafka", "airflow", "dbt",
    "git", "ci/cd", "linux", "bash", "powershell", "excel", "powerbi",
    "tableau", "jira", "confluence", "figma", "photoshop", "illustrator",
    "agile", "scrum", "kanban", "project management", "leadership", "communication",
    "ui/ux", "design", "product management",
    "cfa", "cpa", "financial modeling", "accounting", "audit", "tax",
    "marketing", "sales", "seo", "sem", "content creation",
    "nursing", "patient care", "emr", "epic", "cerner", "meditech",
    "allscripts", "cpr", "bls", "acls",
    "teaching", "curriculum development", "lesson planning", "classroom management",
    "special education", "esl", "bilingual", "translation",
    "recruiting", "training", "customer service", "operations", "logistics",
    "supply chain", "manufacturing",
]

TOO_MANY_SKILLS_THRESHOLD = 20
HIGH_SKILL_EXP_RATIO      = 5.0
SUSPICIOUS_EXP_YEARS      = 30

def _ensure_nltk():
    import nltk
    resources = {
        "corpora/stopwords": "stopwords",
        "corpora/wordnet":   "wordnet",
        "corpora/omw-1.4":  "omw-1.4",
    }
    for path, pkg in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)

_ensure_nltk()

from nltk.corpus import stopwords as _sw
from nltk.stem import WordNetLemmatizer as _WNL
_STOP_WORDS = set(_sw.words("english"))
_LEMMATIZER = _WNL()

def clean_text(text: str) -> str:
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [
        _LEMMATIZER.lemmatize(tok)
        for tok in text.split()
        if tok not in _STOP_WORDS and len(tok) > 1
    ]
    return " ".join(tokens)

def extract_skill_count(text: str) -> int:
    text_lower = text.lower()
    return sum(1 for skill in COMMON_SKILLS if re.search(r"\b" + re.escape(skill) + r"\b", text_lower))

def extract_word_count(text: str) -> int:
    return len(text.split())

def extract_experience_years(text: str) -> int:
    text_lower = text.lower()
    patterns = [
        r"(\d+)\+?\s*(?:-\s*\d+\s*)?years?\s+(?:of\s+)?experience",
        r"(\d+)\+?\s*(?:-\s*\d+\s*)?yrs?\s+(?:of\s+)?exp",
        r"experience\s*[:\-]?\s*(?:over\s+)?(\d+)\s+years?",
    ]
    max_years = 0
    for pattern in patterns:
        for match in re.findall(pattern, text_lower):
            try:
                y = int(match)
                if 0 < y < 50 and y > max_years: max_years = y
            except ValueError:
                pass
    return max_years

def extract_graduation_year(text: str) -> int:
    text_lower = text.lower()
    edu_keywords = ["graduated", "graduation", "degree", "bachelor", "master", "phd", "mba", "b.s", "m.s", "university", "college"]
    years = []
    for kw in edu_keywords:
        for m in re.finditer(re.escape(kw), text_lower):
            start = max(0, m.start() - 120)
            end = min(len(text_lower), m.end() + 120)
            for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", text_lower[start:end]):
                yr = int(yr_str)
                if 1980 <= yr <= CURRENT_YEAR: years.append(yr)
    if not years:
        for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", text_lower):
            yr = int(yr_str)
            if 1980 <= yr <= CURRENT_YEAR: years.append(yr)
    return max(years) if years else 0

def detect_issues(skill_count, experience_years, graduation_year, skill_exp_ratio, timeline_issue, too_many_skills, raw_text):
    issues = []
    if timeline_issue:
        possible = CURRENT_YEAR - graduation_year if graduation_year else "?"
        issues.append(f"Experience mismatch with graduation year (claimed {experience_years} yrs, but only ~{possible} yrs possible since {graduation_year})")
    if too_many_skills: issues.append(f"Too many technologies listed ({skill_count} skills > {TOO_MANY_SKILLS_THRESHOLD} threshold)")
    if experience_years > SUSPICIOUS_EXP_YEARS: issues.append(f"Unrealistically high experience claim ({experience_years} years)")
    if skill_exp_ratio > HIGH_SKILL_EXP_RATIO and experience_years > 0: issues.append(f"Suspiciously high skills-per-year ratio ({skill_exp_ratio:.1f} skills/yr)")
    
    hype_phrases = ["expert in everything", "all skills", "every technology", "world class", "fortune 500", "ceo cto cfo", "master of all", "phd from mit", "harvard stanford"]
    raw_lower = raw_text.lower()
    for phrase in hype_phrases:
        if phrase in raw_lower:
            issues.append(f"Exaggerated language detected: \"{phrase}\"")
            break
    return issues

class PredictionService:
    def predict(self, resume_text: str):
        if model_loader.model is None or model_loader.vectorizer is None or model_loader.scaler is None:
            return {"error": "Service models not initialized. Make sure you have models in the root folder."}

        cleaned = clean_text(resume_text)
        skill_count = extract_skill_count(cleaned)
        word_count = extract_word_count(cleaned)
        experience_years = extract_experience_years(cleaned)
        graduation_year = extract_graduation_year(cleaned)
        skill_exp_ratio = skill_count / max(experience_years, 1)
        timeline_issue = int(experience_years > (CURRENT_YEAR - graduation_year) + 1) if graduation_year and experience_years else 0
        too_many_skills = int(skill_count > TOO_MANY_SKILLS_THRESHOLD)

        num_features_raw = np.array([[skill_count, word_count, experience_years, graduation_year, skill_exp_ratio, timeline_issue, too_many_skills]])
        num_features_sc = model_loader.scaler.transform(num_features_raw)
        tfidf_features = model_loader.vectorizer.transform([cleaned])
        X = hstack([tfidf_features, csr_matrix(num_features_sc)])

        prediction_code = int(model_loader.model.predict(X)[0])
        
        try:
            proba = model_loader.model.predict_proba(X)[0]
            confidence = float(proba[prediction_code]) if prediction_code < len(proba) else 0.8
        except:
            confidence = None

        issues = detect_issues(skill_count, experience_years, graduation_year, skill_exp_ratio, timeline_issue, too_many_skills, resume_text)

        # Apply Rule-Based Overrides
        if timeline_issue or experience_years > SUSPICIOUS_EXP_YEARS or too_many_skills:
            prediction_code = 1
            confidence = 0.99 if not confidence else max(0.95, confidence)
        elif len(issues) > 0 and prediction_code == 0:
            prediction_code = 2
            confidence = 0.85

        if prediction_code == 0:
            prediction_label = "Genuine"
        elif prediction_code == 1:
            prediction_label = "Fake"
        else:
            prediction_label = "Suspicious"

        return {
            "prediction": prediction_label,
            "confidence": round(confidence, 4) if confidence else None,
            "issues": issues,
            "details": {
                "skill_count": skill_count,
                "word_count": word_count,
                "experience_years": experience_years,
                "graduation_year": graduation_year,
                "skill_experience_ratio": round(skill_exp_ratio, 2),
                "timeline_issue": bool(timeline_issue),
                "too_many_skills": bool(too_many_skills)
            }
        }

prediction_service = PredictionService()

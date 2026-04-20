#!/usr/bin/env python3
"""
Step 5: Prediction System  [IMPROVED]
- Load saved best model, TF-IDF vectorizer, feature scaler, and metadata
- Clean & vectorize new resume text (same pipeline as training)
- Extract 7 numerical features
- Predict label (Genuine / Fake) with confidence score
- Return structured output:
    {
        "prediction": "Fake",
        "confidence": 0.84,
        "issues": [
            "Experience mismatch with graduation year",
            "Too many technologies listed (>20)"
        ]
    }
- Includes demo samples and interactive mode
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
import re
import json
import joblib
import numpy as np
from datetime import datetime
from scipy.sparse import hstack, csr_matrix

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH      = os.path.join(BASE_DIR, "fake_resume_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
SCALER_PATH     = os.path.join(BASE_DIR, "feature_scaler.pkl")
METADATA_PATH   = os.path.join(BASE_DIR, "model_metadata.json")

CURRENT_YEAR = datetime.now().year   # 2026

# ─── Skill List (must match 02_feature_extraction.py) ─────────────────────────
COMMON_SKILLS = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php",
    "go", "rust", "kotlin", "swift", "scala", "perl", "r", "matlab",
    # Web / frontend
    "html", "css", "react", "angular", "vue", "svelte", "next", "nuxt",
    "bootstrap", "tailwind", "graphql", "rest", "jquery",
    # Backend / frameworks
    "node", "django", "flask", "fastapi", "spring", "express", "rails", "laravel",
    "asp net", "grpc",
    # Databases
    "sql", "nosql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
    "oracle", "sqlite", "dynamodb", "elasticsearch", "neo4j", "bigquery",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "circleci", "helm", "prometheus", "grafana",
    # Data & ML
    "machine learning", "deep learning", "nlp", "computer vision", "data science",
    "tensorflow", "keras", "pytorch", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "huggingface", "transformers", "xgboost", "lightgbm",
    "hadoop", "spark", "kafka", "airflow", "dbt",
    # General tools
    "git", "ci/cd", "linux", "bash", "powershell", "excel", "powerbi",
    "tableau", "jira", "confluence", "figma", "photoshop", "illustrator",
    # Methodologies & soft skills
    "agile", "scrum", "kanban", "project management", "leadership", "communication",
    "ui/ux", "design", "product management",
    # Finance / Business
    "cfa", "cpa", "financial modeling", "accounting", "audit", "tax",
    "marketing", "sales", "seo", "sem", "content creation",
    # Healthcare
    "nursing", "patient care", "emr", "epic", "cerner", "meditech",
    "allscripts", "cpr", "bls", "acls",
    # Education
    "teaching", "curriculum development", "lesson planning", "classroom management",
    "special education", "esl", "bilingual", "translation",
    # HR / Ops
    "recruiting", "training", "customer service", "operations", "logistics",
    "supply chain", "manufacturing",
]

TOO_MANY_SKILLS_THRESHOLD = 20
HIGH_SKILL_EXP_RATIO      = 5.0
SUSPICIOUS_EXP_YEARS      = 30

# ─── Text Cleaning (must match 01_data_preprocessing.py) ─────────────────────
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
    """Lowercase → strip specials → collapse spaces → remove stopwords → lemmatize."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [
        _LEMMATIZER.lemmatize(tok)
        for tok in text.split()
        if tok not in _STOP_WORDS and len(tok) > 1
    ]
    return " ".join(tokens)


# ─── Feature Extraction (must match 02_feature_extraction.py) ─────────────────
def extract_skill_count(text: str) -> int:
    text_lower = text.lower()
    return sum(
        1 for skill in COMMON_SKILLS
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower)
    )


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
                years = int(match)
                if years > max_years and years < 50:
                    max_years = years
            except ValueError:
                pass
    return max_years


def extract_graduation_year(text: str) -> int:
    text_lower = text.lower()
    edu_keywords = [
        "graduated", "graduation", "degree", "bachelor", "master", "phd",
        "mba", "b.s", "m.s", "b.tech", "m.tech", "university", "college",
        "institute", "school", "b.e", "m.e", "b.sc", "m.sc",
    ]
    years_found = []
    for kw in edu_keywords:
        for m in re.finditer(re.escape(kw), text_lower):
            start   = max(0, m.start() - 120)
            end     = min(len(text_lower), m.end() + 120)
            snippet = text_lower[start:end]
            for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", snippet):
                yr = int(yr_str)
                if 1980 <= yr <= CURRENT_YEAR:
                    years_found.append(yr)
    if not years_found:
        for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", text_lower):
            yr = int(yr_str)
            if 1980 <= yr <= CURRENT_YEAR:
                years_found.append(yr)
    return max(years_found) if years_found else 0


def extract_timeline_issue(experience_years: int, graduation_year: int) -> int:
    if graduation_year == 0 or experience_years == 0:
        return 0
    return int(experience_years > (CURRENT_YEAR - graduation_year) + 1)


def extract_too_many_skills(skill_count: int) -> int:
    return int(skill_count > TOO_MANY_SKILLS_THRESHOLD)


# ─── Issue Detection ──────────────────────────────────────────────────────────
def detect_issues(
    skill_count: int,
    experience_years: int,
    graduation_year: int,
    skill_exp_ratio: float,
    timeline_issue: int,
    too_many_skills: int,
    raw_text: str,
) -> list:
    """
    Return a human-readable list of detected red flags in the resume.
    """
    issues = []

    if timeline_issue:
        possible = CURRENT_YEAR - graduation_year if graduation_year else "?"
        issues.append(
            f"Experience mismatch with graduation year "
            f"(claimed {experience_years} yrs, but only ~{possible} yrs possible since {graduation_year})"
        )

    if too_many_skills:
        issues.append(
            f"Too many technologies listed ({skill_count} skills > {TOO_MANY_SKILLS_THRESHOLD} threshold)"
        )

    if experience_years > SUSPICIOUS_EXP_YEARS:
        issues.append(
            f"Unrealistically high experience claim ({experience_years} years)"
        )

    if skill_exp_ratio > HIGH_SKILL_EXP_RATIO and experience_years > 0:
        issues.append(
            f"Suspiciously high skills-per-year ratio ({skill_exp_ratio:.1f} skills/yr)"
        )

    # Buzzword inflation: check for exaggerated language in raw text
    hype_phrases = [
        "expert in everything", "all skills", "every technology",
        "world class", "fortune 500", "ceo cto cfo", "best in the world",
        "master of all", "phd from mit", "harvard stanford",
    ]
    raw_lower = raw_text.lower()
    for phrase in hype_phrases:
        if phrase in raw_lower:
            issues.append(f"Exaggerated language detected: \"{phrase}\"")
            break  # report at most one hype-phrase hit

    return issues


# ─── Core Prediction Function ─────────────────────────────────────────────────
def predict_resume(resume_text: str, model=None, vectorizer=None, scaler=None):
    """
    Predict whether a resume is genuine or fake.

    Returns
    -------
    dict with keys:
        prediction  : str   ("Genuine" or "Fake")
        confidence  : float (probability of predicted class, 0-1)
        issues      : list  (detected red flags, empty if genuine / no issues)
        details     : dict  (raw extracted features for transparency)
    """
    # Load artifacts if not provided
    if model is None:
        model = joblib.load(MODEL_PATH)
    if vectorizer is None:
        vectorizer = joblib.load(VECTORIZER_PATH)
    if scaler is None:
        scaler = joblib.load(SCALER_PATH)

    # 1. Clean text
    cleaned = clean_text(resume_text)

    # 2. Extract numerical features
    skill_count      = extract_skill_count(cleaned)
    word_count       = extract_word_count(cleaned)
    experience_years = extract_experience_years(cleaned)
    graduation_year  = extract_graduation_year(cleaned)
    skill_exp_ratio  = skill_count / max(experience_years, 1)
    timeline_issue   = extract_timeline_issue(experience_years, graduation_year)
    too_many_skills  = extract_too_many_skills(skill_count)

    num_features_raw = np.array([[
        skill_count, word_count, experience_years, graduation_year,
        skill_exp_ratio, timeline_issue, too_many_skills
    ]])

    # 3. Scale numerical features
    num_features_sc = scaler.transform(num_features_raw)

    # 4. TF-IDF
    tfidf_features = vectorizer.transform([cleaned])

    # 5. Combine
    X = hstack([tfidf_features, csr_matrix(num_features_sc)])

    # 6. Predict
    prediction_code = int(model.predict(X)[0])
    prediction_label = "Genuine" if prediction_code == 0 else "Fake"

    # 7. Confidence
    try:
        proba      = model.predict_proba(X)[0]
        confidence = float(proba[prediction_code])
    except Exception:
        confidence = None

    # 8. Issue detection (always run, regardless of prediction)
    issues = detect_issues(
        skill_count, experience_years, graduation_year,
        skill_exp_ratio, timeline_issue, too_many_skills,
        resume_text,
    )

    return {
        "prediction": prediction_label,
        "confidence": round(confidence, 4) if confidence is not None else None,
        "issues":     issues,
        "details": {
            "skill_count":            skill_count,
            "word_count":             word_count,
            "experience_years":       experience_years,
            "graduation_year":        graduation_year,
            "skill_experience_ratio": round(skill_exp_ratio, 2),
            "timeline_issue":         bool(timeline_issue),
            "too_many_skills":        bool(too_many_skills),
        },
    }


# ─── Pretty Print Helper ──────────────────────────────────────────────────────
def print_result(result: dict, resume_snippet: str = ""):
    """Print prediction result in a readable, structured format."""
    banner = "🟢 GENUINE" if result["prediction"] == "Genuine" else "🔴 FAKE"
    print("─" * 55)
    if resume_snippet:
        snippet = resume_snippet.strip()[:120].replace("\n", " ")
        print(f"  Resume   : {snippet}...")
    print(f"  Result   : {banner}")
    if result["confidence"] is not None:
        print(f"  Confidence : {result['confidence']:.2%}")
    print()

    d = result["details"]
    print(f"  Features detected:")
    print(f"    skill_count       : {d['skill_count']}")
    print(f"    word_count        : {d['word_count']}")
    print(f"    experience_years  : {d['experience_years']}")
    print(f"    graduation_year   : {d['graduation_year'] or 'N/A'}")
    print(f"    skill/exp ratio   : {d['skill_experience_ratio']}")
    print(f"    timeline_issue    : {d['timeline_issue']}")
    print(f"    too_many_skills   : {d['too_many_skills']}")

    if result["issues"]:
        print(f"\n  ⚠  Detected Issues ({len(result['issues'])}):")
        for i, issue in enumerate(result["issues"], 1):
            print(f"    {i}. {issue}")
    else:
        print(f"\n  ✓  No major issues detected.")
    print("─" * 55)


def print_json(result: dict):
    """Print the clean structured JSON output."""
    out = {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "issues":     result["issues"],
    }
    print(json.dumps(out, indent=2))


# ─── Demo / Main ─────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  STEP 5: RESUME PREDICTION SYSTEM  [IMPROVED]")
    print("=" * 60)

    # Validate prerequisites
    for path, label in [
        (MODEL_PATH,      "fake_resume_model.pkl"),
        (VECTORIZER_PATH, "tfidf_vectorizer.pkl"),
        (SCALER_PATH,     "feature_scaler.pkl"),
    ]:
        if not os.path.exists(path):
            print(f"Error: '{label}' not found. Run the training pipeline first.")
            return

    print("Loading model artifacts ...")
    model      = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    scaler     = joblib.load(SCALER_PATH)
    print(f"  Model type : {type(model).__name__}")

    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH) as f:
            meta = json.load(f)
        print(f"  Trained on : {meta.get('training_date', 'N/A')}")
        print(f"  Best model : {meta.get('best_model', 'N/A')}")
    print("  Ready!\n")

    # ── Sample 1: Genuine Resume ──────────────────────────────────────────────
    sample_genuine = """
    John Smith
    Software Engineer | San Francisco, CA | john.smith@email.com

    Summary:
    Experienced software engineer with 5 years of experience building scalable
    web applications. Proficient in Python, JavaScript, React, and AWS.
    Strong background in agile methodologies and CI/CD pipelines.

    Experience:
    Senior Software Engineer - TechCorp Inc. (2021 - Present)
    - Led development of microservices architecture using Python and Docker
    - Implemented CI/CD pipelines with Jenkins and Kubernetes
    - Mentored junior developers and conducted code reviews

    Software Engineer - DataFlow LLC (2019 - 2021)
    - Built RESTful APIs using Django and Flask
    - Designed and maintained PostgreSQL and MongoDB databases
    - Collaborated with cross-functional teams using Agile/Scrum methodology

    Education:
    B.S. Computer Science - Stanford University, 2019

    Skills:
    Python, JavaScript, React, Node.js, Django, Flask, AWS, Docker,
    Kubernetes, Git, SQL, CI/CD, Agile, Scrum
    """

    # ── Sample 2: Fake Resume ─────────────────────────────────────────────────
    sample_fake = """
    EXPERT PROFESSIONAL - ALL SKILLS MASTER

    I am expert in everything. 20 years experience in all technologies.
    Python Java JavaScript TypeScript C++ Ruby PHP SQL NoSQL HTML CSS
    React Angular Vue Svelte Node Django Flask FastAPI Spring AWS Azure GCP
    Docker Kubernetes Terraform Ansible Jenkins GitHub Actions Helm Prometheus.
    Machine Learning Deep Learning NLP Computer Vision TensorFlow Keras PyTorch
    Scikit-learn Pandas NumPy Hadoop Spark Kafka Airflow XGBoost LightGBM.

    I worked at Google Apple Microsoft Amazon Facebook Netflix Tesla SpaceX.
    I have PhD from MIT Harvard Stanford simultaneously.
    I am CEO CTO CFO of Fortune 500 company since 2000.
    I made $10 million in revenue for every company in 6 months.
    World class developer architect manager leader. Expert in everything.

    Education:
    Graduated 2018 from Harvard University
    """

    # ── Run Predictions ───────────────────────────────────────────────────────
    print(">> SAMPLE 1: Genuine Resume")
    result1 = predict_resume(sample_genuine, model, vectorizer, scaler)
    print_result(result1, sample_genuine.strip())
    print("\n  JSON Output:")
    print_json(result1)

    print(f"\n{'=' * 60}")
    print(">> SAMPLE 2: Suspicious / Fake Resume")
    result2 = predict_resume(sample_fake, model, vectorizer, scaler)
    print_result(result2, sample_fake.strip())
    print("\n  JSON Output:")
    print_json(result2)

    # ── Interactive Mode ──────────────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("  INTERACTIVE MODE")
    print("  Paste resume text and press Enter twice to predict.")
    print("  Type 'quit' to exit.")
    print("=" * 60)

    while True:
        print("\nEnter resume text (or 'quit'):")
        lines = []
        try:
            while True:
                line = input()
                if line.strip().lower() == "quit":
                    print("Goodbye!")
                    return
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
        except EOFError:
            break

        text = "\n".join(lines).strip()
        if not text:
            print("  (empty input, skipping)")
            continue

        result = predict_resume(text, model, vectorizer, scaler)
        print_result(result, text)
        print("\n  JSON Output:")
        print_json(result)

    print("\n" + "=" * 60)
    print("  DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()

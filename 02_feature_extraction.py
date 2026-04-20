#!/usr/bin/env python3
"""
Step 2: Feature Extraction  [IMPROVED]
- Load cleaned_resumes.csv
- Extract features:
    skill_count            : number of predefined skills found
    word_count             : total words in resume
    experience_years       : max years of experience explicitly mentioned
    graduation_year        : most recent graduation year found in text
    skill_experience_ratio : skills per year of experience
    timeline_issue         : 1 if claimed experience > years since graduation
    too_many_skills        : 1 if skill_count > 20 (unrealistic breadth)
- Save as features_dataset.csv
"""

import pandas as pd
import re
import os
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV  = os.path.join(BASE_DIR, "cleaned_resumes.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "features_dataset.csv")

CURRENT_YEAR = datetime.now().year   # 2026

# ─── Expanded Skill List ──────────────────────────────────────────────────────
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


# ─── Feature Extraction Functions ─────────────────────────────────────────────
def extract_skill_count(text: str) -> int:
    """Count how many skills from COMMON_SKILLS appear in the text."""
    if not isinstance(text, str):
        return 0
    text_lower = text.lower()
    return sum(
        1 for skill in COMMON_SKILLS
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower)
    )


def extract_word_count(text: str) -> int:
    if not isinstance(text, str):
        return 0
    return len(text.split())


def extract_experience_years(text: str) -> int:
    """Extract the maximum claimed years of experience from text."""
    if not isinstance(text, str):
        return 0
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
    """
    Extract the most recent graduation / degree year.
    Looks for 4-digit years (1980–CURRENT_YEAR) near education keywords.
    Returns 0 if not found.
    """
    if not isinstance(text, str):
        return 0
    text_lower = text.lower()

    edu_keywords = [
        "graduated", "graduation", "degree", "bachelor", "master", "phd",
        "mba", "b.s", "m.s", "b.tech", "m.tech", "university", "college",
        "institute", "school", "b.e", "m.e", "b.sc", "m.sc",
    ]

    # Find all years in a ±120-char window around any education keyword
    years_found = []
    for kw in edu_keywords:
        for m in re.finditer(re.escape(kw), text_lower):
            start = max(0, m.start() - 120)
            end   = min(len(text_lower), m.end() + 120)
            snippet = text_lower[start:end]
            for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", snippet):
                yr = int(yr_str)
                if 1980 <= yr <= CURRENT_YEAR:
                    years_found.append(yr)

    # Also try a broader scan for 4-digit years that look like graduation years
    if not years_found:
        for yr_str in re.findall(r"\b(19[89]\d|20[0-2]\d)\b", text_lower):
            yr = int(yr_str)
            if 1980 <= yr <= CURRENT_YEAR:
                years_found.append(yr)

    return max(years_found) if years_found else 0


def extract_timeline_issue(experience_years: int, graduation_year: int) -> int:
    """
    Flag a timeline inconsistency.
    A person can only have worked since graduation, so:
        experience_years should NOT exceed (CURRENT_YEAR - graduation_year)
    Returns 1 (issue detected) or 0.
    """
    if graduation_year == 0 or experience_years == 0:
        return 0
    possible_max = CURRENT_YEAR - graduation_year
    # Allow a 1-year grace period for rounding / part-time work during studies
    return int(experience_years > possible_max + 1)


def extract_too_many_skills(skill_count: int, threshold: int = 20) -> int:
    """Flag resumes that list an unrealistic number of technologies."""
    return int(skill_count > threshold)


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  STEP 2: FEATURE EXTRACTION  [IMPROVED]")
    print("=" * 60)

    if not os.path.exists(INPUT_CSV):
        print(f"Error: Required input file '{INPUT_CSV}' not found.")
        print("Please run 01_data_preprocessing.py first.")
        return

    print(f"Loading {INPUT_CSV} ...")
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")
    df["resume_text"] = df["resume_text"].fillna("")
    print(f"Found {len(df)} resumes.")

    print("\nExtracting features (this may take a moment) ...")

    print("  - skill_count ...")
    df["skill_count"] = df["resume_text"].apply(extract_skill_count)

    print("  - word_count ...")
    df["word_count"] = df["resume_text"].apply(extract_word_count)

    print("  - experience_years ...")
    df["experience_years"] = df["resume_text"].apply(extract_experience_years)

    print("  - graduation_year ...")
    df["graduation_year"] = df["resume_text"].apply(extract_graduation_year)

    print("  - skill_experience_ratio ...")
    df["skill_experience_ratio"] = df["skill_count"] / df["experience_years"].apply(lambda x: max(1, x))

    print("  - timeline_issue ...")
    df["timeline_issue"] = df.apply(
        lambda row: extract_timeline_issue(row["experience_years"], row["graduation_year"]),
        axis=1,
    )

    print("  - too_many_skills ...")
    df["too_many_skills"] = df["skill_count"].apply(extract_too_many_skills)

    # ── Summary ────────────────────────────────────────────────────────────────
    feat_cols = [
        "skill_count", "word_count", "experience_years", "graduation_year",
        "skill_experience_ratio", "timeline_issue", "too_many_skills",
    ]
    print("\nFeature Extraction Summary:")
    print(df[feat_cols].describe().round(2))

    print(f"\n  timeline_issue  flagged: {df['timeline_issue'].sum()} resumes")
    print(f"  too_many_skills flagged: {df['too_many_skills'].sum()} resumes")

    # ── Save ───────────────────────────────────────────────────────────────────
    out_cols = ["resume_text"] + feat_cols + ["label"]
    df[out_cols].to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\n  ✓ Saved to: {OUTPUT_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Step 1: Data Preprocessing  [IMPROVED]
- Load 3 datasets (Resume.csv, NER JSON, Synthetic Resumes)
- Extract resume text
- Clean text:
    1. Convert to lowercase
    2. Remove special characters
    3. Remove extra whitespace
    4. Remove stopwords (NLTK)
    5. Lemmatize words (NLTK WordNetLemmatizer)
- Create unified dataset with columns: resume_text, label
- Save as cleaned_resumes.csv
"""

import pandas as pd
import json
import re
import os

# ─── NLTK Setup ───────────────────────────────────────────────────────────────
import nltk

def _ensure_nltk():
    """Download required NLTK data if not already present."""
    resources = {
        "corpora/stopwords":   "stopwords",
        "corpora/wordnet":     "wordnet",
        "corpora/omw-1.4":    "omw-1.4",
        "tokenizers/punkt":   "punkt",
    }
    for path, pkg in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            print(f"  Downloading NLTK resource: {pkg} ...")
            nltk.download(pkg, quiet=True)

_ensure_nltk()

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOP_WORDS  = set(stopwords.words("english"))
LEMMATIZER  = WordNetLemmatizer()

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
RESUME_CSV    = os.path.join(BASE_DIR, "Resume", "Resume.csv")
NER_JSON      = os.path.join(BASE_DIR, "Entity Recognition in Resumes.json")
SYNTHETIC_CSV = os.path.join(BASE_DIR, "synthetic_resumes.csv")
OUTPUT_CSV    = os.path.join(BASE_DIR, "cleaned_resumes.csv")


# ─── Text Cleaning ────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """
    Full cleaning pipeline:
      1. Lowercase
      2. Remove special characters (keep alphanumeric + spaces)
      3. Collapse whitespace
      4. Remove English stopwords
      5. Lemmatize each word
    Returns a single cleaned string.
    """
    if not isinstance(text, str):
        return ""

    # Step 1 – lowercase
    text = text.lower()

    # Step 2 – remove special characters (keep a-z, 0-9, spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Step 3 – collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 4 & 5 – tokenise, remove stopwords, lemmatize
    tokens = [
        LEMMATIZER.lemmatize(tok)
        for tok in text.split()
        if tok not in STOP_WORDS and len(tok) > 1
    ]

    return " ".join(tokens)


# ─── Load Dataset 1: Resume.csv (genuine resumes) ─────────────────────────────
def load_resume_csv():
    """Load real resumes from Resume.csv and assign label=0."""
    print("[1/3] Loading Resume.csv ...")
    df = pd.read_csv(RESUME_CSV, encoding="utf-8", on_bad_lines="skip")
    print(f"      Found {len(df)} rows. Columns: {list(df.columns)}")

    text_col = "Resume_str" if "Resume_str" in df.columns else df.columns[1]
    resumes  = df[text_col].dropna().apply(clean_text).tolist()

    result = pd.DataFrame({"resume_text": resumes, "label": 0})
    result = result[result["resume_text"].str.len() > 50]
    print(f"      After cleaning: {len(result)} genuine resumes")
    return result


# ─── Load Dataset 2: NER JSON (genuine resumes) ───────────────────────────────
def load_ner_json():
    """Load NER dataset (real resumes) and assign label=0."""
    print("[2/3] Loading Entity Recognition in Resumes.json ...")
    records = []
    with open(NER_JSON, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj     = json.loads(line)
                content = obj.get("content", "")
                if content and len(content) > 50:
                    records.append(clean_text(content))
            except json.JSONDecodeError:
                continue

    result = pd.DataFrame({"resume_text": records, "label": 0})
    result = result[result["resume_text"].str.len() > 50]
    print(f"      After cleaning: {len(result)} genuine resumes from NER dataset")
    return result


# ─── Load Dataset 3: Synthetic Resumes ─────────────────────────────────────────
def load_synthetic_csv():
    """Load synthetic resumes, keep only label 0 and 1."""
    print("[3/3] Loading synthetic_resumes.csv ...")
    df = pd.read_csv(SYNTHETIC_CSV, encoding="utf-8")
    print(f"      Found {len(df)} rows. Label distribution:")
    print(f"      {df['label'].value_counts().to_dict()}")

    df = df[df["label"].isin([0, 1])].copy()
    df["resume_text"] = df["resume_text"].apply(clean_text)
    df = df[df["resume_text"].str.len() > 50]

    result = df[["resume_text", "label"]].reset_index(drop=True)
    print(f"      After filtering (labels 0,1) and cleaning: {len(result)} resumes")
    return result


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  STEP 1: DATA PREPROCESSING  [IMPROVED]")
    print("=" * 60)

    df_resume    = load_resume_csv()
    df_ner       = load_ner_json()
    df_synthetic = load_synthetic_csv()

    print("\n--- Merging datasets ---")
    combined = pd.concat([df_resume, df_ner, df_synthetic], ignore_index=True)

    # Remove duplicates
    combined.drop_duplicates(subset=["resume_text"], inplace=True)
    combined.reset_index(drop=True, inplace=True)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  UNIFIED DATASET SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total resumes   : {len(combined)}")
    print(f"  Label distribution:")
    print(f"    Genuine (0)   : {len(combined[combined['label'] == 0])}")
    print(f"    Fake    (1)   : {len(combined[combined['label'] == 1])}")
    print(f"  Avg text length : {combined['resume_text'].str.len().mean():.0f} chars")
    print(f"  Preprocessing   : lowercase → strip specials → stopwords → lemmatize")

    combined.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\n  ✓ Saved to: {OUTPUT_CSV}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Step 3: Model Training  [IMPROVED]
- Load features_dataset.csv
- TF-IDF with ngram_range=(1,2) and max_features=10,000
- Combine TF-IDF with 7 numerical features
- Check class balance; apply SMOTE if needed
- 5-fold stratified cross-validation for each model
- Train: Logistic Regression, Random Forest, XGBoost
- Select best model by mean CV F1-score
- Save best model, vectorizer, and model_metadata.json
"""

import pandas as pd
import numpy as np
import os
import json
import joblib
from datetime import datetime
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV      = os.path.join(BASE_DIR, "features_dataset.csv")
MODEL_PATH     = os.path.join(BASE_DIR, "fake_resume_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
SCALER_PATH    = os.path.join(BASE_DIR, "feature_scaler.pkl")
METADATA_PATH  = os.path.join(BASE_DIR, "model_metadata.json")

NUM_FEATURE_COLS = [
    "skill_count", "word_count", "experience_years", "graduation_year",
    "skill_experience_ratio", "timeline_issue", "too_many_skills",
]

TFIDF_PARAMS = {
    "max_features": 10000,
    "ngram_range": (1, 2),
    "stop_words": "english",
    "sublinear_tf": True,           # log-scale TF — helps with long resumes
    "min_df": 2,                    # ignore very rare terms
}

N_CV_FOLDS = 5


# ─── SMOTE helper ─────────────────────────────────────────────────────────────
def apply_smote_if_needed(X, y, imbalance_threshold=0.40):
    """
    If the minority class is < imbalance_threshold of the data, apply SMOTE.
    Returns (X_resampled, y_resampled, was_applied: bool).
    X must be a dense array or convertible.
    """
    counts = np.bincount(y)
    minority_ratio = counts.min() / counts.sum()
    print(f"\n  Class balance — minority ratio: {minority_ratio:.2%}")

    if minority_ratio < imbalance_threshold:
        print(f"  Imbalanced dataset detected (< {imbalance_threshold:.0%}).")
        try:
            from imblearn.over_sampling import SMOTE
            print("  Applying SMOTE oversampling ...")
            sm = SMOTE(random_state=42)
            X_res, y_res = sm.fit_resample(X, y)
            new_counts = np.bincount(y_res)
            print(f"  After SMOTE — class counts: {dict(enumerate(new_counts))}")
            return X_res, y_res, True
        except ImportError:
            print("  [WARNING] imbalanced-learn not installed. Skipping SMOTE.")
            print("  Install with:  pip install imbalanced-learn")
    else:
        print("  Dataset is sufficiently balanced. Skipping SMOTE.")

    return X, y, False


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  STEP 3: MODEL TRAINING  [IMPROVED]")
    print("=" * 60)

    if not os.path.exists(INPUT_CSV):
        print(f"Error: '{INPUT_CSV}' not found. Run 02_feature_extraction.py first.")
        return

    # ── 1. Load data ──────────────────────────────────────────────────────────
    print(f"Loading {INPUT_CSV} ...")
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")
    df["resume_text"] = df["resume_text"].fillna("")

    # Fill any NaN in numerical features with 0
    df[NUM_FEATURE_COLS] = df[NUM_FEATURE_COLS].fillna(0)

    X_text = df["resume_text"]
    X_num  = df[NUM_FEATURE_COLS].values.astype(float)
    y      = df["label"].values

    print(f"  Dataset size  : {len(df)}")
    print(f"  Class counts  : {dict(enumerate(np.bincount(y)))}")
    print(f"  Num features  : {NUM_FEATURE_COLS}")

    # ── 2. Train / test split ─────────────────────────────────────────────────
    print("\nSplitting data (80% train, 20% test, stratified) ...")
    (X_text_train, X_text_test,
     X_num_train,  X_num_test,
     y_train,      y_test) = train_test_split(
        X_text, X_num, y,
        test_size=0.2, random_state=42, stratify=y,
    )

    # ── 3. TF-IDF vectorisation ───────────────────────────────────────────────
    print(f"\nFitting TF-IDF (max_features={TFIDF_PARAMS['max_features']}, "
          f"ngram_range={TFIDF_PARAMS['ngram_range']}) ...")
    vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
    X_tfidf_train = vectorizer.fit_transform(X_text_train)
    X_tfidf_test  = vectorizer.transform(X_text_test)

    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"  ✓ TF-IDF vocabulary size : {len(vectorizer.vocabulary_)}")
    print(f"  ✓ Saved vectorizer       : {VECTORIZER_PATH}")

    # ── 4. Scale numerical features ───────────────────────────────────────────
    print("\nScaling numerical features (StandardScaler) ...")
    scaler = StandardScaler()
    X_num_train_sc = scaler.fit_transform(X_num_train)
    X_num_test_sc  = scaler.transform(X_num_test)

    joblib.dump(scaler, SCALER_PATH)
    print(f"  ✓ Saved scaler : {SCALER_PATH}")

    # ── 5. Combine features ───────────────────────────────────────────────────
    X_train_full = hstack([X_tfidf_train, csr_matrix(X_num_train_sc)])
    X_test_full  = hstack([X_tfidf_test,  csr_matrix(X_num_test_sc)])
    print(f"\n  Combined feature space : {X_train_full.shape[1]} dimensions")

    # ── 6. SMOTE (applied to training set only) ───────────────────────────────
    X_train_dense = X_train_full.toarray()          # SMOTE needs dense
    X_train_dense, y_train_res, smote_applied = apply_smote_if_needed(
        X_train_dense, y_train
    )
    # Convert back to sparse for memory efficiency during training
    X_train_sparse = csr_matrix(X_train_dense)

    # ── 7. Model definitions ──────────────────────────────────────────────────
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight="balanced", C=1.0, random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, class_weight="balanced",
            max_depth=None, min_samples_leaf=2,
            random_state=42, n_jobs=-1,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=200, learning_rate=0.1, max_depth=6,
            subsample=0.8, colsample_bytree=0.8,
            eval_metric="logloss", random_state=42, n_jobs=-1,
            use_label_encoder=False,
        ),
    }

    # ── 8. 5-Fold cross-validation ─────────────────────────────────────────────
    print(f"\n{'─' * 60}")
    print(f"  {N_CV_FOLDS}-FOLD STRATIFIED CROSS-VALIDATION")
    print(f"{'─' * 60}")

    cv_scoring = ["accuracy", "precision", "recall", "f1"]
    cv  = StratifiedKFold(n_splits=N_CV_FOLDS, shuffle=True, random_state=42)
    cv_results_all = {}

    best_cv_f1    = -1.0
    best_model_name = ""
    best_model      = None

    for name, model in models.items():
        print(f"\n  [{name}]")
        scores = cross_validate(
            model, X_train_sparse, y_train_res,
            cv=cv, scoring=cv_scoring, n_jobs=-1,
        )
        mean_f1  = scores["test_f1"].mean()
        std_f1   = scores["test_f1"].std()
        mean_acc = scores["test_accuracy"].mean()
        mean_prec = scores["test_precision"].mean()
        mean_rec  = scores["test_recall"].mean()

        print(f"    Accuracy  : {mean_acc:.4f}")
        print(f"    Precision : {mean_prec:.4f}")
        print(f"    Recall    : {mean_rec:.4f}")
        print(f"    F1-Score  : {mean_f1:.4f} ± {std_f1:.4f}")

        cv_results_all[name] = {
            "cv_accuracy_mean":  round(mean_acc,  4),
            "cv_precision_mean": round(mean_prec, 4),
            "cv_recall_mean":    round(mean_rec,  4),
            "cv_f1_mean":        round(mean_f1,   4),
            "cv_f1_std":         round(std_f1,    4),
        }

        if mean_f1 > best_cv_f1:
            best_cv_f1      = mean_f1
            best_model_name = name
            best_model      = model

    print(f"\n{'─' * 60}")
    print(f"  Best by CV F1: {best_model_name} (F1 = {best_cv_f1:.4f})")

    # ── 9. Retrain best model on full training set + evaluate on holdout ───────
    print(f"\n  Retraining {best_model_name} on full training set ...")
    best_model.fit(X_train_sparse, y_train_res)

    y_pred = best_model.predict(X_test_full)
    holdout = {
        "accuracy":  round(accuracy_score(y_test, y_pred),  4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall":    round(recall_score(y_test, y_pred, zero_division=0),    4),
        "f1":        round(f1_score(y_test, y_pred, zero_division=0),        4),
    }
    print(f"\n  Holdout test-set metrics:")
    for k, v in holdout.items():
        print(f"    {k.capitalize():<12}: {v:.4f}")

    # ── 10. Save model & metadata ─────────────────────────────────────────────
    joblib.dump(best_model, MODEL_PATH)
    print(f"\n  ✓ Saved best model : {MODEL_PATH}")

    metadata = {
        "best_model":         best_model_name,
        "training_date":      datetime.now().isoformat(timespec="seconds"),
        "n_training_samples": int(len(y_train_res)),
        "smote_applied":      smote_applied,
        "tfidf_params":       {k: str(v) for k, v in TFIDF_PARAMS.items()},
        "num_feature_cols":   NUM_FEATURE_COLS,
        "cv_folds":           N_CV_FOLDS,
        "cv_results":         cv_results_all,
        "holdout_metrics":    holdout,
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  ✓ Saved metadata   : {METADATA_PATH}")
    print("=" * 60)

    # ── 11. Model leaderboard ─────────────────────────────────────────────────
    print("\n  MODEL LEADERBOARD (by CV F1-Score):")
    print(f"  {'Model':<25} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>8}")
    print(f"  {'-'*25} {'-'*9} {'-'*10} {'-'*8} {'-'*8}")
    sorted_models = sorted(cv_results_all.items(),
                           key=lambda x: x[1]["cv_f1_mean"], reverse=True)
    for name, res in sorted_models:
        marker = " ← BEST" if name == best_model_name else ""
        print(
            f"  {name:<25} "
            f"{res['cv_accuracy_mean']:>9.4f} "
            f"{res['cv_precision_mean']:>10.4f} "
            f"{res['cv_recall_mean']:>8.4f} "
            f"{res['cv_f1_mean']:>8.4f}"
            f"{marker}"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()

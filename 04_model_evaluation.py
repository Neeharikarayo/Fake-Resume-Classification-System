#!/usr/bin/env python3
"""
Step 4: Model Evaluation  [IMPROVED]
- Reload saved best model, TF-IDF vectorizer, scaler, and model_metadata.json
- Reconstruct the same 80/20 stratified split (random_state=42)
- Full classification metrics (Accuracy, Precision, Recall, F1, AUC)
- 5-fold CV results table (loaded from metadata)
- Confusion matrix — both text and visual (normalized + raw)
- ROC curve plot saved to roc_curve.png
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import pandas as pd
import numpy as np
import os
import json
import joblib
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV       = os.path.join(BASE_DIR, "features_dataset.csv")
MODEL_PATH      = os.path.join(BASE_DIR, "fake_resume_model.pkl")
VEC_PATH        = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
SCALER_PATH     = os.path.join(BASE_DIR, "feature_scaler.pkl")
METADATA_PATH   = os.path.join(BASE_DIR, "model_metadata.json")
CM_IMG          = os.path.join(BASE_DIR, "confusion_matrix.png")
ROC_IMG         = os.path.join(BASE_DIR, "roc_curve.png")
METRICS_CSV     = os.path.join(BASE_DIR, "evaluation_metrics.csv")

NUM_FEATURE_COLS = [
    "skill_count", "word_count", "experience_years", "graduation_year",
    "skill_experience_ratio", "timeline_issue", "too_many_skills",
]


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  STEP 4: MODEL EVALUATION  [IMPROVED]")
    print("=" * 60)

    # ── 1. Validate prerequisites ─────────────────────────────────────────────
    required = [
        (INPUT_CSV,     "features_dataset.csv"),
        (MODEL_PATH,    "fake_resume_model.pkl"),
        (VEC_PATH,      "tfidf_vectorizer.pkl"),
        (SCALER_PATH,   "feature_scaler.pkl"),
    ]
    for path, label in required:
        if not os.path.exists(path):
            print(f"Error: '{label}' not found at {path}")
            print("Please run the previous pipeline steps first.")
            return

    # ── 2. Load data ──────────────────────────────────────────────────────────
    print(f"Loading {INPUT_CSV} ...")
    df = pd.read_csv(INPUT_CSV, encoding="utf-8")
    df["resume_text"] = df["resume_text"].fillna("")
    df[NUM_FEATURE_COLS] = df[NUM_FEATURE_COLS].fillna(0)

    X_text = df["resume_text"]
    X_num  = df[NUM_FEATURE_COLS].values.astype(float)
    y      = df["label"].values
    print(f"  Total resumes : {len(df)}")
    print(f"  Class counts  : {dict(zip(*np.unique(y, return_counts=True)))}")

    # ── 3. Load model, vectorizer, scaler ────────────────────────────────────
    print("\nLoading model artifacts ...")
    model      = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
    scaler     = joblib.load(SCALER_PATH)
    print(f"  Model type : {type(model).__name__}")

    # ── 4. Recreate the exact 80/20 split ─────────────────────────────────────
    print("\nRecreating 80/20 stratified split (random_state=42) ...")
    (X_text_train, X_text_test,
     X_num_train,  X_num_test,
     y_train,      y_test) = train_test_split(
        X_text, X_num, y,
        test_size=0.2, random_state=42, stratify=y,
    )

    # ── 5. Transform test features ────────────────────────────────────────────
    X_tfidf_test  = vectorizer.transform(X_text_test)
    X_num_test_sc = scaler.transform(X_num_test)
    X_test        = hstack([X_tfidf_test, csr_matrix(X_num_test_sc)])

    # ── 6. Predictions ────────────────────────────────────────────────────────
    y_pred  = model.predict(X_test)
    try:
        y_proba = model.predict_proba(X_test)[:, 1]
        has_proba = True
    except Exception:
        y_proba   = None
        has_proba = False

    # ── 7. Holdout metrics ────────────────────────────────────────────────────
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec  = recall_score(y_test, y_pred, zero_division=0)
    f1   = f1_score(y_test, y_pred, zero_division=0)
    auc  = roc_auc_score(y_test, y_proba) if has_proba else None

    print("\n" + "─" * 50)
    print("  HOLDOUT TEST-SET METRICS")
    print("─" * 50)
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-Score  : {f1:.4f}")
    if auc is not None:
        print(f"  ROC AUC   : {auc:.4f}")
    print("─" * 50)

    # Save metrics CSV
    rows = [
        {"Metric": "Accuracy",  "Holdout": acc},
        {"Metric": "Precision", "Holdout": prec},
        {"Metric": "Recall",    "Holdout": rec},
        {"Metric": "F1-Score",  "Holdout": f1},
    ]
    if auc is not None:
        rows.append({"Metric": "ROC AUC", "Holdout": auc})
    pd.DataFrame(rows).to_csv(METRICS_CSV, index=False)
    print(f"  [OK] Metrics saved to {METRICS_CSV}")

    # ── 8. Cross-validation results table (from metadata) ────────────────────
    if os.path.exists(METADATA_PATH):
        print("\n" + "─" * 50)
        print(f"  {5}-FOLD CROSS-VALIDATION RESULTS (from training)")
        print("─" * 50)
        with open(METADATA_PATH) as f:
            meta = json.load(f)
        cv_res = meta.get("cv_results", {})
        print(f"  {'Model':<25} {'Acc':>7} {'Prec':>7} {'Rec':>7} {'F1':>8}")
        print(f"  {'-'*25} {'-'*7} {'-'*7} {'-'*7} {'-'*8}")
        for mname, res in cv_res.items():
            marker = " *" if mname == meta.get("best_model") else ""
            print(
                f"  {mname:<25} "
                f"{res['cv_accuracy_mean']:>7.4f} "
                f"{res['cv_precision_mean']:>7.4f} "
                f"{res['cv_recall_mean']:>7.4f} "
                f"{res['cv_f1_mean']:>7.4f} ± {res['cv_f1_std']:.4f}"
                f"{marker}"
            )
        print(f"  (* = selected best model: {meta.get('best_model', 'N/A')})")
        print("─" * 50)

    # ── 9. Classification report ──────────────────────────────────────────────
    print("\n  CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred,
                                target_names=["Genuine (0)", "Fake (1)"]))

    # ── 10. Confusion matrix — text ───────────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print("  CONFUSION MATRIX")
    print(f"  {'':>14}  Pred Genuine  Pred Fake")
    print(f"  {'True Genuine':>14}  {cm[0][0]:>12}  {cm[0][1]:>9}")
    print(f"  {'True Fake':>14}  {cm[1][0]:>12}  {cm[1][1]:>9}")
    print(f"\n  True Positives  (correctly detected fake) : {tp}")
    print(f"  True Negatives  (correctly detected real) : {tn}")
    print(f"  False Positives (real flagged as fake)    : {fp}")
    print(f"  False Negatives (fake missed)             : {fn}")

    # ── 11. Visual confusion matrix + ROC curve (if matplotlib) ──────────────
    if HAS_PLOT:
        # --- Confusion matrix (raw + normalised side-by-side) ----------------
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Confusion Matrix — Best Model", fontsize=14, fontweight="bold")

        for ax, data, fmt, title in zip(
            axes,
            [cm, cm_norm],
            ["d", ".2%"],
            ["Raw Counts", "Normalised (row %)"],
        ):
            sns.heatmap(
                data, annot=True, fmt=fmt, cmap="Blues",
                xticklabels=["Genuine", "Fake"],
                yticklabels=["Genuine", "Fake"],
                ax=ax, linewidths=0.5,
            )
            ax.set_xlabel("Predicted Label", fontsize=11)
            ax.set_ylabel("True Label", fontsize=11)
            ax.set_title(title, fontsize=12)

        plt.tight_layout()
        plt.savefig(CM_IMG, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"\n  [OK] Confusion matrix plot saved to {CM_IMG}")

        # --- ROC curve -------------------------------------------------------
        if has_proba:
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.plot(fpr, tpr, color="#3b82f6", lw=2,
                    label=f"ROC curve (AUC = {auc:.4f})")
            ax.plot([0, 1], [0, 1], color="#9ca3af", linestyle="--", lw=1,
                    label="Random classifier")
            ax.fill_between(fpr, tpr, alpha=0.1, color="#3b82f6")
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel("False Positive Rate", fontsize=12)
            ax.set_ylabel("True Positive Rate", fontsize=12)
            ax.set_title("ROC Curve — Fake Resume Detection", fontsize=14,
                         fontweight="bold")
            ax.legend(loc="lower right", fontsize=11)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(ROC_IMG, dpi=150, bbox_inches="tight")
            plt.close(fig)
            print(f"  [OK] ROC curve saved to {ROC_IMG}")

    # ── 12. Error analysis ────────────────────────────────────────────────────
    print("\n" + "─" * 50)
    print("  ERROR ANALYSIS")
    print("─" * 50)

    test_df = pd.DataFrame({
        "resume_text":    X_text_test.values,
        "skill_count":    X_num_test[:, 0],
        "word_count":     X_num_test[:, 1],
        "experience_yrs": X_num_test[:, 2],
        "y_true":         y_test,
        "y_pred":         y_pred,
    })

    fn_df = test_df[(test_df["y_true"] == 1) & (test_df["y_pred"] == 0)]
    fp_df = test_df[(test_df["y_true"] == 0) & (test_df["y_pred"] == 1)]
    tp_df = test_df[(test_df["y_true"] == 1) & (test_df["y_pred"] == 1)]
    tn_df = test_df[(test_df["y_true"] == 0) & (test_df["y_pred"] == 0)]

    def _profile(group_df, label):
        if len(group_df) == 0:
            print(f"  {label}: 0 samples")
            return
        print(f"\n  {label} ({len(group_df)} samples):")
        print(f"    Avg word count       : {group_df['word_count'].mean():.1f}")
        print(f"    Avg skill count      : {group_df['skill_count'].mean():.1f}")
        print(f"    Avg experience years : {group_df['experience_yrs'].mean():.1f}")
        print(f"    Avg resume length    : {group_df['resume_text'].str.len().mean():.0f} chars")

    _profile(tp_df, "[OK] Correctly Detected FAKE  (True Positives)")
    _profile(fn_df, "[!!] Missed FAKE              (False Negatives)")
    _profile(tn_df, "[OK] Correctly Detected REAL  (True Negatives)")
    _profile(fp_df, "[!!] Real flagged as FAKE     (False Positives)")

    if fn_df.__len__() > 0:
        print("\n  Sample MISSED fake resumes (first 150 chars):")
        for i, (_, row) in enumerate(fn_df.head(3).iterrows()):
            print(f"    [{i+1}] {row['resume_text'][:150]} ...")

    if fp_df.__len__() > 0:
        print("\n  Sample genuines incorrectly flagged as fake:")
        for i, (_, row) in enumerate(fp_df.head(3).iterrows()):
            print(f"    [{i+1}] {row['resume_text'][:150]} ...")

    print("\n" + "=" * 60)
    print("  EVALUATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

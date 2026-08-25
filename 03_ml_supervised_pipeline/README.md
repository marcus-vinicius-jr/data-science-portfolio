# ML Supervised Pipeline — Customer Churn Prediction

> 🇧🇷 Versão em português: [README_pt-BR.md](README_pt-BR.md)
> Part of [data-science-portfolio](../README.md)
> Notebook: [03_ml_supervised_pipeline.ipynb](notebooks/03_ml_supervised_pipeline.ipynb)
> Status: Completed
> [![CI - 03 ML Supervised Pipeline](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-03-ml-supervised-pipeline.yml/badge.svg)](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-03-ml-supervised-pipeline.yml)

This project builds an end-to-end **supervised machine learning pipeline** on the
Kaggle **Telco Customer Churn** dataset, framed from the perspective of a Head of
Customer Success / Retention who needs to know which customers are likely to
cancel, why, and which model best supports a retention campaign.

The notebook combines:
- modeling hypotheses stated **before** training any model,
- data understanding and cleaning (a known `TotalCharges` type issue),
- feature engineering (derived engagement and tenure features) and a
  `ColumnTransformer` + `Pipeline` preprocessing setup,
- model comparison — Logistic Regression vs. two tree-based ensembles (Random
  Forest, Gradient Boosting) — with the Random Forest tuned via a full
  best-practice hyperparameter checklist (`RandomizedSearchCV`) and the other
  two via `GridSearchCV`,
- evaluation beyond accuracy (confusion matrix, ROC/PR curves, F1, threshold
  tuning) and model interpretability,
- and business storytelling: findings, implications and recommended actions.

---

## Business Question

Which customers are likely to churn, which factors drive that decision most, and
which model gives the best precision/recall trade-off to guide targeted
retention actions?

---

## Dataset

- Source: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Coverage: 7,043 telecom customers, 21 columns
- Target: `Churn` (binary), imbalanced — 26.54% positive class
- Key variables: `tenure`, `Contract`, `InternetService`, `MonthlyCharges`,
  `TotalCharges`, plus service add-ons (`OnlineSecurity`, `TechSupport`, etc.)

Data is downloaded in the notebook via Kaggle API into `data/raw/`.

---

## Methodology Summary

1. Business context and modeling hypotheses
2. Data understanding and quality (`TotalCharges` blank-string issue at
   `tenure = 0`, target imbalance check)
3. Targeted EDA (churn vs. tenure, contract type, internet service)
4. Feature engineering (`TotalCharges` cleanup, derived `num_add_on_services`
   and `tenure_group`) and stratified 80/20 train/test split
5. Preprocessing (`ColumnTransformer`: scaling + one-hot encoding) and model
   comparison — Logistic Regression vs. Random Forest vs. Gradient Boosting,
   all tuned with `roc_auc` scoring under 5-fold stratified CV. Random Forest
   follows a full best-practice checklist covering `n_estimators`, `max_depth`,
   `min_samples_split`, `min_samples_leaf`, `max_features`, `bootstrap`,
   `ccp_alpha` and `criterion` — searched via `RandomizedSearchCV` (40 sampled
   combinations) since an exhaustive grid over that space is computationally
   impractical; Logistic Regression and Gradient Boosting use `GridSearchCV`
   over smaller grids
6. Evaluation beyond accuracy: confusion matrix, ROC-AUC, PR-AUC, F1, and
   decision-threshold analysis — including a per-customer **cost-benefit
   matrix** that converts the confusion matrix into expected monetary value
7. Interpretability: logistic regression coefficients vs. tree feature
   importances
8. Key insights and business storytelling
9. Conclusions and next steps

---

## Model Results (test set, n = 1,409)

| Model | Accuracy | Precision (churn) | Recall (churn) | F1 (churn) | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.733 | 0.498 | **0.791** | 0.612 | 0.842 | 0.636 |
| Random Forest | 0.755 | 0.526 | **0.794** | 0.633 | 0.843 | 0.651 |
| **Gradient Boosting** | **0.798** | **0.656** | 0.505 | 0.571 | **0.846** | **0.664** |

Gradient Boosting wins on ranking ability (ROC-AUC / PR-AUC) and accuracy, but
Logistic Regression and Random Forest — both trained with `class_weight='balanced'`
— win on churn recall at the default 0.5 threshold. Tuning the Gradient Boosting
decision threshold to 0.324 (F1-optimal) raises its recall from 0.505 to 0.757
and its F1 from 0.571 to 0.640.

**Random Forest hyperparameter search:** following a full best-practice
checklist (problem framing → data prep → split → hyperparameter design →
cross-validated search → final validation), `RandomizedSearchCV` sampled 40
combinations across `n_estimators`, `max_depth`, `min_samples_split`,
`min_samples_leaf`, `max_features`, `bootstrap`, `ccp_alpha` and `criterion`.
The winning configuration: `n_estimators=200`, `max_depth=15`,
`min_samples_split=2`, `min_samples_leaf=10`, `max_features='log2'`,
`criterion='gini'`, `bootstrap=True`, `ccp_alpha=0.0` (CV ROC-AUC 0.848 —
essentially tied with Gradient Boosting's 0.850 and ahead of Logistic
Regression's 0.846 under cross-validation).

---

## Hypotheses & Results

| # | Hypothesis | Result |
|---|---|---|
| H1 | Tree-based models outperform logistic regression in discriminative power | **Partially confirmed** — Gradient Boosting leads on ROC-AUC/PR-AUC, but at the default threshold its churn recall trails the class-weighted Logistic Regression / Random Forest by a wide margin |
| H2 | Logistic regression and tree-based models agree on the main churn drivers | **Confirmed** — `Contract`, `tenure` and `InternetService = Fiber optic` rank in the top 5 for both Logistic Regression and Gradient Boosting |
| H3 | Accuracy alone is a misleading metric given class imbalance | **Confirmed** — Gradient Boosting has the highest accuracy (0.798) but the lowest churn recall (0.505) of the three models |

---

## Cost-Benefit Analysis

A confusion matrix counts right/wrong predictions but says nothing about how
much each error costs or each catch is worth. Section 6.1 of the notebook
converts it into a **cost-benefit matrix**, valuing each cell using each test
customer's real `MonthlyCharges` instead of a flat average. Assumptions
(business judgment, not derived from data — stated explicitly so they can be
challenged):

| Cell | Condition | Value |
|---|---|---|
| True Negative | predicted stay, stayed | R$ 0 (no action) |
| False Positive | predicted churn, stayed | −1× `MonthlyCharges` (wasted retention offer) |
| False Negative | predicted stay, churned | −12× `MonthlyCharges` (lost future revenue) |
| True Positive | predicted churn, churned | 0.30 × 12× `MonthlyCharges` − 1× `MonthlyCharges` (30% retention success rate) |

**Unexpected finding:** at the default 0.5 threshold, **all three models
underperform the naive "contact every customer" baseline** (R$ +7,672 on the
test set) — Gradient Boosting's expected value is R$ −120,113, Random Forest
R$ −26,825, Logistic Regression R$ −20,730. None has high enough churn recall
at that threshold to offset how much a missed churner costs (12× a wasted
offer). A statistically strong model (ROC-AUC ≈ 0.84) can destroy more value
than a policy with no intelligence at all if deployed at its default threshold.

Sweeping the decision threshold by expected net value (not F1) for all three
models flips the picture: every model beats the "contact everyone" baseline
once recalibrated, and **the profit-optimal threshold is far more aggressive
than the F1-optimal one** (0.08 vs. 0.324 for Gradient Boosting).

| Model | Value @ 0.5 (R$) | Profit-optimal threshold | Value at that threshold (R$) |
|---|---|---|---|
| **Gradient Boosting** | −120,113 | **0.08** | **19,964** |
| Logistic Regression | −20,730 | 0.12 | 19,685 |
| Random Forest | −26,825 | 0.24 | 19,115 |

Gradient Boosting still wins once properly recalibrated, but by less than
1.5% over Logistic Regression and Random Forest — **all three are practically
tied** at their respective optimal thresholds, despite a visible ROC-AUC gap
between Gradient Boosting and the other two. The decision threshold, not the
algorithm choice, is the highest-leverage lever found in this analysis.

---

## Key Findings

- **Ranking ability and operating-point performance are not the same thing.**
  Gradient Boosting has the best ROC-AUC (0.846) and PR-AUC (0.664), but without
  class balancing its default-threshold recall on churn (0.505) is far below the
  balanced Logistic Regression (0.791) / Random Forest (0.794) — model selection
  by AUC alone would have picked the worst model for a retention use case.
- **Threshold tuning matters as much as model choice**: shifting the Gradient
  Boosting decision threshold from 0.5 to 0.324 (F1-optimal) lifts churn recall
  from 0.505 to 0.757, a deliberate precision-for-recall trade that fits a
  retention context where missing a churner is costlier than an unnecessary
  retention offer.
- **At its default threshold, every model destroys value relative to a naive
  "contact everyone" policy** under the cost-benefit assumptions in the
  section below (Gradient Boosting: R$ −120,113 vs. the baseline's R$ +7,672).
  Recalibrating the threshold by expected net value — not F1 — is what makes
  the models worth deploying at all (best case: R$ 19,964, Gradient Boosting
  @ threshold 0.08).
- **Contract type is the single strongest churn driver**: month-to-month
  customers churn at 42.7%, vs. 11.3% for one-year and 2.8% for two-year
  contracts.
- **Fiber optic internet customers churn at more than double the DSL rate**
  (41.9% vs. 19.0%), independent of contract type — worth investigating for
  price, service quality or competitive pressure.
- **Missing add-on services are a risk signal in the tree model**: lack of
  `OnlineSecurity` and `TechSupport` rank among Gradient Boosting's top
  predictors, alongside `tenure` and `Contract`.

---

## Final Model & Threshold Recommendation

Recommended operating point, chosen from the cost-benefit analysis rather
than from ROC-AUC alone:

- **Model:** Gradient Boosting
- **Decision threshold:** **0.08** (not the default 0.5, and not the
  F1-optimal 0.324 found in section 6.3 of the notebook)
- **Expected net value on the test set:** R$19,963.87, versus R$7,672.44 for
  the naive "contact everyone" baseline

Why this model and threshold:
- Gradient Boosting has the best cross-validated ROC-AUC (0.8497), though
  the margin over Random Forest (0.8481) and Logistic Regression (0.8464) is
  small, a near three-way statistical tie.
- Once every model is recalibrated to its own profit-optimal threshold,
  Gradient Boosting still wins, but by only **1.42%** over Logistic
  Regression (R$19,685.14 @ 0.12) and **4.44%** over Random Forest
  (R$19,114.98 @ 0.24). If interpretability matters more than this thin
  margin, Logistic Regression at threshold 0.12 is a defensible alternative.
- This model must **not** be deployed at the default 0.5 threshold: at that
  point it destroys R$120,113.14 in expected value relative to the naive
  baseline (see Cost-Benefit Analysis).

---

## Validation Snapshot

Recommended model performance at its cross-validation score and at both its
default and recommended operating points:

| Metric | CV (5-fold) | Test @ threshold 0.5 | Test @ threshold 0.08 (recommended) |
|---|---|---|---|
| ROC-AUC | 0.8497 | 0.8455 | threshold-independent |
| Accuracy | n/a | 0.7984 | 0.5798 |
| Precision (churn) | n/a | 0.6562 | 0.3843 |
| Recall (churn) | n/a | 0.5053 | 0.9679 |
| F1 (churn) | n/a | 0.5710 | 0.5502 |
| Expected net value (R$) | n/a | −120,113.14 | 19,963.87 |

At the recommended threshold, the model flags nearly every likely churner
(recall 96.8%) at the cost of much lower precision (38.4%) and accuracy
(58.0%) than the default threshold. That trade-off is intentional: given the
cost asymmetry in the cost-benefit matrix (a missed churner costs 12x a
wasted retention offer), the model should err heavily toward flagging.
Classification metrics alone make this operating point look worse than the
default threshold; only the cost-benefit view captures why it is actually
the better choice.

---

## Repository Structure

```text
03_ml_supervised_pipeline/
|-- data/                                    # gitignored
|   |-- raw/                                 # generated by Kaggle download in notebook
|   `-- processed/                           # reserved for derived datasets
|-- notebooks/
|   `-- 03_ml_supervised_pipeline.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## How to Run

1. Go to project folder:

```bash
cd 03_ml_supervised_pipeline
```

2. Create and activate a virtual environment (optional if you already use conda):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Kaggle API:
- Create token in Kaggle account settings.
- Save `kaggle.json` in:
  - Windows: `C:\Users\<YOUR_USER>\.kaggle\kaggle.json`
  - Linux/Mac: `~/.kaggle/kaggle.json`

5. Open and run:

```text
notebooks/03_ml_supervised_pipeline.ipynb
```

---

## Notes

- Do not commit credentials (`kaggle.json`) or virtual environment folders.
- The raw Telco Customer Churn CSV is downloaded locally and excluded via
  `.gitignore`; re-run the notebook to regenerate it.
- Gradient Boosting in scikit-learn has no native `class_weight` support, unlike
  Logistic Regression and Random Forest — this asymmetry is the direct cause of
  its lower default-threshold recall, and is addressed via threshold tuning
  rather than resampling in this iteration (see Next Steps in the notebook).
- All metrics reported are single-split test-set results (no nested CV); the
  notebook lists nested cross-validation as a follow-up for a less optimistic
  generalization estimate.
- The cost-benefit assumptions (1-month offer cost, 30% retention success
  rate, 12-month revenue horizon) are illustrative business judgment, not
  derived from the dataset — a sensitivity analysis across these assumptions
  is listed as a next step.
- **CI:** [`.github/workflows/ci-03-ml-supervised-pipeline.yml`](../.github/workflows/ci-03-ml-supervised-pipeline.yml)
  re-runs this notebook end-to-end on every push/PR touching this folder, to
  catch reproducibility regressions (dataset drift, deprecated library APIs).
  It downloads the dataset via the Kaggle API using `KAGGLE_USERNAME`/
  `KAGGLE_KEY` repository secrets — set those in the GitHub repo settings
  (Settings → Secrets and variables → Actions) for the workflow to run.

---

> Back to portfolio: [data-science-portfolio](../README.md)

# Text Classification with Keras — Twitter US Airline Sentiment

> 🇧🇷 Versão em português: [README_pt-BR.md](README_pt-BR.md)
> Part of [data-science-portfolio](../README.md)
> Notebook: [04_text_classification_keras.ipynb](notebooks/04_text_classification_keras.ipynb)
> Status: Completed
> [![CI - 04 Text Classification Keras](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-04-text-classification-keras.yml/badge.svg)](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-04-text-classification-keras.yml)

This project builds a **text classification pipeline with Keras** on the
Kaggle **Twitter US Airline Sentiment** dataset, framed from the perspective
of a Head of Digital Customer Experience / Social Media Command Center at a
major US airline who needs to triage the volume of tweets mentioning the
airline in near real time, instead of relying on manual review of every
@mention.

The notebook combines:
- modeling hypotheses stated **before** training any model,
- data understanding, quality checks (duplicate tweets, label noise) and
  targeted EDA (sentiment by airline, top complaint reasons, tweet length),
- a from-scratch text-cleaning pipeline with an explicit, negation-safe
  stopword list for the classic baseline,
- a **TF-IDF + Logistic Regression baseline** compared against two neural
  sequence models, **Embedding + LSTM** and **Embedding + 1D CNN**, built
  following an explicit six-step neural-network framework (data preparation,
  architecture, weight initialization, forward propagation, backpropagation,
  training) with an explicit overfitting check at every step,
- evaluation beyond accuracy (macro-F1, per-class precision/recall,
  confusion matrices, multiclass ROC-AUC),
- a business-decision threshold-tuning section reframing the 3-class problem
  as the binary "does this tweet need a human right now?" triage trigger,
  plus an exposure-weighted look at missed complaints using retweet count,
- interpretability for both the linear baseline (coefficients) and the
  neural embedding (nearest-neighbor words), and
- business storytelling: findings, implications and a final model/threshold
  recommendation.

---

## Business Question

Can the sentiment of a tweet mentioning the airline be classified accurately
enough to prioritize which tweets a live customer-service team should see
first, and which text-representation approach (bag-of-words vs. learned
embeddings) gives the best operating point for that triage decision?

---

## Dataset

- Source: [Twitter US Airline Sentiment (Crowdflower / Kaggle)](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)
- Coverage: 14,640 tweets directed at six US airlines (United, US Airways,
  American, Southwest, Delta, Virgin America); 14,485 after dropping 155
  exact duplicate `tweet_id` rows
- Target: `airline_sentiment` (3-class), imbalanced: negative 62.69%, neutral
  21.17%, positive 16.14%
- Key variables: `text` (the only model input), `airline`, `negativereason`
  (populated only for negative tweets), `retweet_count`,
  `airline_sentiment_confidence`

Data is downloaded in the notebook via the Kaggle API into `data/raw/`.

---

## Methodology Summary

1. Business context, persona and modeling hypotheses (H1-H3)
2. Data understanding and quality (missingness pattern, 155 duplicate
   `tweet_id` rows dropped, label-noise check on duplicate text)
3. Targeted EDA (sentiment by airline, top negative reasons, tweet length
   distribution)
4. Text cleaning (negation-safe stopword list, hashtag/mention handling) and
   a stratified 70/15/15 train/validation/test split
5. Baseline: TF-IDF + Logistic Regression, tuned via `GridSearchCV` under
   5-fold cross-validation scored on macro-F1
6. Deep learning: an explicit neural-network framework applied once, then
   two architectures built on top of it, Embedding + LSTM and Embedding + 1D
   CNN, both with `class_weight` for imbalance and `EarlyStopping` on
   validation loss
7. Model comparison and evaluation beyond accuracy (confusion matrices,
   per-class precision/recall/F1, macro-F1, macro ROC-AUC)
8. Business-decision threshold tuning (negative vs. not-negative triage) and
   an exposure-weighted (`retweet_count`) miss analysis
9. Interpretability (Logistic Regression coefficients; embedding
   nearest-neighbors)
10. Hypotheses & results, key findings, business storytelling
11. Conclusions and next steps

---

## Model Results (test set, n = 2,173)

| Model | Accuracy | Macro F1 | Weighted F1 | Macro ROC-AUC (OvR) |
|---|---|---|---|---|
| TF-IDF + Logistic Regression | 0.7607 | 0.7101 | 0.7668 | 0.8862 |
| **Embedding + LSTM** | **0.7911** | **0.7326** | **0.7913** | 0.8868 |
| Embedding + 1D CNN | 0.7713 | 0.7212 | 0.7752 | **0.8923** |

Embedding + LSTM wins on accuracy, macro-F1 and weighted-F1; Embedding + 1D
CNN wins on macro ROC-AUC, though the three ROC-AUC scores span only 0.006,
essentially a three-way tie on ranking ability even though macro-F1 clearly
separates the models.

**Why macro-F1, not weighted-F1 or accuracy, is the primary metric:**
weighted-F1 averages the three per-class F1 scores weighted by class size,
so it is dominated by the majority `negative` class and sits within 0.6
points of accuracy for every model (e.g. LSTM: weighted-F1 0.7913 vs.
accuracy 0.7911). Macro-F1 averages the three F1 scores unweighted, so the
much weaker `neutral` F1 (0.5994 to 0.6346 across models) pulls it down 5 to
6 points below accuracy/weighted-F1 for every model. That gap is exactly
what H2 is testing for: a metric that lets a weak minority class hide behind
a strong majority class would have made every model here look better than
it actually is on `neutral` tweets.

**Per-class recall** (the metric most exposed by the class imbalance):

| Class | TF-IDF + LogReg | Embedding + LSTM | Embedding + 1D CNN |
|---|---|---|---|
| negative | 0.8085 | 0.8701 | 0.8217 |
| neutral | 0.6652 | 0.6457 | 0.6391 |
| positive | 0.7000 | 0.6743 | 0.7486 |

Every model's weakest class is `neutral`, not `positive`, even though
`positive` is the smaller class (16.1% vs. 21.2% of tweets).

---

## Hypotheses & Results

| # | Hypothesis | Result |
|---|---|---|
| H1 | Embedding + LSTM / 1D CNN outperform the TF-IDF + Logistic Regression baseline on macro-F1 | **Confirmed.** LSTM reached macro-F1 0.7326 (+3.2% relative vs. the baseline's 0.7101) and the CNN reached 0.7212 (+1.6% relative); both beat the baseline on every headline metric. |
| H2 | Accuracy overstates performance on the minority classes given the negative-class imbalance | **Partially confirmed.** Accuracy exceeded macro-F1 by 5 to 6 points for every model, confirming the core claim, but the hardest class was `neutral` (21.2% of tweets), not the smaller `positive` class (16.1%) as hypothesized. Class size alone did not predict difficulty; `neutral` tweets appear intrinsically more ambiguous. |
| H3 | The 1D CNN trains faster than the LSTM at comparable classification performance | **Confirmed.** The CNN trained 2.21x faster per epoch (3.83s vs. 8.46s) and converged in fewer epochs (5 vs. 6), while reaching 98.4% of the LSTM's test macro-F1 (0.7212 vs. 0.7326). |

---

## Business-Decision Threshold & Exposure-Weighted Analysis

Section 8 of the notebook reframes the 3-class output of the best model
(Embedding + LSTM) as a binary "negative vs. not-negative" triage trigger,
the actionable decision for a live customer-service team, and sweeps the
decision threshold instead of using the default 0.5 cutoff an `argmax`
implicitly uses:

| Threshold | Precision | Recall | Selection rule |
|---|---|---|---|
| 0.186 | 0.8279 | 0.9318 | F1-optimal |
| **0.119** | 0.7979 | 0.9501 | recall-priority (at least 95% recall on `negative`) |

Lowering the threshold from the default 0.5 to the recommended 0.119 cuts
**missed negative tweets by 65.8%** (199 to 68 on the test set), at the cost
of routing more tweets to the triage queue (61.11% to 74.69% of all test
tweets). Using `retweet_count` as a visibility/exposure proxy, the maximum
retweet count among missed tweets stayed at 2 under both thresholds, far
below the 32 retweets seen on the most-retweeted negative tweet in the test
set, so even the default threshold was not disproportionately missing the
highest-visibility complaints; `retweet_count` itself is a weak signal in
this dataset (mean 0.092 across all negative test tweets).

---

## Key Findings

- **Deep learning beat the classic baseline, but by a modest margin**:
  Embedding + LSTM's macro-F1 (0.7326) is only 3.2% better (relative) than
  TF-IDF + Logistic Regression's (0.7101), evidence that a well-regularized
  bag-of-words model with bigrams remains a strong baseline for short,
  informal text.
- **`neutral` tweets, not `positive` ones, are the hardest to classify**:
  every model's recall on `neutral` (0.639 to 0.665) was its weakest class,
  even though `positive` is the smaller class, and the dominant confusion for
  every model is `neutral` tweets pulled toward `negative` (104 to 113
  tweets) rather than toward `positive` (50 to 58 tweets).
- **The 1D CNN is the pragmatic production choice for this task**: it trains
  2.21x faster per epoch than the LSTM and lands within 1.5 macro-F1 points
  of it, while narrowly winning on ranking ability (macro ROC-AUC 0.8923 vs.
  0.8868).
- **Calibrating the decision threshold changes the triage outcome more than
  the model choice does**: moving from 0.5 to 0.119 cuts missed negative
  tweets by 65.8%, at the cost of a larger triage queue (61.11% to 74.69%).
- **The LSTM's learned embedding organized itself around real sentiment
  structure** with no explicit word-level supervision: nearest neighbors of
  "rude" were "worst", "unacceptable" and "ridiculous"; neighbors of "thanks"
  were "awesome", "great" and "excellent".
- **The TF-IDF baseline's top negative-class coefficients** ("not", "hours",
  "hold", "worst", "delayed", "cancelled") map directly onto the top negative
  reasons found in the EDA ("Customer Service Issue": 2,885 tweets, "Late
  Flight": 1,650), showing the linear baseline picks up on the same
  operational pain points a human analyst would flag.

---

## Final Model & Threshold Recommendation

- **Model:** Embedding + LSTM (test macro-F1 0.7326, accuracy 0.7911, the
  strongest model on every headline metric except ranking ability)
- **Decision threshold for the negative-vs-not-negative triage trigger:**
  **0.119** (not the default 0.5, and not the F1-optimal 0.186), chosen for
  at least 95% recall on `negative`
- **Trade-off accepted:** missed negative tweets drop from 199 to 68 (a
  65.8% reduction) at the cost of a larger triage queue (61.11% to 74.69% of
  tweets routed for human review)

For a deployment that prioritizes training and inference cost over the last
1.5 macro-F1 points, Embedding + 1D CNN is a credible alternative: it trains
2.21x faster per epoch and reaches 98.4% of the LSTM's macro-F1.

---

## Repository Structure

```text
04_text_classification_keras/
|-- data/                                    # gitignored
|   |-- raw/                                 # generated by Kaggle download in notebook
|   `-- processed/                           # reserved for derived datasets
|-- notebooks/
|   `-- 04_text_classification_keras.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## How to Run

1. Go to project folder:

```bash
cd 04_text_classification_keras
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
notebooks/04_text_classification_keras.ipynb
```

---

## Notes

- Do not commit credentials (`kaggle.json`) or virtual environment folders.
- The raw Twitter US Airline Sentiment CSV is downloaded locally and
  excluded via `.gitignore`; re-run the notebook to regenerate it. NLTK's
  stopword corpus is likewise downloaded on first run.
- 155 rows shared an exact duplicate `tweet_id` and were dropped before
  splitting, to avoid the same tweet appearing in both train and test. A
  further 400 rows share identical `text` under different `tweet_id`s
  (retweet-style duplicates); 25 of the 187 unique texts involved were
  labeled inconsistently by different crowd workers, real label noise that
  sets a known ceiling on achievable accuracy.
- Both neural models train on CPU only: TensorFlow >= 2.11 has no native GPU
  support on Windows outside WSL2 or the DirectML plugin, neither of which
  was set up for this notebook. Training still completes in under a minute
  per model at this dataset size.
- Word embeddings are learned from scratch for both neural models, not
  loaded from a pretrained source (e.g. GloVe); the notebook's Next Steps
  list this as a follow-up A/B test.
- `neutral` was the hardest class for every model tested, not `positive` as
  originally hypothesized (H2); the notebook lists a dedicated follow-up on
  why in its Next Steps.
- All metrics reported are single-split test-set results (no nested CV).
- **CI:** [`.github/workflows/ci-04-text-classification-keras.yml`](../.github/workflows/ci-04-text-classification-keras.yml)
  re-runs this notebook end-to-end on every push/PR touching this folder, to
  catch reproducibility regressions (dataset drift, deprecated library APIs).
  It downloads the dataset via the Kaggle API using `KAGGLE_USERNAME`/
  `KAGGLE_KEY` repository secrets — set those in the GitHub repo settings
  (Settings → Secrets and variables → Actions) for the workflow to run.

---

> Back to portfolio: [data-science-portfolio](../README.md)

---
name: data-science-setup
description: Automates the setup of a data science portfolio project in Python, including folder structure, virtual environment, package installation, and initial notebook creation for insurance cost analysis.
---

You are a specialized AI assistant for setting up data science projects in Python.

The user is working on a Data Science portfolio project in Python. The current directory is the project root: 01_statistical_foundations_insurance_cost_regression/

Your task is to perform the following steps in order:

STEP 1 — Create folder structure

Create the following folders inside the current directory if they don't exist yet:
- notebooks/
- data/
- src/

Use the create_directory tool for each.

STEP 2 — Create .gitignore

Create a .gitignore file in the project root with the following content:

venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
.DS_Store
data/

Use the create_file tool.

STEP 3 — Create virtual environment

Create a virtual environment named venv inside the project root:

Run the command: python -m venv venv

Use the run_in_terminal tool with mode='sync'.

STEP 4 — Activate the virtual environment (Windows PowerShell)

Activate the venv: venv\Scripts\activate

Run the command in the terminal. Since terminals persist, subsequent commands will use the activated venv.

STEP 5 — Install all required libraries

With the venv activated, install:

pip install numpy pandas scipy statsmodels scikit-learn matplotlib seaborn jupyter ipykernel kaggle

Run the command in the terminal.

STEP 6 — Register the venv as a Jupyter kernel for VS Code

python -m ipykernel install --user --name=venv_insurance --display-name "Python (insurance)"

Run the command in the terminal.

STEP 7 — Save dependencies

pip freeze > requirements.txt

Run the command in the terminal.

STEP 8 — Create the Jupyter notebook

Create the file: notebooks/01_insurance_cost_analysis_regression.ipynb

With the following cells in order:

Cell 1 (Markdown):
# Insurance Cost Analysis & Regression — Medical Cost Personal Dataset

This notebook explores the *Medical Cost Personal Dataset* (Kaggle) to understand
which factors drive individual medical insurance charges.

We will:
- perform a thorough **statistical analysis** (descriptive + inferential),
- build and interpret **linear regression models** (simple and multiple),
- evaluate model assumptions (residuals, normality, homoscedasticity),
- and connect each step to statistical theory (CLT, hypothesis testing, OLS).

**Business question**

> Which factors explain individual medical insurance costs, and what is the
> average effect of age, BMI and smoking habits on charges, with quantified uncertainty?

**Dataset**
- Each row: one insured individual
- Target variable (y): `charges` (medical insurance cost)
- Features (X): `age`, `bmi`, `smoker`, `children`, `sex`, `region`
- Source: [Kaggle — Medical Cost Personal Dataset](https://www.kaggle.com/datasets/mirichoi0218/insurance)

> **Note (Português):** Este projeto foi desenvolvido como parte do meu portfólio
> de Data Science, com foco em fundamentos estatísticos e regressão linear aplicados
> a custos de seguro saúde.

Cell 2 (Markdown):
## Notebook Roadmap

1. Context & data loading
2. Data cleaning & exploratory data analysis (EDA)
3. Inferential statistics (confidence intervals & hypothesis tests)
4. Simple linear regression — `charges ~ age`
5. Multiple linear regression — full model
6. Model diagnostics (residuals, normality, homoscedasticity)
7. Conclusions & industry relevance

Cell 3 (Markdown):
## 1. Context & data loading

In this section:
- Load the dataset into a pandas DataFrame via Kaggle API.
- Inspect basic information: shape, dtypes, missing values.
- Connect the dataset to the business problem: pricing health insurance
  based on individual risk factors.

### How to reproduce — Data access

This notebook downloads the dataset automatically via the **Kaggle API**.

To run it locally:

1. Create a free account at [kaggle.com](https://www.kaggle.com).
2. Go to **Settings → API → Create New Token** to download your `kaggle.json`.
3. Place the file at the standard path:
   - Windows: `C:\Users\<YOUR_USER>\.kaggle\kaggle.json`
   - Mac/Linux: `~/.kaggle/kaggle.json`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the notebook — the dataset will be downloaded automatically.

No credentials are stored in this repository.

Cell 4 (Code — imports):

# === Standard Library ===
import warnings
warnings.filterwarnings('ignore')
import os
import subprocess

# === Data Manipulation ===
import numpy as np
import pandas as pd

# === Statistical Tests ===
from scipy import stats
from scipy.stats import ttest_ind, shapiro, norm, t

# === Modelling ===
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan

# === Validation ===
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# === Visualisation ===
import matplotlib.pyplot as plt
import seaborn as sns

# === Display settings ===
pd.set_option('display.float_format', '{:.4f}'.format)
sns.set_theme(style='whitegrid')
%matplotlib inline

Cell 5 (Code — load data via Kaggle API):

# Download dataset via Kaggle API
DATASET = "mirichoi0218/insurance"
DATA_DIR = "../data"

if not os.path.exists(f"{DATA_DIR}/insurance.csv"):
    os.makedirs(DATA_DIR, exist_ok=True)
    subprocess.run(
        [
            "kaggle", "datasets", "download",
            "-d", DATASET,
            "--unzip",
            "-p", DATA_DIR,
        ],
        check=True,
    )

# Load dataset
df = pd.read_csv(f"{DATA_DIR}/insurance.csv")

# First look
print(df.shape)
df.head()

Cell 6 (Markdown):
## 2. Exploratory Data Analysis (EDA)

Goals of this section:
- Understand the distribution of key variables: `charges`, `age`, `bmi`, `children`
- Compare charges across groups: `smoker` vs `non-smoker`, `sex`, `region`
- Inspect pairwise relationships between variables

Concepts applied (from study notes):
- Descriptive statistics: mean, median, variance, standard deviation, quantiles
- Distribution shape: skewness, outliers, heavy tails
- Correlation (Pearson): linear association between two continuous variables

Cell 7 (Markdown):
## 3. Inferential Statistics — smokers vs non-smokers

Business questions:
- Are average medical charges significantly higher for smokers than non-smokers?
- What is the estimated difference in mean charges, with a 95% confidence interval?

Analyses:
1. Two-sided t-test for difference in means:
   - H0: μ_smoker = μ_nonsmoker
   - H1: μ_smoker ≠ μ_nonsmoker
2. 95% confidence intervals for mean charges per group and for the difference

Concepts applied:
- Central Limit Theorem (CLT) and standard error of the mean
- t-test for independent samples (Welch), p-value, Type I/II errors
- Confidence intervals as a range of plausible values for the population mean
- Linear algebra connection: data vectors for smokers/non-smokers as subspaces of Rⁿ

Cell 8 (Markdown):
## 4. Simple Linear Regression — charges ~ age

Objective:
- Fit a simple OLS model using only `age` to predict `charges`
- Show OLS in matrix form: β̂ = (XᵀX)⁻¹ Xᵀy (computed manually with NumPy)
- Illustrate the connection between Pearson correlation and R² in simple regression

Analyses:
1. Fit `charges ~ age` using OLS
2. Compute slope, intercept, R² and compare with r² (Pearson correlation squared)
3. Plot scatter of `age` vs `charges` with fitted regression line

Concepts applied:
- OLS objective: minimize SSE = Σ(yᵢ − ŷᵢ)²
- Matrix form: ŷ = Xβ, β̂ = (XᵀX)⁻¹ Xᵀy
- In simple regression: R² = r² (Pearson squared)

Cell 9 (Markdown):
## 5. Multiple Linear Regression — full model

Objective:
- Fit a multiple OLS model: `charges ~ age + bmi + children + smoker + sex + region`
- Interpret coefficients as ceteris paribus marginal effects on charges

Analyses:
1. Create dummy variables for `smoker`, `sex`, `region` (drop_first=True)
2. Fit the full model with statsmodels and inspect the summary output:
   - R² and adjusted R²
   - F-statistic (global significance)
   - Coefficient estimates, standard errors, t-statistics, p-values
   - 95% confidence intervals for key coefficients
3. Compute VIF (Variance Inflation Factor) for each predictor

Concepts applied:
- Multiple regression matrix form: y = Xβ, β̂ = (XᵀX)⁻¹ Xᵀy
- Marginal effect interpretation (ceteris paribus)
- R² vs adjusted R², F-test for global significance
- Multicollinearity and VIF

Cell 10 (Markdown):
## 6. Model Diagnostics

Objective:
- Check whether the main OLS assumptions are reasonably satisfied:
  - Normality of residuals
  - Homoscedasticity (constant variance)
  - Absence of severe multicollinearity
  - No overfitting (generalisation check)

Analyses:
1. Residuals vs fitted values plot
2. Histogram / KDE of residuals
3. Shapiro–Wilk test for normality of residuals
4. Breusch–Pagan test for homoscedasticity
5. VIF table
6. Train/test split: compare R² on train vs test
7. k-Fold cross-validation (k=10): mean R² ± std

Concepts applied:
- Residuals as unexplained variation in y
- Normality of residuals: required for valid t-tests and CIs on coefficients
- Homoscedasticity: constant variance assumption
- Overfitting vs underfitting: train vs validation R² comparison

Cell 11 (Markdown):
## 7. Conclusions

Summarise:
- Which variables have the strongest and most robust association with charges?
- How large is the estimated effect of smoking and BMI on costs?
- Model quality: R² / adjusted R², assumption checks, limitations

## 8. Relevance to Industry

This workflow — EDA → inferential statistics → regression with diagnostics —
mirrors how pricing and risk teams in health insurance and insurtech companies:

- Estimate the impact of risk factors (age, BMI, smoking) on expected costs
- Set premiums that reflect individual risk while controlling for uncertainty
- Communicate results using interpretable coefficients and confidence intervals
- Ensure model robustness by checking assumptions and out-of-sample performance

It is a core pattern in actuarial analytics, healthcare cost modelling
and risk-based pricing in the insurance industry.

To create the notebook, use the create_new_jupyter_notebook tool with the query: "Create a Jupyter notebook for insurance cost analysis with the following cells: [then the above cell descriptions]"

The query should include all the cell content as described above.

After creating the notebook, ensure it is saved in the correct path: notebooks/01_insurance_cost_analysis_regression.ipynb

Perform all steps in order, and validate that each step completes successfully. If any step fails, report the error and stop.

Once all steps are done, summarize what was accomplished.
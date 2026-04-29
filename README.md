# Data Science & Machine Learning Portfolio

> 🇧🇷 Versão em português: [README_pt-BR.md](README_pt-BR.md)

---

## About me

I am a **Data & Analytics professional** with a **B.Sc. in Production Engineering** and an **MBA in Data Science & Analytics (USP/Esalq)**. I also completed a **specialization in IT Project & Business Management (IFRJ)** and an **executive program in Project Management & Business English (Ohio University)**.

Over the past years I have:
- led **end-to-end analytics projects**, including full ETL:
  - **Extract**: ingesting data from APIs, databases and flat files using Python and SQL;
  - **Transform**: cleaning, joining and enriching datasets with Python, SQL and Power Query;
  - **Load & Visualize**: loading curated data into Power BI and deploying dashboards in cloud environments (AWS/Azure);
- implemented **RPA and data integrations** to reduce manual work across financial and governance areas;
- and developed **academic capstone projects** applying text similarity metrics and LLM evaluation
  (malaria case study, USP/Esalq), and a **web application in R** to analyze offshore wind potential
  using ERA5 climate reanalysis data based on satellite observations (IFRJ).


This portfolio organizes my current learning path in **Data Science, ML and AI engineering**,
connecting:
- theoretical foundations (statistics, probability, linear algebra, calculus),
- practical projects (simulation, EDA, ML pipelines, deep learning, LLMs),
- and previous academic work (capstones),

into a coherent journey towards a future **MSc in Data Science / AI**.

---

## Repository Structure

```text
data-science-portfolio/
├── README.md
├── .gitignore
├── .gitattributes
├── LICENSE
├── 01_statistical_foundations_insurance_cost_regression/
├── 90_tcc_usp_malaria/
└── 91_tcc_ifrj_offshore_wind/
```

Planned next folders (roadmap):
- `02_eda_olist_storytelling/`
- `03_ml_supervised_pipeline/`
- `04_text_classification_keras/`
- `05_llm_rag_pdf_chatbot/`

---

## Current & Planned Projects

> Projects are built progressively alongside a structured reading path.  
> Each project has its own folder with code, notebooks and a detailed README.
> Planned/in-progress projects may be listed before their folder is created.

### 01 · Statistical Foundations — Insurance Cost Regression  
`📁 01_statistical_foundations_insurance_cost_regression/` · *Status: Completed*

Applied a full statistical workflow on the Medical Cost Personal Dataset:
- exploratory analysis and inferential statistics,
- multiple linear regression with diagnostics and robust inference,
- validation with train/test split and cross-validation.

**Stack:** Python · NumPy · pandas · statsmodels · matplotlib · seaborn · scipy

---

### 02 · Business Analytics — EDA & Storytelling with Real Data  
`📁 02_eda_olist_storytelling/` · *Status: In progress*

Exploratory data analysis and **business storytelling** on a real Brazilian dataset
(e.g. Olist), with:
- clearly stated hypotheses,
- EDA and basic statistical tests,
- narrative notebook from a business stakeholder perspective.

**Stack:** Python · pandas · seaborn · matplotlib · scipy

---

### 03 · ML Pipeline — Supervised Learning & Evaluation  
`📁 03_ml_supervised_pipeline/` · *Status: Planned*

End-to-end **supervised ML pipeline** (churn or credit/default), including:
- feature engineering,
- model comparison (logistic regression vs. tree-based models),
- evaluation beyond accuracy (ROC, PR, F1, etc.).

**Stack:** Python · scikit-learn · pandas · matplotlib · seaborn

---

### 04 · Deep Learning — Text Classification with Keras  
`📁 04_text_classification_keras/` · *Status: Planned*

**Text classification** (sentiment/spam) with Keras, bridging classic ML and deep learning:
- simple neural sequence model (Embedding + LSTM/GRU or 1D CNN),
- comparison with a TF‑IDF + logistic regression baseline.

**Stack:** Python · TensorFlow/Keras · scikit-learn · pandas · matplotlib

---

### 05 · LLM & RAG — Domain-Specific PDF Chatbot  
`📁 05_llm_rag_pdf_chatbot/` · *Status: Planned*

A **Retrieval-Augmented Generation (RAG)** system over a focused document corpus
(e.g. health, legislation or technical reports), with:
- ingestion, chunking, embeddings and vector search,
- documented architectural choices and basic evaluation of answer quality.

**Stack:** Python · LangChain / LlamaIndex · vector store · LLM API / open-source LLM

---

## Previous Academic Work (Capstones / Theses)

> Two completed academic capstone projects, with full code, data and reports.

### A · Evaluation of Generative Neural Networks in Public Health — Malaria Case Study  
`📁 90_tcc_usp_malaria/` · *MBA Capstone — USP/Esalq (2025)*

Evaluated the **readability, textual similarity and consistency** of answers from 10 LLM-based
systems about malaria, using WHO fact sheets as ground truth.

- Readability: Flesch Reading Ease, Flesch–Kincaid Grade Level  
- Text similarity: cosine (TF‑IDF), Levenshtein distance, Jaccard similarity  
- Composite ranking via min–max normalization across metrics  
- Unsupervised learning: K‑Means clustering (k via Elbow & Silhouette)  
- Statistical validation: one-way ANOVA, Chi-square  
- Multiple Correspondence Analysis (MCA): 2D + interactive 3D maps (models × topics × clusters)

**Outcome:** identified three statistically distinct clusters of models, showed how question topic
drives model behavior, and proposed a reusable methodology for auditing generative AI in
sensitive health contexts.

**Stack:** Python · pandas · scikit-learn · textstat · python‑Levenshtein · pingouin · prince · plotly · seaborn

---

### B · Offshore Wind Potential Analysis — R Shiny Web Application (Campos Basin)  
`📁 91_tcc_ifrj_offshore_wind/` · *Specialization Capstone — IFRJ (2024)*

Developed an interactive **R Shiny web application** to analyze offshore wind potential on
nine decommissioned oil platforms in Brazil’s Campos Basin, following a **CRISP‑DM** process.

- Data: ERA5 climate reanalysis (NetCDF) + INMET station for validation  
- Processing: wind speed and direction from u/v components, seasonal analysis, time-series  
- Modeling: physics-based turbine power potential per platform (ρ, swept area, η, v³)  
- Visualization: maps with wind speed, direction fields and platform-level potential  
- Validation: comparison with São Tomé meteorological station data

**Outcome:** showed that reusing decommissioned platforms can provide competitive and more
consistent offshore wind generation, supporting Brazil’s energy transition strategy.

**Stack:** Python (`cdsapi`, `xarray`) · R (`shiny`, `ggplot2`, `ncdf4`, `viridis`, `maps`, `dplyr`, `grid`)

---

## Study Roadmap

Projects in this portfolio are tied to a structured reading plan:

- **Foundations** — *Naked Statistics*, *Essential Math for Data Science*, *Data Science for Business*  
  Focus on probability, statistical thinking and how data connects to business decisions.

- **Tools & Practice** — *Python for Data Analysis*  
  Hands-on data wrangling, cleaning and EDA in Python (NumPy, pandas, visualization).

- **Applied ML** — *Hands-On Machine Learning*  
  Supervised/unsupervised learning, model evaluation and practical ML pipelines.

- **ML Systems & MLOps** — *Designing Machine Learning Systems*, *ML Design Patterns*  
  From “one-off models” to robust ML systems: design choices, patterns and trade-offs.

- **Deep Learning** — *Deep Learning with Python*  
  Neural networks for tabular, text and sequence data, connecting to portfolio DL projects.

- **LLMs & AI Engineering** — *Hands-On Large Language Models*, *AI Engineering*  
  Architectures, prompting, RAG and evaluation for large language models in production-style setups.

---

## Contact

- **Email:** vinicius98freire@gmail.com  
- **LinkedIn:** [marcus-vinicius-freire-junior](https://www.linkedin.com/in/marcus-vinicius-freire-junior/?locale=en-US)
- **Location:** Rio de Janeiro, Brazil

# -*- coding: utf-8 -*-
"""
Created on Fri May 23 12:50:42 2025

@author: Marcus Vinicius Freire Junior
"""
# %% Necessary installations:
# pip install pandas
# pip install numpy
# pip install matplotlib
# pip install seaborn
# pip install scikit-learn
# pip install textstat
# pip install python-Levenshtein
# pip install scipy
# pip install statsmodels
# pip install pingouin
# pip install prince
# pip install plotly

# %% Libraries
import pandas as pd
import numpy as np
import os
import textstat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from math import pi
from scipy.stats import zscore
from sklearn.cluster import KMeans
from scipy.stats import chi2_contingency
from sklearn.metrics import silhouette_score
import pingouin as pg
import prince
import plotly.express as px

# %% Repository path configuration
os.makedirs(
    "data", exist_ok=True
)  # ensures existence (does not fail if already exists)
os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)
# %% Data import
# Folder path
caminho_pasta = "data"

# Import with corresponding variable name
df_claude = pd.read_excel(os.path.join(caminho_pasta, "df_claude.xlsx"))
df_copilot = pd.read_excel(os.path.join(caminho_pasta, "df_copilot.xlsx"))
df_deepseek = pd.read_excel(os.path.join(caminho_pasta, "df_deepseek.xlsx"))
df_gemini = pd.read_excel(os.path.join(caminho_pasta, "df_gemini.xlsx"))
df_gpt = pd.read_excel(os.path.join(caminho_pasta, "df_gpt.xlsx"))
df_gpt_escholar = pd.read_excel(os.path.join(caminho_pasta, "df_gpt_escholar.xlsx"))
df_gpt_vision = pd.read_excel(os.path.join(caminho_pasta, "df_gpt_vision.xlsx"))
df_meta_llama = pd.read_excel(os.path.join(caminho_pasta, "df_meta_llama.xlsx"))
df_reka = pd.read_excel(os.path.join(caminho_pasta, "df_reka.xlsx"))
df_perplexity = pd.read_excel(os.path.join(caminho_pasta, "df_perplexity.xlsx"))
df_oms = pd.read_excel(os.path.join(caminho_pasta, "df_oms.xlsx"))

# %% List with all AI DataFrames
# List with all AI DataFrames
dfs_ia = [
    df_claude,
    df_copilot,
    df_deepseek,
    df_gemini,
    df_gpt,
    df_gpt_escholar,
    df_gpt_vision,
    df_meta_llama,
    df_reka,
    df_perplexity,
]

# %% Word Count + Difference with the OMS
# Objective:
# Add a word_count column with the number of words in the AI response
# Add a word_count_diff column with the absolute difference compared to the OMS response (line by line, by index)


def contar_palavras(texto):
    return len(str(texto).split())


# Apply to df_oms once
df_oms["word_count"] = df_oms["response"].apply(contar_palavras)

# Apply to all AI DataFrames
for df in dfs_ia:
    df["word_count"] = df["response"].apply(contar_palavras)
    df["word_count_diff"] = df["word_count"] - df_oms["word_count"]

# %% Flesch Reading Ease
# This metric calculates the ease of reading of a text based on the Flesch Reading Ease formula.
# Although theoretically the scale varies from 0 to 100, in practice values can be negative for extremely complex texts.
# The higher the value, the easier it is to read the text.

# Typical interpretation of the score (approximate):
# 90–100  → Very easy (5th grade)
# 60–70   → Easy (elementary school)
# 30–50   → Medium to difficult (high school)
# 0–30    → Difficult (university level)
# < 0     → Extremely difficult

# Interpretation of the flesch_diff column:
# > 0: AI response is easier to read than OMS
# < 0: AI response is more difficult
# = 0: same ease

# Apply to df_oms
df_oms["flesch_reading_ease"] = df_oms["response"].apply(textstat.flesch_reading_ease)

# Apply to each AI DataFrame and calculate the difference
for df in dfs_ia:
    df["flesch_reading_ease"] = df["response"].apply(textstat.flesch_reading_ease)
    df["flesch_diff"] = df["flesch_reading_ease"] - df_oms["flesch_reading_ease"]

# %% Flesch-Kincaid Grade Level
# This metric calculates the Flesch-Kincaid Grade Level, which estimates the number of years of formal education
# required to understand the text. Although the scale normally varies between 0 and 12,
# in texts more complex (such as long and technical responses), the value can exceed 20, 30 or more.

# Typical interpretation (theoretical reference):
#  5.0  →  5th grade (easy)
#  8.0  →  8th grade (intermediate)
# 12.0  →  High school
# >13.0 →  University level or technical language

# The analysis allows comparing the textual complexity of AIs with OMS.

# Interpretation of the fk_grade_diff column:
# > 0: AI response requires more education than OMS (more difficult)
# < 0: AI response requires less education than OMS (simpler)
# = 0: same education level

# Apply to df_oms
df_oms["fk_grade_level"] = df_oms["response"].apply(textstat.flesch_kincaid_grade)

# Apply to AI DataFrames
for df in dfs_ia:
    df["fk_grade_level"] = df["response"].apply(textstat.flesch_kincaid_grade)
    df["fk_grade_diff"] = df["fk_grade_level"] - df_oms["fk_grade_level"]

# %%  Cosine Similarity
# This metric calculates the semantic similarity between two responses (AI vs OMS) based on the angle between their TF-IDF vectors.
# The closer to 1, the more similar the texts are in content.
# Range of the cosine_similarity column:
# 1.0 → texts semantically identical
# 0.5 → some thematic alignment
# 0.0 → no semantic relation

# Prepare the OMS reference vector
oms_respostas = df_oms["response"].fillna("")

# Instantiate the TF-IDF vector
vectorizer = TfidfVectorizer()

# Apply to each AI
for df in dfs_ia:
    ia_respostas = df["response"].fillna("")

    # Concatenate line by line (each OMS–AI pair)
    similaridades = []
    for ia, oms in zip(ia_respostas, oms_respostas):
        tfidf = vectorizer.fit_transform([ia, oms])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        similaridades.append(sim)

    # Add to DataFrame
    df["cosine_similarity"] = similaridades

# %% Levenshtein Distance
# This metric calculates the Levenshtein distance between the AI and OMS texts,
# that is, the minimum number of editing operations (addition, removal or character substitution) necessary to transform one text into the other.
# Interpretation:
# 0 → identical texts
# Small value → similar texts in structure
# Large value → very different texts

# Apply to each AI DataFrame
for df in dfs_ia:
    distancias = []
    for ia_resp, oms_resp in zip(df["response"], df_oms["response"]):
        distancia = Levenshtein.distance(str(ia_resp), str(oms_resp))
        distancias.append(distancia)

    df["levenshtein_dist"] = distancias

# %% Jaccard Coefficient
# This metric calculates the Jaccard coefficient between the AI and OMS responses.
# It evaluates similarity based on the intersection and union of the sets of unique words.
#
# Interpretation of the jaccard_similarity column:
# 1.0 → texts with identical vocabulary
# 0.0 → no common vocabulary
# 0.5 Intermediate → partially overlapping


def jaccard_similarity(str1, str2):
    set1 = set(str(str1).lower().split())
    set2 = set(str(str2).lower().split())
    if not set1 and not set2:
        return 1.0
    elif not set1 or not set2:
        return 0.0
    return len(set1.intersection(set2)) / len(set1.union(set2))


# Apply to each AI DataFrame
for df in dfs_ia:
    jaccard_scores = []
    for ia_resp, oms_resp in zip(df["response"], df_oms["response"]):
        score = jaccard_similarity(ia_resp, oms_resp)
        jaccard_scores.append(score)
    df["jaccard_similarity"] = jaccard_scores

# %% Concatenate AI DataFrames
# Concatenate all AI DataFrames directly
df_all_responses = pd.concat(dfs_ia, ignore_index=True)

# %%########### GRAPHICAL ANALYSIS ###################

# %% Bar chart of average difference in number of words

plt.figure(figsize=(11, 6))

# Calculate the average per AI
ranking_wc_raw = df_all_responses.groupby("AI")["word_count_diff"].mean()

# Order by absolute distance from zero
ranking_wc = ranking_wc_raw.reindex((ranking_wc_raw - 0).abs().sort_values().index)

# Create the chart
ax = sns.barplot(x=ranking_wc.values, y=ranking_wc.index, palette="viridis")

# Add labels at the end of the bars
for i, v in enumerate(ranking_wc.values):
    alinhamento = "left" if v >= 0 else "right"
    offset = 0.01 if v >= 0 else -0.01
    ax.text(v + offset, i, f"{v:.1f}", va="center", ha=alinhamento, fontweight="bold")

# Reference line
plt.axvline(0, color="purple", linestyle="--")

# Titles and axes
plt.title("Average difference in words between AI and OMS")
plt.xlabel("Words more (positive) or less (negative)")
plt.ylabel("AI")
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/01_average_word_count_difference.png", dpi=300, bbox_inches="tight")


# %% Combined chart – Flesch Reading Ease (Barplot + Boxplot) ordered by proximity to OMS

# Calculate the average Flesch Reading Ease of OMS
media_flesch = df_oms["flesch_reading_ease"].mean()

# Calculate the average per AI
medias_flesch = df_all_responses.groupby("AI")["flesch_reading_ease"].mean()

# Calculate the absolute difference relative to OMS average
proximidade = (medias_flesch - media_flesch).abs().sort_values()

# Get the order of AIs based on this proximity
ordem_ias = proximidade.index.tolist()

# Create the figure with two subplots
fig, axes = plt.subplots(
    2, 1, figsize=(12, 10), sharex=True, gridspec_kw={"height_ratios": [1, 1]}
)

# Barplot (averages)
ranking_flesch = medias_flesch.reindex(ordem_ias)
sns.barplot(
    x=ranking_flesch.values, y=ranking_flesch.index, palette="viridis", ax=axes[0]
)
axes[0].axvline(
    media_flesch,
    color="red",
    linestyle="--",
    label=f"OMS (average: {media_flesch:.2f})",
)
axes[0].set_title("Flesch Reading Ease – Averages by AI (ordered by proximity to OMS)")
axes[0].set_xlabel("")
axes[0].set_ylabel("AI")
axes[0].legend()
for i, v in enumerate(ranking_flesch.values):
    axes[0].text(v + 0.5, i, f"{v:.1f}", va="center", fontweight="bold")

# Boxplot (distribution by AI)
df_ord = df_all_responses.copy()
df_ord["AI"] = pd.Categorical(df_ord["AI"], categories=ordem_ias, ordered=True)
sns.boxplot(data=df_ord, x="flesch_reading_ease", y="AI", palette="Set3", ax=axes[1])
axes[1].axvline(
    media_flesch,
    color="red",
    linestyle="--",
    label=f"OMS (average: {media_flesch:.2f})",
)
axes[1].set_title("Flesch Reading Ease – Distribution by AI vs OMS Average")
axes[1].set_xlabel("Flesch Reading Ease")
axes[1].set_ylabel("AI")
axes[1].legend()
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/02_flesch_reading_ease_sorted.png", dpi=300, bbox_inches="tight")

# %% Combined chart – Flesch-Kincaid Grade Level (Barplot + Boxplot) ordered by proximity to OMS

# Calculate the average of OMS
media_fk = df_oms["fk_grade_level"].mean()

# Calculate the averages per AI
medias_fk = df_all_responses.groupby("AI")["fk_grade_level"].mean()

# Absolute difference relative to OMS average
proximidade_fk = (medias_fk - media_fk).abs().sort_values()

# Order of AIs by proximity
ordem_ias_fk = proximidade_fk.index.tolist()

# Create the figure
fig, axes = plt.subplots(
    2, 1, figsize=(12, 10), sharex=True, gridspec_kw={"height_ratios": [1, 1]}
)

# Barplot
ranking_fk = medias_fk.reindex(ordem_ias_fk)
sns.barplot(x=ranking_fk.values, y=ranking_fk.index, palette="viridis", ax=axes[0])
axes[0].axvline(
    media_fk, color="red", linestyle="--", label=f"OMS (average: {media_fk:.2f})"
)
axes[0].set_title(
    "Flesch-Kincaid Grade Level – Averages by AI (ordered by proximity to OMS)"
)
axes[0].set_xlabel("")
axes[0].set_ylabel("AI")
axes[0].legend()
for i, v in enumerate(ranking_fk.values):
    axes[0].text(v + 0.3, i, f"{v:.1f}", va="center", fontweight="bold")

# Boxplot
df_ord_fk = df_all_responses.copy()
df_ord_fk["AI"] = pd.Categorical(df_ord_fk["AI"], categories=ordem_ias_fk, ordered=True)
sns.boxplot(data=df_ord_fk, x="fk_grade_level", y="AI", palette="Set2", ax=axes[1])
axes[1].axvline(
    media_fk, color="red", linestyle="--", label=f"OMS (average: {media_fk:.2f})"
)
axes[1].set_title("Flesch-Kincaid Grade Level – Distribution by AI vs OMS Average")
axes[1].set_xlabel("Estimated School Level (Flesch-Kincaid)")
axes[1].set_ylabel("AI")
axes[1].legend()
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/03_flesch_kincaid_grade_sorted.png", dpi=300, bbox_inches="tight")

# %% Bar chart of cosine similarity by AI
# Ranking: average cosine similarity per AI
ranking_cosine = (
    df_all_responses.groupby("AI")["cosine_similarity"]
    .mean()
    .sort_values(ascending=False)
)
ranking_cosine

# Bar chart with labels
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=ranking_cosine.values, y=ranking_cosine.index, palette="viridis")

# Add label to each bar
for i, v in enumerate(ranking_cosine.values):
    ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontweight="bold")

plt.title("Ranking of AIs by Cosine Similarity with OMS")
plt.xlabel("Average Cosine Similarity")
plt.ylabel("AI")
plt.xlim(0, 1.05)
plt.grid(axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/04_cosine_similarity_ranking.png", dpi=300, bbox_inches="tight")


# %% Bar chart of Levenshtein Distance

plt.figure(figsize=(10, 6))
ranking_lev = df_all_responses.groupby("AI")["levenshtein_dist"].mean().sort_values()
ax = sns.barplot(x=ranking_lev.values, y=ranking_lev.index, palette="viridis")
for i, v in enumerate(ranking_lev.values):
    ax.text(v + 2, i, f"{v:.0f}", va="center", fontweight="bold")
plt.title("Average Levenshtein Distance (AI vs. OMS)")
plt.xlabel("Average number of edits (characters)")
plt.ylabel("AI")
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/05_levenshtein_distance.png", dpi=300, bbox_inches="tight")


# %% Bar chart of Jaccard Similarity

plt.figure(figsize=(10, 6))
ranking_jaccard = (
    df_all_responses.groupby("AI")["jaccard_similarity"]
    .mean()
    .sort_values(ascending=False)
)
ax = sns.barplot(x=ranking_jaccard.values, y=ranking_jaccard.index, palette="viridis")
for i, v in enumerate(ranking_jaccard.values):
    ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontweight="bold")
plt.title("Vocabulary Similarity (Jaccard) between AI and OMS")
plt.xlabel("Average Jaccard Coefficient")
plt.ylabel("AI")
plt.xlim(0, 1.05)
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/06_jaccard_coefficient.png", dpi=300, bbox_inches="tight")

# %% Pearson Correlation Graph of Variables

correlation_matrix = df_all_responses[
    [
        "word_count_diff",
        "fk_grade_level",
        "flesch_reading_ease",
        "cosine_similarity",
        "levenshtein_dist",
        "jaccard_similarity",
    ]
].corr(method="pearson")

plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    square=True,
)
plt.title("Pearson Correlation between Metrics")
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/07_pearson_correlation_matrix.png", dpi=300, bbox_inches="tight")

# %% RANKING OF AIs
# Methodology Stages
# Group by AI and calculate the averages:

# cosine_similarity → the higher, the better.

# flesch_reading_ease → the higher, the more readable.

# fk_grade_level → the lower, the more accessible.

# word_count_diff → ideal is close to 0 (smaller absolute value).

# levenshtein_dist → the lower, the closer to the original.

# jaccard_similarity → the higher, the more common words.

# Normalize the metrics (scale 0 to 1):

# Positive metrics: cosine_similarity, flesch_reading_ease, jaccard_similarity

# Negative metrics (invert): fk_grade_level, word_count_diff (abs), levenshtein_dist

# Calculate final score as weighted average (or simple) of normalized metrics.

# Sort by final score.

# 1. Grouping by AI
agg = (
    df_all_responses.groupby("AI")
    .agg(
        {
            "word_count_diff": lambda x: x.abs().mean(),
            "fk_grade_level": "mean",
            "flesch_reading_ease": "mean",
            "cosine_similarity": "mean",
            "levenshtein_dist": "mean",
            "jaccard_similarity": "mean",
        }
    )
    .reset_index()
)

# 2. Normalization
scaler = MinMaxScaler()

# Invert metrics where lower is better
agg["fk_grade_level_inv"] = -agg["fk_grade_level"]
agg["word_count_diff_inv"] = -agg["word_count_diff"]
agg["levenshtein_dist_inv"] = -agg["levenshtein_dist"]

# Only the columns for ranking
rank_columns = [
    "word_count_diff_inv",
    "fk_grade_level_inv",
    "flesch_reading_ease",
    "cosine_similarity",
    "jaccard_similarity",
    "levenshtein_dist_inv",
]

agg_ranked = agg.copy()
agg_ranked[rank_columns] = scaler.fit_transform(agg[rank_columns])

# 3. Final score
agg_ranked["score_final"] = agg_ranked[rank_columns].mean(axis=1)
agg_ranked = agg_ranked.drop(
    ["fk_grade_level", "word_count_diff", "levenshtein_dist"], axis=1
)
# Column order:

# Final score in agg
agg["score_final"] = agg_ranked[rank_columns].mean(axis=1)

# Ranking in agg
agg["ranking"] = agg["score_final"].rank(ascending=False).astype(int)

# 4. Ranking
agg_ranked = agg_ranked.sort_values(by="score_final", ascending=False).reset_index(
    drop=True
)
agg_ranked["ranking"] = agg_ranked.index + 1

# Column order:
agg_ranked = agg_ranked[
    [
        "AI",
        "word_count_diff_inv",
        "fk_grade_level_inv",
        "flesch_reading_ease",
        "cosine_similarity",
        "jaccard_similarity",
        "levenshtein_dist_inv",
        "score_final",
        "ranking",
    ]
]


# %% Bar Chart of Normalized Score of AIs
# Visualize result
plt.figure(figsize=(10, 6))
ax = sns.barplot(data=agg_ranked, x="score_final", y="AI", palette="viridis")
# Add value labels to the right of the bars
for i, v in enumerate(agg_ranked["score_final"]):
    ax.text(v + 0.005, i, f"{v:.2f}", va="center", fontweight="bold")
plt.title("Final Ranking of AIs by Composite Performance")
plt.xlabel("Normalized Score (0–1)")
plt.ylabel("AI")
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/08_ai_final_ranking.png", dpi=300, bbox_inches="tight")


# %% Radar Chart of Top 5 AIs
# Select only the top 5 AIs
top5 = agg_ranked.head(5).copy()

# Prepare data for radar chart
metrics = [
    "word_count_diff_inv",
    "fk_grade_level_inv",
    "flesch_reading_ease",
    "cosine_similarity",
    "jaccard_similarity",
    "levenshtein_dist_inv",
]


# Manually normalize metrics to ensure values from 0 to 1
def min_max_normalization(column):
    return (column - column.min()) / (column.max() - column.min())


radar_data = top5[["AI"] + metrics].copy()
for metric in metrics:
    radar_data[metric] = min_max_normalization(radar_data[metric])

# Reorganize for radar format
labels = metrics
num_vars = len(labels)

angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]  # Close the chart

# Plot
plt.figure(figsize=(8, 8))
for i, row in radar_data.iterrows():
    values = row[metrics].tolist()
    values += values[:1]
    plt.polar(angles, values, label=row["AI"], linewidth=2)
    plt.fill(angles, values, alpha=0.1)

plt.xticks(angles[:-1], labels, fontsize=10)
plt.yticks([0.25, 0.5, 0.75, 1.0], ["0.25", "0.5", "0.75", "1.0"], color="gray", size=8)
plt.ylim(0, 1)
plt.title("Performance by Metric – Top 5 AIs", size=14)
plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1))
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/09_top5_ai_radar_chart.png", dpi=300, bbox_inches="tight")

# %%################ ANALYSIS OF AI BY QUESTION TOPIC ####################


# %% Ranking of AI by topic
# Group by AI and topic and calculate metrics
agg_topic = (
    df_all_responses.groupby(["AI", "topic"])
    .agg(
        {
            "word_count_diff": lambda x: x.abs().mean(),
            "fk_grade_level": "mean",
            "flesch_reading_ease": "mean",
            "cosine_similarity": "mean",
            "levenshtein_dist": "mean",
            "jaccard_similarity": "mean",
        }
    )
    .reset_index()
)

# Invert metrics where lower is better
agg_topic["fk_grade_level_inv"] = -agg_topic["fk_grade_level"]
agg_topic["word_count_diff_inv"] = -agg_topic["word_count_diff"]
agg_topic["levenshtein_dist_inv"] = -agg_topic["levenshtein_dist"]

# Only the columns for ranking
rank_columns = [
    "word_count_diff_inv",
    "fk_grade_level_inv",
    "flesch_reading_ease",
    "cosine_similarity",
    "jaccard_similarity",
    "levenshtein_dist_inv",
]

# Min-max normalization by topic

agg_topic_ranked = agg_topic.copy()
for topic in agg_topic["topic"].unique():
    scaler = MinMaxScaler()
    mask = agg_topic["topic"] == topic
    agg_topic_ranked.loc[mask, rank_columns] = scaler.fit_transform(
        agg_topic.loc[mask, rank_columns]
    )

# Final score by topic
agg_topic_ranked["score_topic"] = agg_topic_ranked[rank_columns].mean(axis=1)

# Ranking by topic
agg_topic_ranked["ranking_topic"] = (
    agg_topic_ranked.groupby("topic")["score_topic"].rank(ascending=False).astype(int)
)
agg_topic_ranked = agg_topic_ranked.drop(
    ["fk_grade_level", "word_count_diff", "levenshtein_dist"], axis=1
)


# Include score and rank directly in the original agg_topic
agg_topic["score_topic"] = agg_topic_ranked["score_topic"]
agg_topic["ranking_topic"] = agg_topic_ranked["ranking_topic"]

# %% Chart for Visualizing Final Ranking by Topic
# Create 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

# List of unique topics
topics = agg_topic_ranked["topic"].unique()

# Generate chart by topic
for i, topic in enumerate(topics):
    df_topic = agg_topic_ranked[agg_topic_ranked["topic"] == topic].sort_values(
        "score_topic", ascending=False
    )

    ax = axes[i]
    sns.barplot(data=df_topic, x="score_topic", y="AI", ax=ax, palette="viridis")

    for j, score in enumerate(df_topic["score_topic"]):
        ax.text(score + 0.01, j, f"{score:.2f}", va="center", fontweight="bold")

    ax.set_title(f"Topic: {topic}", fontsize=14)
    ax.set_xlabel("Normalized Score")
    ax.set_ylabel("AI")
    ax.set_xlim(0, 1.05)

# General title
plt.suptitle("Ranking of AIs by Topic (4 Quadrants)", fontsize=18)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/10_ai_ranking_by_topic.png", dpi=300, bbox_inches="tight")


# %%######################### CLUSTER and ANACOR ##########################

# Cluster in df_agg_topic to obtain groups of responses according to the metrics obtained

# %% DataFrame Preparation
# Separating only the quantitative variables from the database df_agg_topic
df_agg_topic_quanti = agg_topic.drop(
    ["AI", "topic", "score_topic", "ranking_topic"], axis=1
)

# Descriptive statistics of variables
df_agg_topic_quanti.describe()

# %% Performing standardization using Z-Score
# The variables are in different units of measurement and need to be standardized
df_agg_topic_pad = df_agg_topic_quanti.apply(zscore, ddof=1)

# %% Identification of number of clusters (Elbow Method)

elbow = []
K = range(1, 11)  # stopping point can be manually parameterized
for k in K:
    kmeanElbow = KMeans(n_clusters=k, init="random", random_state=42).fit(
        df_agg_topic_pad
    )
    elbow.append(kmeanElbow.inertia_)

plt.figure(figsize=(16, 8))
plt.plot(K, elbow, marker="o")
plt.xlabel("Number of Clusters", fontsize=16)
plt.xticks(range(1, 11))  # adjust range
plt.ylabel("WCSS", fontsize=16)
plt.title("Elbow Method", fontsize=16)
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/11_elbow_method.png", dpi=300, bbox_inches="tight")

# %% Identification of number of clusters (Silhouette Method) seeking the maximum point

silhueta = []
I = range(2, 11)  # stopping point can be manually parameterized
for i in I:
    kmeansSil = KMeans(n_clusters=i, init="random", random_state=100).fit(
        df_agg_topic_pad
    )
    silhueta.append(silhouette_score(df_agg_topic_pad, kmeansSil.labels_))

plt.figure(figsize=(16, 8))
plt.plot(range(2, 11), silhueta, color="purple", marker="o")
plt.xlabel("Number of Clusters", fontsize=16)
plt.ylabel("Average Silhouette", fontsize=16)
plt.title("Silhouette Method", fontsize=16)
plt.axvline(x=silhueta.index(max(silhueta)) + 2, linestyle="dotted", color="red")
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/12_silhouette_method.png", dpi=300, bbox_inches="tight")

# %% K-means Cluster

# Consider 3 clusters, given the previous evidence
kmeans_final = KMeans(n_clusters=3, init="random", random_state=100).fit(
    df_agg_topic_pad
)

# Generating the variable to identify the generated clusters
kmeans_clusters = kmeans_final.labels_
agg_topic["Cluster"] = kmeans_clusters
df_agg_topic_pad["Cluster"] = kmeans_clusters
agg_topic_ranked["Cluster"] = kmeans_clusters

# Transform the cluster variable to category to be used in Anacor
agg_topic["Cluster"] = agg_topic["Cluster"].astype("category")
agg_topic_ranked["Cluster"] = agg_topic_ranked["Cluster"].astype("category")
df_agg_topic_pad["Cluster"] = df_agg_topic_pad["Cluster"].astype("category")

# Column order:
agg_topic_ranked = agg_topic_ranked[
    [
        "AI",
        "topic",
        "word_count_diff_inv",
        "fk_grade_level_inv",
        "flesch_reading_ease",
        "cosine_similarity",
        "jaccard_similarity",
        "levenshtein_dist_inv",
        "score_topic",
        "ranking_topic",
        "Cluster",
    ]
]

# %% ANOVA Test for cluster variables

# Objective:
# Verify whether the generated clusters are statistically different regarding each of the evaluated metrics.
# ANOVA (Analysis of Variance) tests whether the mean of a continuous variable differs between two or more groups (in this case, clusters).

# Interpretation:
# - p-value < 0.05 → there is statistical evidence that at least one cluster is different from the others.
# - High F → greater separation between clusters for that metric.
# - Partial Eta² (np2) → effect size (above 0.14 is already considered strong).

# List of metrics to be tested
metricas = [
    "word_count_diff",
    "fk_grade_level",
    "flesch_reading_ease",
    "cosine_similarity",
    "jaccard_similarity",
    "levenshtein_dist",
]

# List to store results
anova_results = []

# Loop to apply ANOVA to each metric
for metrica in metricas:
    resultado = pg.anova(
        dv=metrica,  # dependent variable (metric)
        between="Cluster",  # independent variable (groups = cluster)
        data=agg_topic,  # DataFrame with data
        detailed=True,  # include F, p, partial eta² etc.
    )

    # Print individual result
    print(f"\nANOVA for: {metrica}\n")
    print(resultado)

    # Storage
    row = {
        "Metric": metrica,
        "F": resultado.loc[0, "F"],
        "p-value": resultado.loc[0, "p-unc"],
        "Partial Eta²": resultado.loc[0, "np2"],
    }
    anova_results.append(row)

# Create DataFrame with results
df_anova = pd.DataFrame(anova_results)
print("\nSummary of ANOVA Results:")
print(df_anova)

# %% Boxplots of metrics by cluster
plt.figure(figsize=(16, 12))
for i, metrica in enumerate(metricas):
    plt.subplot(3, 2, i + 1)
    sns.boxplot(data=agg_topic, x="Cluster", y=metrica, palette="Set2")
    plt.title(f"{metrica} by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel(metrica)

plt.suptitle("Distribution of Metrics by Cluster", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/13_metrics_distribution_by_cluster.png", dpi=300, bbox_inches="tight")

# %% Boxplots of score_topic by Cluster
# Objective: see if there are systematic differences in average performance between clusters.
# Interpretation: if the boxplots have different levels of score, the clusters have different performance.
plt.figure(figsize=(8, 6))
sns.boxplot(data=agg_topic, x="Cluster", y="score_topic", palette="Set2")
plt.title("Distribution of Score by Cluster")
plt.xlabel("Cluster")
plt.ylabel("Average Score per Topic")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/14_score_distribution_by_cluster.png", dpi=300, bbox_inches="tight")


# Average score per cluster
media_score_cluster = agg_topic.groupby("Cluster")["score_topic"].mean().reset_index()
media_score_cluster.columns = ["Cluster", "score_medio"]
media_score_cluster["ranking_cluster"] = (
    media_score_cluster["score_medio"].rank(ascending=False).astype(int)
)
print(media_score_cluster)

# Correlation between average score and cluster ranking
correlacao = media_score_cluster["score_medio"].corr(
    media_score_cluster["ranking_cluster"], method="spearman"
)
print(f"Spearman Correlation Coefficient: {correlacao:.2f}")

# High correlation (|ρ| ≥ 0.7): your clusters well reflect AI performance by topic.
# Well-separated boxplots: reinforce that clusters are internally cohesive and externally distinct.

# %% Average characteristics of clusters in the evaluated metrics

# Objective:
# Compare the clusters formed based on the average of the main metrics evaluated (similarity, readability, etc.)
# This helps understand the typical "profile" of each cluster.

# Calculate averages by cluster
cluster_summary = (
    agg_topic.groupby("Cluster")[
        [
            "word_count_diff",
            "fk_grade_level",
            "flesch_reading_ease",
            "cosine_similarity",
            "jaccard_similarity",
            "levenshtein_dist",
        ]
    ]
    .mean()
    .round(2)
)

# %% MULTIPLE ANACOR

# %% Start

# Perform a MULTIPLE ANACOR (ACM) on the qualitative variables (include clusters!)

# Separating only the significant categorical variables for ANACOR in the database
# The question and response variables do not make sense in Correspondence Analysis) because:
# They are free text variables (not simple categorical)
df_agg_topic_quali = agg_topic[["AI", "topic", "Cluster"]]

# %% Chi-Square Test between qualitative variables (using df_all_responses_quali)
# Objective:
# Check if there is a statistically significant association between the variable 'topic'
# and other qualitative variables such as AI and Cluster.


# List of categorical variables to be tested against 'topic'
variaveis_quali = [
    "AI",
    "Cluster",
]  # Adjust as per available columns in df_all_responses_quali

# Loop for association tests
print("Association test with the variable 'topic':\n")
for var in variaveis_quali:
    tabela = pd.crosstab(df_agg_topic_quali["topic"], df_agg_topic_quali[var])
    chi2, p, dof, expected = chi2_contingency(tabela)
    print(f"- {var}: p-value = {round(p, 4)}")

# Interpretation:
# p < 0.05 → There is a statistical association between 'topic' and the categorical variable analyzed.
# p >= 0.05 → There is no evidence of association.

# the result indicates: "Certain patterns of writing, readability, similarity, vocabulary or textual structure are more associated with specific topics."

# %% Developing correspondence analysis with two dimensions!

# Creating coordinates for 3 dimensions (afterward, verify feasibility)
mca = prince.MCA(n_components=2).fit(df_agg_topic_quali)

# Execute the MCA
mca = prince.MCA(n_components=2, random_state=42)
mca = mca.fit(df_agg_topic_quali)

# Analyzing the results

# Eigenvalues analysis
tabela_autovalores = mca.eigenvalues_summary
print(tabela_autovalores)

# Total inertia of the analysis
print(mca.total_inertia_)

# Plot only dimensions with partial inertia exceeding average total inertia
quant_dim = mca.J_ - mca.K_
print(mca.total_inertia_ / quant_dim)


# Inertia explained by dimension
eigenvalues = mca.eigenvalues_

# Coordinates of categories
coord_col = mca.column_coordinates(df_agg_topic_quali).reset_index()
coord_col.columns = ["Category", "Dim1", "Dim2"]


# Plot the chart (categories only)
# Classify type of category: AI, topic, Cluster
def classificar_categoria(cat):
    if cat.startswith("AI_"):
        return "AI"
    elif cat.startswith("topic_"):
        return "Topic"
    elif cat.startswith("Cluster_"):
        return "Cluster"
    else:
        return "Other"


# Apply classification
coord_col["tipo"] = coord_col["Category"].apply(classificar_categoria)

# Define colors by type
cores = {"AI": "blue", "Topic": "orange", "Cluster": "purple"}

# Customized plot
plt.figure(figsize=(10, 8))
for tipo, cor in cores.items():
    dados = coord_col[coord_col["tipo"] == tipo]
    plt.scatter(dados["Dim1"], dados["Dim2"], label=tipo, color=cor, s=70)
    for _, row in dados.iterrows():
        plt.text(row["Dim1"] + 0.03, row["Dim2"] - 0.02, row["Category"], fontsize=9)

# Lines and legends
plt.axhline(0, color="gray", linestyle="--", linewidth=1)
plt.axvline(0, color="gray", linestyle="--", linewidth=1)
plt.title("Perceptual Map – MCA (AI, Topic and Cluster)", fontsize=14, weight="bold")
plt.xlabel(f"Dim 1: {round(eigenvalues[0] * 100, 2)}% of inertia", fontsize=10)
plt.ylabel(f"Dim 2: {round(eigenvalues[1] * 100, 2)}% of inertia", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(title="Category Type")
plt.tight_layout()
plt.show()

# Export Chart (Optional)
# plt.savefig("figures/15_mca_perceptual_map_2d.png", dpi=300, bbox_inches="tight")

# %% Developing correspondence analysis with 3 dimensions!

# Creating coordinates for 3 dimensions (afterward, verify feasibility)
mca = prince.MCA(n_components=3).fit(df_agg_topic_quali)

# Analyzing the results

# Eigenvalues analysis
tabela_autovalores = mca.eigenvalues_summary
print(tabela_autovalores)

# Total inertia of the analysis
print(mca.total_inertia_)

# Plot only dimensions with partial inertia exceeding average total inertia
quant_dim = mca.J_ - mca.K_
print(mca.total_inertia_ / quant_dim)

# Obtaining the standard coordinates of the variable categories
coord_padrao = mca.column_coordinates(df_agg_topic_quali) / np.sqrt(mca.eigenvalues_)
print(coord_padrao)

# Plotting the perceptual map (standard coordinates)
# First step: generate a detailed DataFrame
chart = coord_padrao.reset_index()
var_chart = pd.Series(chart["index"].str.split("_", expand=True).iloc[:, 0])

nome_categ = []
for col in df_agg_topic_quali:
    nome_categ.append(df_agg_topic_quali[col].sort_values(ascending=True).unique())
    categorias = pd.DataFrame(nome_categ).stack().reset_index()

chart_df_mca = pd.DataFrame(
    {
        "categoria": chart["index"],
        "obs_x": chart[0],
        "obs_y": chart[1],
        "obs_z": chart[2],
        "variavel": var_chart,
        "categoria_id": categorias[0],
    }
)

# Second step: generate the point chart
fig = px.scatter_3d(
    chart_df_mca,
    x="obs_x",
    y="obs_y",
    z="obs_z",
    color="variavel",
    text=chart_df_mca.categoria_id,
)

fig.write_html("figures/16_mca_perceptual_map_3d.html")
fig.show()

# %% Exporting main files (Optional)

# df_all_responses.to_excel("results/df_all_responses.xlsx", index=False)
# df_oms.to_excel("results/df_oms_metrics.xlsx", index=False)
# agg_ranked.to_excel("results/df_agg_ranked.xlsx", index=False)
# agg_topic_ranked.to_excel("results/df_agg_topic_cluster.xlsx", index=False)

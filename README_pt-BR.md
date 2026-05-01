# Portfólio de Data Science & Machine Learning

> 🇺🇸 English version: [README.md](README.md)

---

## Sobre mim

Sou um profissional de **Ciência de Dados e Analytics** com **graduação em Engenharia de Produção** e **MBA em Data Science & Analytics (USP/Esalq)**. Também concluí uma **especialização em Gestão de Projetos e Negócios em TI (IFRJ)** e um **programa executivo em Project Management & Business English (Ohio University)**.

Nos últimos anos, eu:
- liderei **projetos de Analytics ponta a ponta**, incluindo ETL completo:
  - **Extração**: ingestão de dados a partir de APIs, bases de dados e arquivos utilizando Python e SQL;
  - **Transformação**: limpeza, junção e enriquecimento de dados com Python, SQL e Power Query;
  - **Carga & Visualização**: carga de dados curados em Power BI e publicação de dashboards em ambientes de nuvem (AWS/Azure);
- implementei **RPA e integrações de dados** para reduzir trabalho manual em áreas financeiras e de governança;
- e desenvolvi **projetos de TCC/capstone** com métricas de similaridade textual e avaliação de LLMs
  (estudo de caso em malária, USP/Esalq), além de uma **aplicação web em R** para analisar potencial eólico offshore
  usando dados de reanálise climática ERA5 baseados em observações de satélites (IFRJ).

Este portfólio organiza minha trilha atual em **Data Science, ML e AI engineering**,
conectando:
- fundamentos teóricos (estatística, probabilidade, álgebra linear, cálculo),
- projetos práticos (simulação, EDA, pipelines de ML, deep learning, LLMs),
- e trabalhos acadêmicos anteriores,

em uma trilha técnica coerente, alinhada a futuros estudos de pós-graduação em **Data Science / IA**.

---

## Estrutura do Repositório

```text
data-science-portfolio/
├── README.md
├── README_pt-BR.md
├── .gitignore
├── .gitattributes
├── LICENSE
├── 01_statistical_foundations_insurance_cost_regression/
├── 90_tcc_usp_malaria/
└── 91_tcc_ifrj_offshore_wind/
```

Próximas pastas planejadas (roadmap):
- `02_eda_olist_storytelling/`
- `03_ml_supervised_pipeline/`
- `04_text_classification_keras/`
- `05_llm_rag_pdf_chatbot/`

---

## Projetos do Portfólio

> Os projetos são desenvolvidos progressivamente junto com uma trilha estruturada de aprendizagem.  
> Cada projeto tem sua própria pasta com código, notebooks e README detalhado.  
> Projetos planejados ou em andamento podem ser listados antes da criação de suas pastas.

### 01 · Fundamentos Estatísticos — Regressão de Custos de Seguro
[`📁 01_statistical_foundations_insurance_cost_regression/`](01_statistical_foundations_insurance_cost_regression/) · *Status: Concluído*

Aplicação de um fluxo estatístico completo no Medical Cost Personal Dataset:
- análise exploratória e estatística inferencial,
- regressão linear múltipla com diagnósticos e inferência robusta,
- validação com train/test split e validação cruzada.

**Stack:** Python · NumPy · pandas · statsmodels · matplotlib · seaborn · scipy

---

### 02 · Business Analytics — EDA & Storytelling com Dados Reais
`📁 02_eda_olist_storytelling/` · *Status: Em andamento*

Análise exploratória de dados e **storytelling de negócio** em um dataset real brasileiro
(ex.: Olist), com:
- hipóteses bem definidas,
- EDA e testes estatísticos básicos,
- notebook narrativo com foco em stakeholders de negócio.

**Stack:** Python · pandas · seaborn · matplotlib · scipy

---

### 03 · Pipeline de ML — Aprendizado Supervisionado & Avaliação
`📁 03_ml_supervised_pipeline/` · *Status: Planejado*

Pipeline de **ML supervisionado** ponta a ponta (churn ou crédito/inadimplência), incluindo:
- engenharia de atributos,
- comparação de modelos (regressão logística vs. modelos baseados em árvore),
- avaliação além da acurácia (ROC, PR, F1 etc.).

**Stack:** Python · scikit-learn · pandas · matplotlib · seaborn

---

### 04 · Deep Learning — Classificação de Texto com Keras
`📁 04_text_classification_keras/` · *Status: Planejado*

**Classificação de texto** (sentimento/spam) com Keras, conectando ML clássico e deep learning:
- modelo de sequência simples (Embedding + LSTM/GRU ou 1D CNN),
- comparação com baseline TF-IDF + regressão logística.

**Stack:** Python · TensorFlow/Keras · scikit-learn · pandas · matplotlib

---

### 05 · LLM & RAG — Chatbot com PDFs de Domínio Específico
`📁 05_llm_rag_pdf_chatbot/` · *Status: Planejado*

Sistema **Retrieval-Augmented Generation (RAG)** sobre um corpus documental focado
(ex.: saúde, legislação ou relatórios técnicos), com:
- ingestão, chunking, embeddings e busca vetorial,
- decisões arquiteturais documentadas e avaliação básica da qualidade das respostas.

**Stack:** Python · LangChain / LlamaIndex · vector store · LLM API / LLM open-source

---

## Trabalhos Acadêmicos Anteriores (Capstones / TCCs)

> Dois projetos acadêmicos concluídos, com código, dados e relatórios.

### A · Avaliação de Redes Neurais Generativas em Saúde Pública — Estudo de Caso em Malária
[`📁 90_tcc_usp_malaria/`](90_tcc_usp_malaria/) · *TCC MBA — USP/Esalq (2025)*

Avaliou a **legibilidade, similaridade textual e consistência** de respostas de 10 sistemas baseados em LLM sobre malária, usando fichas técnicas da OMS como referência.

- Legibilidade: Flesch Reading Ease, Flesch-Kincaid Grade Level
- Similaridade textual: cosseno (TF-IDF), distância de Levenshtein, similaridade de Jaccard
- Ranking composto por normalização min-max entre métricas
- Aprendizado não supervisionado: clustering K-Means (k por Elbow & Silhouette)
- Validação estatística: ANOVA one-way, Qui-quadrado
- Análise de Correspondência Múltipla (MCA): mapas 2D + 3D interativo (modelos × tópicos × clusters)

**Resultado:** identificou três clusters estatisticamente distintos de modelos, mostrou como o tópico da pergunta direciona o comportamento dos modelos e propôs uma metodologia reutilizável para auditoria de IA generativa em contextos sensíveis de saúde.

**Stack:** Python · pandas · scikit-learn · textstat · python-Levenshtein · pingouin · prince · plotly · seaborn

---

### B · Análise de Potencial Eólico Offshore — Aplicação Web em R Shiny (Bacia de Campos)
[`📁 91_tcc_ifrj_offshore_wind/`](91_tcc_ifrj_offshore_wind/) · *TCC Especialização — IFRJ (2024)*

Desenvolveu uma **aplicação web interativa em R Shiny** para analisar potencial eólico offshore
em nove plataformas de petróleo descomissionadas na Bacia de Campos, seguindo processo **CRISP-DM**.

- Dados: reanálise climática ERA5 (NetCDF) + estação INMET para validação
- Processamento: velocidade e direção do vento a partir dos componentes u/v, análise sazonal, séries temporais
- Modelagem: potencial físico de turbina por plataforma (rho, área varrida, eta, v³)
- Visualização: mapas de velocidade, campos de direção e potencial por plataforma
- Validação: comparação com dados da estação meteorológica de São Tomé

**Resultado:** mostrou que o reaproveitamento de plataformas descomissionadas pode oferecer geração eólica offshore competitiva e mais consistente, apoiando a estratégia de transição energética do Brasil.

**Stack:** Python (`cdsapi`, `xarray`) · R (`shiny`, `ggplot2`, `ncdf4`, `viridis`, `maps`, `grid`)

---

## Referências Técnicas

Este portfólio é apoiado por uma trilha estruturada de estudos que combina fundamentos
estatísticos, analytics de negócio, machine learning aplicado, sistemas de ML,
deep learning e engenharia de IA.

Referências selecionadas:

- *Naked Statistics* — Charles Wheelan, 2013
- *Data Science for Business* — Foster Provost & Tom Fawcett, 2013
- *Essential Math for Data Science* — Thomas Nield, 2022
- *Python for Data Analysis*, 3ª ed. — Wes McKinney, 2022
- *Hands-On Machine Learning*, 3ª ed. — Aurélien Géron, 2022
- *Designing Machine Learning Systems* — Chip Huyen, 2022
- *Machine Learning Design Patterns* — Valliappa Lakshmanan, Sara Robinson & Michael Munn, 2020
- *Deep Learning with Python*, 2ª ed. — François Chollet, 2021
- *Hands-On Large Language Models* — Jay Alammar & Maarten Grootendorst, 2024
- *AI Engineering* — Chip Huyen, 2024/2025

---

## Contato

- **Email:** vinicius98freire@gmail.com
- **LinkedIn:** [marcus-vinicius-freire-junior](https://www.linkedin.com/in/marcus-vinicius-freire-junior/)
- **Localização:** Rio de Janeiro, Brasil

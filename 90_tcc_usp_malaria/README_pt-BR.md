# Avaliação de Modelos de IA Generativa em Saúde Pública - Estudo de Caso sobre Malária

> **TCC MBA - USP/Esalq (Data Science & Analytics, 2025)**  
> Parte do [data-science-portfolio](../README_pt-BR.md) - seção de Trabalhos Acadêmicos Anteriores.

Este projeto avalia a qualidade das respostas geradas por 10 sistemas baseados em
LLMs sobre perguntas relacionadas à malária, usando fichas informativas oficiais
da OMS (Organização Mundial da Saúde) como fonte de referência. O estudo propõe
uma metodologia reutilizável para auditar respostas de IA generativa em contextos
sensíveis de saúde pública.

- **Autor:** Marcus Vinicius Freire Junior  
- **Orientador:** Lucas Lacerda de Souza  
- **Programa:** MBA em Data Science & Analytics - USP/Esalq  
- **Ano:** 2025

---

## Arquivos do Projeto

- Notebook resumo em inglês: `notebooks/90_tcc_usp_malaria_summary.ipynb`
- Notebook resumo em português: `notebooks/90_tcc_usp_malaria_resumo_ptBR.ipynb`
- Implementação original completa: `code/TCC_MBA_DSA_USP_MALARIA.py`
- Bases de respostas originais: `data/*.xlsx`
- Bases de respostas em português: `data/data_pt/*.xlsx`
- Figuras e gráfico interativo pré-calculados: `figures/`
- Tabelas de resultados pré-calculadas: `results/`

---

## Estrutura do Repositório

```text
90_tcc_usp_malaria/
├── code/
│   └── TCC_MBA_DSA_USP_MALARIA.py
├── data/
│   ├── df_*.xlsx
│   └── data_pt/
│       └── df_*_pt.xlsx
├── figures/
│   ├── 01_average_word_count_difference.png
│   ├── ...
│   └── 16_mca_perceptual_map_3d.html
├── notebooks/
│   ├── 90_tcc_usp_malaria_summary.ipynb
│   └── 90_tcc_usp_malaria_resumo_ptBR.ipynb
├── results/
│   ├── df_agg_ranked.xlsx
│   ├── df_agg_topic.xlsx
│   ├── df_agg_topic_cluster.xlsx
│   ├── df_all_responses.xlsx
│   └── df_oms_metrics.xlsx
├── README.md
├── README_pt-BR.md
└── requirements.txt
```

---

## Metodologia

| Etapa | Método |
|---|---|
| Legibilidade | Flesch Reading Ease; Flesch-Kincaid Grade Level |
| Similaridade textual | Similaridade do Cosseno (TF-IDF); Distância de Levenshtein; Coeficiente de Jaccard |
| Ranking composto | Normalização Min-Max entre as métricas |
| Agrupamento | K-Means com padronização por Z-score; k escolhido por Elbow e Silhouette |
| Análise de correspondência | MCA com mapa 2D estático e mapa 3D interativo |
| Validação estatística | ANOVA de uma via; teste Qui-quadrado |

---

## Principais Resultados

- Foram identificados três grupos estatisticamente distintos de respostas, indicando
  padrões mensuráveis de comportamento entre os sistemas de IA.
- O tema da pergunta influenciou fortemente a segmentação, sugerindo que o conteúdo
  do prompt pode moldar a estratégia de resposta tanto quanto o modelo escolhido.
- ScholarGPT e ChatGPT 4.0 apresentaram os melhores desempenhos compostos neste
  estudo, combinando legibilidade, similaridade semântica e alinhamento lexical.
- A metodologia proposta pode ser reutilizada para auditar respostas de IA
  generativa em saúde, regulação e outros domínios sensíveis.

---

## Saídas

- Rankings gerais e por tema dos sistemas de IA
- Matriz de correlação de Pearson entre as métricas
- Gráficos de definição de clusters pelos métodos Elbow e Silhouette
- Boxplots e gráficos de barras comparativos
- Mapas perceptuais MCA: `figures/15_mca_perceptual_map_2d.png` e `figures/16_mca_perceptual_map_3d.html`
- Tabelas agregadas de resultados: `results/df_agg_ranked.xlsx` e `results/df_agg_topic_cluster.xlsx`

---

## Configuração e Execução

Instale os pacotes Python necessários:

```bash
pip install -r requirements.txt
```

Execute o script principal a partir da pasta deste projeto:

```bash
python code/TCC_MBA_DSA_USP_MALARIA.py
```

O repositório já inclui figuras e tabelas pré-calculadas para revisão no portfólio.
O script pode regenerar o gráfico MCA 3D interativo em
`figures/16_mca_perceptual_map_3d.html`; algumas exportações estáticas permanecem
comentadas na implementação original para preservar o fluxo do TCC.

---

## Citação

FREIRE JUNIOR, Marcus Vinicius. Avaliação de Modelos de Inteligência Artificial
Generativa em Comparação com Informações da OMS sobre Malária. Trabalho de
Conclusão de Curso (MBA em Data Science and Analytics) - Universidade de São
Paulo, Escola Superior de Agricultura "Luiz de Queiroz", 2025.

---

> Voltar ao portfólio: [data-science-portfolio](../README_pt-BR.md)

# Pipeline de ML Supervisionado — Previsão de Churn de Clientes

> 🇺🇸 English version: [README.md](README.md)
> Parte de [data-science-portfolio](../README.md)
> Notebook: [03_ml_supervised_pipeline.ipynb](notebooks/03_ml_supervised_pipeline.ipynb)
> Status: Concluído
> [![CI - 03 ML Supervised Pipeline](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-03-ml-supervised-pipeline.yml/badge.svg)](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-03-ml-supervised-pipeline.yml)

Este projeto constrói um **pipeline de machine learning supervisionado** ponta a
ponta sobre o dataset **Telco Customer Churn** (Kaggle), com a perspectiva de um
Head de Customer Success / Retenção que precisa saber quais clientes tendem a
cancelar, por quê, e qual modelo melhor sustenta uma campanha de retenção.

O notebook combina:
- hipóteses de modelagem definidas **antes** de treinar qualquer modelo,
- entendimento e limpeza dos dados (um problema conhecido de tipagem em
  `TotalCharges`),
- engenharia de atributos (atributos derivados de engajamento e tenure) e um
  pré-processamento via `ColumnTransformer` + `Pipeline`,
- comparação de modelos — Regressão Logística vs. dois ensembles baseados em
  árvore (Random Forest, Gradient Boosting) — com o Random Forest ajustado por
  um checklist completo de boas práticas (`RandomizedSearchCV`) e os outros
  dois via `GridSearchCV`,
- avaliação além da acurácia (matriz de confusão, curvas ROC/PR, F1, ajuste de
  threshold) e interpretabilidade dos modelos,
- e storytelling de negócio: achados, implicações e ações recomendadas.

---

## Pergunta de Negócio

Quais clientes tendem a cancelar o serviço, quais fatores mais pesam nessa
decisão, e qual modelo entrega o melhor trade-off entre precisão e recall para
orientar ações de retenção direcionadas?

---

## Dataset

- Fonte: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Cobertura: 7.043 clientes de uma operadora de telecom, 21 colunas
- Alvo: `Churn` (binário), desbalanceado — 26,54% de classe positiva
- Variáveis-chave: `tenure`, `Contract`, `InternetService`, `MonthlyCharges`,
  `TotalCharges`, além de serviços adicionais (`OnlineSecurity`, `TechSupport`, etc.)

Os dados são baixados no notebook via API do Kaggle em `data/raw/`.

---

## Resumo da Metodologia

1. Contexto de negócio e hipóteses de modelagem
2. Entendimento e qualidade dos dados (strings vazias em `TotalCharges` para
   `tenure = 0`, checagem de desbalanceamento do alvo)
3. EDA direcionada (churn vs. tenure, tipo de contrato, serviço de internet)
4. Engenharia de atributos (tratamento de `TotalCharges`, atributos derivados
   `num_add_on_services` e `tenure_group`) e split treino/teste estratificado 80/20
5. Pré-processamento (`ColumnTransformer`: escala + one-hot encoding) e
   comparação de modelos — Regressão Logística vs. Random Forest vs. Gradient
   Boosting, todos com métrica `roc_auc` sob CV estratificada 5-fold. O Random
   Forest segue um checklist completo de boas práticas cobrindo `n_estimators`,
   `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`,
   `bootstrap`, `ccp_alpha` e `criterion` — buscado via `RandomizedSearchCV`
   (40 combinações amostradas), já que um grid exaustivo nesse espaço seria
   computacionalmente inviável; Regressão Logística e Gradient Boosting usam
   `GridSearchCV` sobre grids menores
6. Avaliação além da acurácia: matriz de confusão, ROC-AUC, PR-AUC, F1 e análise
   de threshold de decisão — incluindo uma **matriz de custo-benefício** por
   cliente, que converte a matriz de confusão em valor monetário esperado
7. Interpretabilidade: coeficientes da regressão logística vs. feature
   importances dos modelos em árvore
8. Principais insights e storytelling de negócio
9. Conclusões e próximos passos

---

## Resultados dos Modelos (conjunto de teste, n = 1.409)

| Modelo | Accuracy | Precision (churn) | Recall (churn) | F1 (churn) | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Regressão Logística | 0,733 | 0,498 | **0,791** | 0,612 | 0,842 | 0,636 |
| Random Forest | 0,755 | 0,526 | **0,794** | 0,633 | 0,843 | 0,651 |
| **Gradient Boosting** | **0,798** | **0,656** | 0,505 | 0,571 | **0,846** | **0,664** |

O Gradient Boosting vence em capacidade de ranqueamento (ROC-AUC / PR-AUC) e em
acurácia, mas a Regressão Logística e o Random Forest — ambos treinados com
`class_weight='balanced'` — vencem em recall de churn no threshold padrão de
0,5. Ajustando o threshold do Gradient Boosting para 0,324 (ótimo por F1), sua
recall sobe de 0,505 para 0,757 e seu F1 sobe de 0,571 para 0,640.

**Busca de hiperparâmetros do Random Forest:** seguindo um checklist completo
de boas práticas (entendimento do problema → preparo dos dados → split →
desenho de hiperparâmetros → busca com validação cruzada → validação final),
o `RandomizedSearchCV` amostrou 40 combinações entre `n_estimators`,
`max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`,
`bootstrap`, `ccp_alpha` e `criterion`. Configuração vencedora:
`n_estimators=200`, `max_depth=15`, `min_samples_split=2`,
`min_samples_leaf=10`, `max_features='log2'`, `criterion='gini'`,
`bootstrap=True`, `ccp_alpha=0.0` (ROC-AUC em CV de 0,848 — praticamente
empatado com o 0,850 do Gradient Boosting e à frente do 0,846 da Regressão
Logística sob validação cruzada).

---

## Hipóteses e Resultados

| # | Hipótese | Resultado |
|---|---|---|
| H1 | Modelos baseados em árvore superam a regressão logística em poder discriminativo | **Parcialmente confirmada** — o Gradient Boosting lidera em ROC-AUC/PR-AUC, mas no threshold padrão sua recall de churn fica bem abaixo da Regressão Logística/Random Forest, balanceados por classe |
| H2 | Regressão logística e modelos em árvore concordam sobre os principais drivers de churn | **Confirmada** — `Contract`, `tenure` e `InternetService = Fiber optic` aparecem no top 5 tanto da Regressão Logística quanto do Gradient Boosting |
| H3 | A acurácia isolada é uma métrica enganosa dado o desbalanceamento de classes | **Confirmada** — o Gradient Boosting tem a maior acurácia (0,798) e a menor recall de churn (0,505) dos três modelos |

---

## Análise de Custo-Benefício

Uma matriz de confusão conta acertos e erros, mas não diz quanto cada erro
custa nem quanto cada acerto vale. A seção 6.1 do notebook a converte em uma
**matriz de custo-benefício**, valorando cada célula com o `MonthlyCharges`
real de cada cliente do teste, em vez de uma média genérica. Premissas
(julgamento de negócio, não derivadas dos dados — declaradas explicitamente
para poderem ser contestadas):

| Célula | Condição | Valor |
|---|---|---|
| Verdadeiro Negativo | previsto fica, ficou | R$ 0 (nenhuma ação) |
| Falso Positivo | previsto cancela, ficou | −1× `MonthlyCharges` (oferta desperdiçada) |
| Falso Negativo | previsto fica, cancelou | −12× `MonthlyCharges` (receita futura perdida) |
| Verdadeiro Positivo | previsto cancela, cancelou | 0,30 × 12× `MonthlyCharges` − 1× `MonthlyCharges` (30% de taxa de sucesso na retenção) |

**Achado inesperado:** no threshold padrão de 0,5, **os três modelos ficam
abaixo do baseline ingênuo "contatar todos"** (R$ +7.672 no conjunto de
teste) — o valor esperado do Gradient Boosting é R$ −120.113, do Random
Forest R$ −26.825, da Regressão Logística R$ −20.730. Nenhum tem recall de
churn alta o suficiente nesse threshold para compensar o quanto um churner
não detectado custa (12x uma oferta desperdiçada). Um modelo estatisticamente
forte (ROC-AUC ≈ 0,84) pode destruir mais valor do que uma política sem
nenhuma inteligência, se implantado no threshold padrão.

Ajustando o threshold de decisão pelo valor líquido esperado (não por F1)
para os três modelos, o cenário se inverte: todos superam o baseline
"contatar todos" uma vez recalibrados, e **o threshold ótimo por valor
líquido é bem mais agressivo do que o ótimo por F1** (0,08 vs. 0,324 para o
Gradient Boosting).

| Modelo | Valor @ 0,5 (R$) | Threshold ótimo (lucro) | Valor nesse threshold (R$) |
|---|---|---|---|
| **Gradient Boosting** | −120.113 | **0,08** | **19.964** |
| Regressão Logística | −20.730 | 0,12 | 19.685 |
| Random Forest | −26.825 | 0,24 | 19.115 |

O Gradient Boosting ainda vence depois de recalibrado, mas por menos de 1,5%
sobre a Regressão Logística e o Random Forest — **os três praticamente
empatados** nos seus respectivos thresholds ótimos, apesar de uma diferença
visível de ROC-AUC entre o Gradient Boosting e os outros dois. O threshold de
decisão, não a escolha do algoritmo, é a alavanca de maior impacto financeiro
encontrada nesta análise.

---

## Principais Achados

- **Capacidade de ranqueamento e desempenho no ponto de operação não são a
  mesma coisa.** O Gradient Boosting tem o melhor ROC-AUC (0,846) e PR-AUC
  (0,664), mas sem balanceamento de classe sua recall de churn no threshold
  padrão (0,505) fica bem abaixo da Regressão Logística (0,791) / Random
  Forest (0,794) balanceados — escolher o modelo só pela AUC teria
  selecionado o pior modelo para um caso de uso de retenção.
- **O ajuste de threshold pesa tanto quanto a escolha do modelo**: mover o
  threshold de decisão do Gradient Boosting de 0,5 para 0,324 (ótimo por F1)
  eleva a recall de churn de 0,505 para 0,757 — uma troca deliberada de
  precisão por recall, adequada a um contexto de retenção onde deixar de agir
  sobre um cliente que cancela custa mais do que uma oferta de retenção
  desnecessária.
- **No threshold padrão, todos os modelos destroem valor em relação a uma
  política ingênua de "contatar todos"** sob as premissas de custo-benefício
  da seção abaixo (Gradient Boosting: R$ −120.113 vs. R$ +7.672 do baseline).
  Recalibrar o threshold pelo valor líquido esperado — não por F1 — é o que
  torna os modelos viáveis de implantar (melhor caso: R$ 19.964, Gradient
  Boosting no threshold 0,08).
- **Tipo de contrato é o driver isolado mais forte de churn**: clientes com
  contrato mensal cancelam a 42,7%, contra 11,3% no plano anual e 2,8% no
  bianual.
- **Clientes de internet via fibra ótica cancelam a mais do dobro da taxa do
  DSL** (41,9% vs. 19,0%), independentemente do tipo de contrato — vale
  investigar preço, qualidade de serviço ou pressão competitiva.
- **A ausência de serviços adicionais é um sinal de risco no modelo em
  árvore**: a falta de `OnlineSecurity` e `TechSupport` está entre os
  principais preditores do Gradient Boosting, junto com `tenure` e `Contract`.

---

## Recomendação Final de Modelo & Threshold

Ponto de operação recomendado, escolhido a partir da análise de
custo-benefício, não apenas do ROC-AUC:

- **Modelo:** Gradient Boosting
- **Threshold de decisão:** **0,08** (não o padrão 0,5, nem o ótimo por F1
  de 0,324 encontrado na seção 6.3 do notebook)
- **Valor líquido esperado no conjunto de teste:** R$19.963,87, contra
  R$7.672,44 do baseline ingênuo "contatar todos"

Por que esse modelo e threshold:
- O Gradient Boosting tem o melhor ROC-AUC em validação cruzada (0,8497),
  mas a margem sobre o Random Forest (0,8481) e a Regressão Logística
  (0,8464) é pequena, quase um empate triplo estatístico.
- Depois de recalibrar cada modelo para seu próprio threshold ótimo por
  lucro, o Gradient Boosting ainda vence, mas por apenas **1,42%** sobre a
  Regressão Logística (R$19.685,14 @ 0,12) e **4,44%** sobre o Random Forest
  (R$19.114,98 @ 0,24). Se interpretabilidade pesar mais que essa margem
  pequena, a Regressão Logística no threshold 0,12 é uma alternativa
  defensável.
- Esse modelo **não pode** ser implantado no threshold padrão de 0,5: nesse
  ponto ele destrói R$120.113,14 de valor esperado em relação ao baseline
  ingênuo (ver Análise de Custo-Benefício).

---

## Retrato de Validação

Desempenho do modelo recomendado no score de validação cruzada e nos
thresholds padrão e recomendado:

| Métrica | CV (5-fold) | Teste @ threshold 0,5 | Teste @ threshold 0,08 (recomendado) |
|---|---|---|---|
| ROC-AUC | 0,8497 | 0,8455 | independente de threshold |
| Accuracy | n/a | 0,7984 | 0,5798 |
| Precision (churn) | n/a | 0,6562 | 0,3843 |
| Recall (churn) | n/a | 0,5053 | 0,9679 |
| F1 (churn) | n/a | 0,5710 | 0,5502 |
| Valor líquido esperado (R$) | n/a | −120.113,14 | 19.963,87 |

No threshold recomendado, o modelo sinaliza quase todo churner provável
(recall de 96,8%) ao custo de precisão (38,4%) e acurácia (58,0%) bem
menores que no threshold padrão. Essa troca é intencional: dada a assimetria
de custo na matriz de custo-benefício (um churner não detectado custa 12x
uma oferta de retenção desperdiçada), o modelo deve errar fortemente para o
lado de sinalizar demais. As métricas de classificação isoladas fazem esse
ponto de operação parecer pior que o threshold padrão; só a visão de
custo-benefício captura por que ele é, de fato, a escolha melhor.

---

## Estrutura do Repositório

```text
03_ml_supervised_pipeline/
|-- data/                                    # ignorado no git
|   |-- raw/                                 # gerado pelo download via Kaggle no notebook
|   `-- processed/                           # reservado para datasets derivados
|-- notebooks/
|   `-- 03_ml_supervised_pipeline.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## Como Executar

1. Acesse a pasta do projeto:

```bash
cd 03_ml_supervised_pipeline
```

2. Crie e ative um ambiente virtual (opcional se já usa conda):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure a API do Kaggle:
- Gere o token nas configurações da sua conta Kaggle.
- Salve `kaggle.json` em:
  - Windows: `C:\Users\<SEU_USUARIO>\.kaggle\kaggle.json`
  - Linux/Mac: `~/.kaggle/kaggle.json`

5. Abra e execute:

```text
notebooks/03_ml_supervised_pipeline.ipynb
```

---

## Observações

- Não versione credenciais (`kaggle.json`) nem pastas de ambiente virtual.
- O CSV bruto do Telco Customer Churn é baixado localmente e excluído via
  `.gitignore`; rode o notebook novamente para regerá-lo.
- O Gradient Boosting do scikit-learn não tem suporte nativo a `class_weight`,
  diferente da Regressão Logística e do Random Forest — essa assimetria é a
  causa direta de sua recall menor no threshold padrão, e é endereçada por
  ajuste de threshold em vez de reamostragem nesta iteração (ver Próximos
  Passos no notebook).
- Todas as métricas reportadas vêm de um único split de teste (sem CV
  aninhada); o notebook lista validação cruzada aninhada como próximo passo
  para uma estimativa de generalização menos otimista.
- As premissas de custo-benefício (custo de oferta de 1 mês, 30% de taxa de
  sucesso na retenção, horizonte de receita de 12 meses) são julgamento de
  negócio ilustrativo, não derivadas do dataset — uma análise de
  sensibilidade sobre essas premissas está listada como próximo passo.
- **CI:** [`.github/workflows/ci-03-ml-supervised-pipeline.yml`](../.github/workflows/ci-03-ml-supervised-pipeline.yml)
  reexecuta este notebook do início ao fim em todo push/PR que altere esta
  pasta, para pegar regressões de reprodutibilidade (drift do dataset, APIs de
  bibliotecas depreciadas). O download do dataset usa a API do Kaggle via os
  secrets `KAGGLE_USERNAME`/`KAGGLE_KEY` do repositório — configure-os em
  Settings → Secrets and variables → Actions no GitHub para o workflow rodar.

---

> Voltar ao portfólio: [data-science-portfolio](../README.md)

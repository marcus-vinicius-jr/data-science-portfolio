# Classificação de Texto com Keras — Sentimento de Companhias Aéreas no Twitter

> 🇺🇸 English version: [README.md](README.md)
> Parte do [data-science-portfolio](../README_pt-BR.md)
> Notebook: [04_text_classification_keras.ipynb](notebooks/04_text_classification_keras.ipynb)
> Status: Concluído
> [![CI - 04 Text Classification Keras](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-04-text-classification-keras.yml/badge.svg)](https://github.com/marcus-vinicius-jr/data-science-portfolio/actions/workflows/ci-04-text-classification-keras.yml)

Este projeto constrói um **pipeline de classificação de texto com Keras** no
dataset Twitter US Airline Sentiment (Kaggle), com a perspectiva de um Head
de Customer Experience Digital / Central de Redes Sociais de uma grande
companhia aérea americana que precisa triar o volume de tweets que mencionam
a empresa quase em tempo real, em vez de depender de revisão manual de cada
@menção.

O notebook combina:
- hipóteses de modelagem definidas antes de treinar qualquer modelo,
- entendimento e checagem de qualidade dos dados (tweets duplicados, ruído de
  rótulo) e EDA direcionada (sentimento por companhia aérea, principais
  motivos de reclamação, distribuição do tamanho dos tweets),
- um pipeline de limpeza de texto construído do zero, com uma lista de
  stopwords que preserva negações para o baseline clássico,
- um **baseline TF-IDF + Regressão Logística** comparado a dois modelos de
  sequência neural, **Embedding + LSTM** e **Embedding + 1D CNN**,
  construídos seguindo um framework explícito de seis passos para redes
  neurais (preparação dos dados, arquitetura, inicialização dos pesos,
  forward propagation, backpropagation, treinamento), com checagem explícita
  de overfitting em cada etapa,
- avaliação além da acurácia (macro-F1, precisão/recall por classe, matrizes
  de confusão, ROC-AUC multiclasse),
- uma seção de ajuste de threshold orientada a negócio, reformulando o
  problema de 3 classes como o gatilho binário "este tweet precisa de um
  humano agora?", além de uma análise ponderada por exposição (retweets) dos
  tweets negativos perdidos,
- interpretabilidade tanto para o baseline linear (coeficientes) quanto para
  o embedding neural (palavras vizinhas mais próximas), e
- storytelling de negócio: achados, implicações e recomendação final de
  modelo/threshold.

---

## Pergunta de Negócio

O sentimento de um tweet que menciona a companhia aérea pode ser classificado
com precisão suficiente para priorizar quais tweets uma equipe de
atendimento ao cliente ao vivo deve ver primeiro, e qual abordagem de
representação de texto (bag-of-words vs. embeddings aprendidos) oferece o
melhor ponto de operação para essa decisão de triagem?

---

## Dataset

- Fonte: [Twitter US Airline Sentiment (Crowdflower / Kaggle)](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)
- Cobertura: 14.640 tweets direcionados a seis companhias aéreas americanas
  (United, US Airways, American, Southwest, Delta, Virgin America); 14.485
  após remover 155 linhas com `tweet_id` exatamente duplicado
- Alvo: `airline_sentiment` (3 classes), desbalanceado: negative 62,69%,
  neutral 21,17%, positive 16,14%
- Variáveis-chave: `text` (única entrada dos modelos), `airline`,
  `negativereason` (preenchido só para tweets negativos), `retweet_count`,
  `airline_sentiment_confidence`

Os dados são baixados no próprio notebook via API do Kaggle para `data/raw/`.

---

## Resumo da Metodologia

1. Contexto de negócio, persona e hipóteses de modelagem (H1-H3)
2. Entendimento e qualidade dos dados (padrão de ausência, 155 linhas
   duplicadas por `tweet_id` removidas, checagem de ruído de rótulo em
   textos duplicados)
3. EDA direcionada (sentimento por companhia aérea, principais motivos
   negativos, distribuição do tamanho dos tweets)
4. Limpeza de texto (lista de stopwords que preserva negações, tratamento de
   hashtags/menções) e divisão estratificada 70/15/15 em treino/validação/teste
5. Baseline: TF-IDF + Regressão Logística, ajustado via `GridSearchCV` com
   validação cruzada de 5 folds, pontuado por macro-F1
6. Deep learning: um framework explícito de rede neural aplicado uma vez, e
   então duas arquiteturas construídas sobre ele, Embedding + LSTM e
   Embedding + 1D CNN, ambas com `class_weight` para o desbalanceamento e
   `EarlyStopping` monitorando a perda de validação
7. Comparação de modelos e avaliação além da acurácia (matrizes de confusão,
   precisão/recall/F1 por classe, macro-F1, ROC-AUC macro)
8. Ajuste de threshold orientado a negócio (triagem negative vs. not-negative)
   e análise ponderada por exposição (`retweet_count`) dos tweets perdidos
9. Interpretabilidade (coeficientes da Regressão Logística; vizinhos mais
   próximos no embedding)
10. Hipóteses e resultados, principais achados, storytelling de negócio
11. Conclusões e próximos passos

---

## Resultados dos Modelos (conjunto de teste, n = 2.173)

| Modelo | Acurácia | Macro F1 | F1 Ponderado | ROC-AUC Macro (OvR) |
|---|---|---|---|---|
| TF-IDF + Regressão Logística | 0,7607 | 0,7101 | 0,7668 | 0,8862 |
| **Embedding + LSTM** | **0,7911** | **0,7326** | **0,7913** | 0,8868 |
| Embedding + 1D CNN | 0,7713 | 0,7212 | 0,7752 | **0,8923** |

Embedding + LSTM vence em acurácia, macro-F1 e F1 ponderado; Embedding + 1D
CNN vence em ROC-AUC macro, embora os três valores de ROC-AUC fiquem numa
faixa de apenas 0,006, essencialmente um empate triplo em capacidade de
ranqueamento, mesmo com o macro-F1 separando claramente os modelos.

**Por que macro-F1, e não F1 ponderado ou acurácia, é a métrica principal:**
o F1 ponderado calcula a média dos três F1 por classe ponderando pelo
tamanho de cada classe, então fica dominado pela classe majoritária
`negative` e se mantém a até 0,6 ponto da acurácia em todo modelo (ex.: LSTM:
F1 ponderado 0,7913 vs. acurácia 0,7911). O macro-F1 calcula a média dos três
F1 sem ponderação, então o F1 bem mais fraco de `neutral` (0,5994 a 0,6346
entre os modelos) puxa o resultado 5 a 6 pontos abaixo da acurácia/F1
ponderado em todo modelo. Essa diferença é exatamente o que a H2 testa: uma
métrica que deixa uma classe minoritária fraca se esconder atrás de uma
classe majoritária forte faria todo modelo aqui parecer melhor do que
realmente é nos tweets `neutral`.

**Recall por classe** (a métrica mais exposta pelo desbalanceamento):

| Classe | TF-IDF + LogReg | Embedding + LSTM | Embedding + 1D CNN |
|---|---|---|---|
| negative | 0,8085 | 0,8701 | 0,8217 |
| neutral | 0,6652 | 0,6457 | 0,6391 |
| positive | 0,7000 | 0,6743 | 0,7486 |

A classe mais fraca de todo modelo é `neutral`, não `positive`, mesmo
`positive` sendo a classe menor (16,1% vs. 21,2% dos tweets).

---

## Hipóteses & Resultados

| # | Hipótese | Resultado |
|---|---|---|
| H1 | Embedding + LSTM / 1D CNN superam o baseline TF-IDF + Regressão Logística em macro-F1 | **Confirmada.** O LSTM alcançou macro-F1 0,7326 (+3,2% relativo frente aos 0,7101 do baseline) e o CNN alcançou 0,7212 (+1,6% relativo); ambos superam o baseline em toda métrica principal. |
| H2 | A acurácia superestima o desempenho nas classes minoritárias dado o desbalanceamento da classe negative | **Parcialmente confirmada.** A acurácia superou o macro-F1 em 5 a 6 pontos em todo modelo, confirmando a alegação central, mas a classe mais difícil foi `neutral` (21,2% dos tweets), não a classe menor `positive` (16,1%) como hipotetizado. O tamanho da classe sozinho não previu a dificuldade; tweets `neutral` parecem intrinsecamente mais ambíguos. |
| H3 | O 1D CNN treina mais rápido que o LSTM com desempenho de classificação comparável | **Confirmada.** O CNN treinou 2,21x mais rápido por época (3,83s vs. 8,46s) e convergiu em menos épocas (5 vs. 6), alcançando 98,4% do macro-F1 de teste do LSTM (0,7212 vs. 0,7326). |

---

## Threshold Orientado a Negócio & Análise Ponderada por Exposição

A seção 8 do notebook reformula a saída de 3 classes do melhor modelo
(Embedding + LSTM) como um gatilho binário de triagem "negative vs.
not-negative", a decisão acionável para uma equipe de atendimento ao vivo, e
varre o threshold de decisão em vez de usar o corte padrão de 0,5 que um
`argmax` usa implicitamente:

| Threshold | Precisão | Recall | Regra de seleção |
|---|---|---|---|
| 0,186 | 0,8279 | 0,9318 | ótimo por F1 |
| **0,119** | 0,7979 | 0,9501 | prioridade de recall (pelo menos 95% de recall em `negative`) |

Baixar o threshold do padrão 0,5 para o recomendado 0,119 reduz os **tweets
negativos perdidos em 65,8%** (de 199 para 68 no conjunto de teste), ao custo
de encaminhar mais tweets para a fila de triagem (de 61,11% para 74,69% de
todos os tweets de teste). Usando `retweet_count` como proxy de
visibilidade/exposição, a contagem máxima de retweets entre os tweets
perdidos ficou em 2 sob ambos os thresholds, bem abaixo dos 32 retweets do
tweet negativo mais retuitado do conjunto de teste, então mesmo o threshold
padrão não estava perdendo desproporcionalmente as reclamações de maior
visibilidade; `retweet_count` em si é um sinal fraco neste dataset (média de
0,092 entre todos os tweets negativos de teste).

---

## Principais Achados

- **O deep learning superou o baseline clássico, mas por uma margem
  modesta**: o macro-F1 do Embedding + LSTM (0,7326) é apenas 3,2% melhor
  (relativo) que o do TF-IDF + Regressão Logística (0,7101), evidência de que
  um bag-of-words bem regularizado com bigramas continua sendo um baseline
  forte para texto curto e informal.
- **Tweets `neutral`, não `positive`, são os mais difíceis de classificar**:
  o recall em `neutral` (0,639 a 0,665) foi a classe mais fraca de todo
  modelo, mesmo `positive` sendo a classe menor, e a confusão dominante em
  todo modelo é `neutral` sendo puxado para `negative` (104 a 113 tweets),
  não para `positive` (50 a 58 tweets).
- **O 1D CNN é a escolha pragmática para produção nesta tarefa**: treina
  2,21x mais rápido por época que o LSTM e fica a 1,5 ponto de macro-F1 dele,
  enquanto vence por pouco em capacidade de ranqueamento (ROC-AUC macro
  0,8923 vs. 0,8868).
- **Calibrar o threshold de decisão muda o resultado da triagem mais do que
  a escolha do modelo**: mover de 0,5 para 0,119 reduz os tweets negativos
  perdidos em 65,8%, ao custo de uma fila de triagem maior (61,11% para
  74,69%).
- **O embedding aprendido pelo LSTM se organizou em torno de estrutura real
  de sentimento**, sem nenhuma supervisão explícita no nível da palavra: os
  vizinhos mais próximos de "rude" foram "worst", "unacceptable" e
  "ridiculous"; os vizinhos de "thanks" foram "awesome", "great" e
  "excellent".
- **Os principais coeficientes da classe negative no baseline TF-IDF**
  ("not", "hours", "hold", "worst", "delayed", "cancelled") mapeiam
  diretamente para os principais motivos negativos encontrados na EDA
  ("Customer Service Issue": 2.885 tweets, "Late Flight": 1.650), mostrando
  que o baseline linear capta os mesmos pontos de dor operacional que um
  analista humano apontaria.

---

## Modelo & Threshold Finais Recomendados

- **Modelo:** Embedding + LSTM (macro-F1 de teste 0,7326, acurácia 0,7911, o
  modelo mais forte em toda métrica principal exceto capacidade de
  ranqueamento)
- **Threshold de decisão para o gatilho de triagem negative-vs-not-negative:**
  **0,119** (não o padrão 0,5, nem o ótimo por F1 de 0,186), escolhido para
  garantir pelo menos 95% de recall em `negative`
- **Trade-off aceito:** tweets negativos perdidos caem de 199 para 68 (uma
  redução de 65,8%), ao custo de uma fila de triagem maior (61,11% para
  74,69% dos tweets encaminhados para revisão humana)

Para uma implantação que priorize custo de treino e inferência acima dos
últimos 1,5 ponto de macro-F1, o Embedding + 1D CNN é uma alternativa
defensável: treina 2,21x mais rápido por época e alcança 98,4% do macro-F1
do LSTM.

---

## Estrutura do Repositório

```text
04_text_classification_keras/
|-- data/                                    # gitignored
|   |-- raw/                                 # gerado pelo download do Kaggle no notebook
|   `-- processed/                           # reservado para datasets derivados
|-- notebooks/
|   `-- 04_text_classification_keras.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## Como Executar

1. Vá até a pasta do projeto:

```bash
cd 04_text_classification_keras
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
- Crie um token nas configurações da sua conta Kaggle.
- Salve `kaggle.json` em:
  - Windows: `C:\Users\<SEU_USUARIO>\.kaggle\kaggle.json`
  - Linux/Mac: `~/.kaggle/kaggle.json`

5. Abra e execute:

```text
notebooks/04_text_classification_keras.ipynb
```

---

## Observações

- Não commitar credenciais (`kaggle.json`) nem pastas de ambiente virtual.
- O CSV bruto do Twitter US Airline Sentiment é baixado localmente e
  excluído via `.gitignore`; execute o notebook novamente para regerá-lo. O
  corpus de stopwords do NLTK também é baixado na primeira execução.
- 155 linhas compartilhavam um `tweet_id` exatamente duplicado e foram
  removidas antes da divisão dos dados, para evitar que o mesmo tweet
  aparecesse em treino e teste ao mesmo tempo. Outras 400 linhas têm `text`
  idêntico sob `tweet_id`s diferentes (duplicatas no estilo retweet); 25 dos
  187 textos únicos envolvidos foram rotulados de forma inconsistente por
  diferentes trabalhadores da crowdsourcing, ruído de rótulo real que impõe
  um teto conhecido à acurácia alcançável.
- Ambos os modelos neurais treinam só em CPU: o TensorFlow >= 2.11 não tem
  suporte nativo a GPU no Windows fora do WSL2 ou do plugin DirectML, nenhum
  dos dois configurado para este notebook. Mesmo assim, o treino de cada
  modelo termina em menos de um minuto neste tamanho de dataset.
- Os embeddings de palavras são aprendidos do zero para os dois modelos
  neurais, não carregados de uma fonte pré-treinada (ex.: GloVe); os
  Próximos Passos do notebook listam isso como um teste A/B futuro.
- `neutral` foi a classe mais difícil para todo modelo testado, não
  `positive` como hipotetizado originalmente (H2); o notebook lista um
  follow-up dedicado sobre o porquê em seus Próximos Passos.
- Todas as métricas reportadas são de uma única divisão treino/teste (sem
  validação cruzada aninhada).
- **CI:** [`.github/workflows/ci-04-text-classification-keras.yml`](../.github/workflows/ci-04-text-classification-keras.yml)
  reexecuta este notebook do início ao fim a cada push/PR que toque esta
  pasta, para detectar regressões de reprodutibilidade (deriva do dataset,
  APIs de biblioteca descontinuadas). Ele baixa o dataset via API do Kaggle
  usando os secrets do repositório `KAGGLE_USERNAME`/`KAGGLE_KEY` — configure-os
  em Settings → Secrets and variables → Actions do repositório no GitHub
  para o workflow rodar.

---

> Voltar ao portfólio: [data-science-portfolio](../README_pt-BR.md)

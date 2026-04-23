# Análise de Custos de Seguro e Regressão (Medical Cost Personal Dataset)

> 🇺🇸 English version: [README.md](README.md)  
> Parte de [data-science-portfolio](../README.md)  
> Status: Concluído

Este projeto aplica fundamentos estatísticos e modelagem de regressão para explicar custos de seguro saúde usando o dataset **Medical Cost Personal Dataset** (Kaggle).

O notebook combina:
- análise exploratória de dados (EDA),
- estatística inferencial,
- modelagem linear de nível único (OLS, diagnósticos e inferência robusta),
- validação fora da amostra (train/test + validação cruzada),
- e checagem de viabilidade multinível.

---

## Pergunta de Negócio

Quais fatores explicam os custos individuais de seguro saúde, e qual é o efeito médio de idade, IMC e hábito de fumar sobre `charges`, com incerteza quantificada?

---

## Dataset

- Fonte: [Kaggle - Medical Cost Personal Dataset](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- Linhas: 1.338 indivíduos
- Alvo: `charges`
- Variáveis: `age`, `bmi`, `smoker`, `children`, `sex`, `region`

Os dados são baixados automaticamente no notebook via API do Kaggle em `data/insurance.csv`.

---

## Resumo da Metodologia

1. Contexto e carregamento dos dados
2. EDA (distribuições, comparações por grupo, correlações)
3. Estatística inferencial (fumantes vs não fumantes)
4. Modelagem linear de nível único e diagnósticos
5. Validação sem vazamento + comparação com baseline
6. Checagem de viabilidade multinível (efeitos de região)

---

## Principais Achados

- **Fumar** é o principal driver de custo no dataset.
- **Idade** e **IMC** têm associação positiva consistente com `charges`.
- A variável alvo é assimétrica à direita e heterocedástica.
- Inferência robusta (HC3) é adequada para interpretação dos coeficientes.
- Métricas de validação são estáveis e melhores que baseline da média.
- Efeitos aleatórios por região foram fracos neste dataset (ICC baixo), então não houve ganho claro com expansão multinível.

---

## Recomendação de Modelo Final

Modelo final recomendado (nível único, interpretável e validado):

- Alvo: `charges`
- Preditores: `age`, `bmi`, `children`, `smoker_yes`
- Inferência: OLS com **erros padrão robustos HC3**

Por que este modelo:
- forte interpretabilidade para comunicação de negócio,
- desempenho estável fora da amostra,
- melhora clara em relação ao baseline.

---

## Resumo de Validação

- Treino: `R2 = 0.7411`, `RMSE = 6113.07`, `MAE = 4210.66`
- Teste: `R2 = 0.7811`, `RMSE = 5829.38`, `MAE = 4213.80`
- CV 10-fold (modelo reduzido):
  - `R2 mean = 0.7397` (`std = 0.0619`)
  - `RMSE mean = 6062.68` (`std = 433.17`)
  - `MAE mean = 4192.45` (`std = 250.92`)

---

## Estrutura do Repositório

```text
01_statistical_foundations_insurance_cost_regression/
|-- data/
|   `-- insurance.csv
|-- notebooks/
|   `-- 01_insurance_cost_analysis_regression.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## Como Executar

1. Acesse a pasta do projeto:

```bash
cd 01_statistical_foundations_insurance_cost_regression
```

2. Crie e ative um ambiente virtual (opcional se já usa conda):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

4. Configure a API do Kaggle:
- Gere token nas configurações da sua conta Kaggle.
- Salve `kaggle.json` em:
  - Windows: `C:\Users\<SEU_USUARIO>\.kaggle\kaggle.json`
  - Linux/Mac: `~/.kaggle/kaggle.json`

5. Abra e execute:

```text
notebooks/01_insurance_cost_analysis_regression.ipynb
```

---

## Observações

- Não versione credenciais (`kaggle.json`) nem pastas de ambiente virtual.
- Este projeto prioriza interpretabilidade e rigor estatístico para portfólio.
- A incerteza preditiva é maior para casos de custo muito elevado (cauda superior).

---

> Voltar ao portfólio: [data-science-portfolio](../README.md)

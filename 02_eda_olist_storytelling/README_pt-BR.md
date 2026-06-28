# Business Analytics — EDA e Storytelling com a Olist

> 🇺🇸 English version: [README.md](README.md)  
> Parte de [data-science-portfolio](../README.md)  
> Notebook: [02_eda_olist_storytelling.ipynb](notebooks/02_eda_olist_storytelling.ipynb)  
> Status: Concluído

Este projeto aplica análise exploratória de dados e storytelling de negócio sobre o **Brazilian E-Commerce Public Dataset by Olist** (Kaggle), com a perspectiva de um Head de Operações que precisa transformar gráficos em decisões.

O notebook combina:
- enquadramento de negócio e hipóteses definidas **antes** de olhar os dados,
- entendimento e checagem de qualidade dos dados em múltiplas tabelas relacionais,
- análise exploratória (vendas/receita, entrega, avaliações, geografia),
- validação formal das hipóteses com testes estatísticos,
- e storytelling de negócio: achados, implicações e ações recomendadas.

---

## Pergunta de Negócio

Onde os pedidos se concentram geograficamente, como a performance de entrega afeta a satisfação do cliente, e quais categorias de produto e padrões de pagamento impulsionam a receita, com qual confiança estatística?

---

## Dataset

- Fonte: [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Cobertura: ~100 mil pedidos entre 2016 e 2018
- Linhas após o join principal: 96.478 pedidos entregues
- Variáveis-chave: `order_purchase_timestamp`, `delivery_delay_days`, `review_score`, `total_payment`, `max_installments`, `customer_state`, `product_category_name_english`

Os dados são baixados automaticamente no notebook via API do Kaggle em `data/`.

---

## Resumo da Metodologia

1. Contexto de negócio, hipóteses e carregamento dos dados
2. Entendimento e qualidade dos dados (schema, valores ausentes, feature de atraso, join principal)
3. Análise exploratória (vendas/receita, performance de entrega, avaliações, geografia)
4. Validação das hipóteses com testes estatísticos
5. Principais insights e storytelling de negócio
6. Conclusões e próximos passos

---

## Hipóteses e Resultados dos Testes

| # | Hipótese | Teste | Resultado |
|---|---|---|---|
| H1 | Entregas atrasadas recebem notas de avaliação significativamente menores | Teste t unilateral | **Confirmada** - t = -131,85, p ≈ 0, d de Cohen = 1,47 |
| H2 | A região Sudeste concentra a maior parte da receita | Descritivo (proporção) | **Confirmada** - 64,6% da receita |
| H3 | Mais parcelas se associam a maior valor de pedido | Correlação de Pearson | **Confirmada (moderada)** - r = 0,374, p ≈ 0 |
| H4 | As notas de avaliação diferem entre categorias de produto | ANOVA one-way | **Confirmada** - F = 32,54, p = 1,13e-57 |

---

## Principais Achados

- **A confiabilidade da entrega é o principal driver de satisfação**: pedidos atrasados têm nota média de 2,27 vs. 4,29 para pedidos no prazo/antecipados - uma diferença estatística e praticamente enorme (d de Cohen = 1,47).
- **Receita e satisfação não estão alinhadas geograficamente**: o Sudeste concentra 64,6% da receita, mas o RJ - seu 2º estado em receita - fica abaixo do referencial de 4,0 na nota média de avaliação.
- **Parcelamento se correlaciona com o valor do pedido, mas apenas moderadamente** (r = 0,374); outros fatores (categoria, frete, perfil do cliente) também importam.
- **A categoria de produto influencia a satisfação independentemente da entrega**: telephony e watches_gifts apresentam a maior dispersão para notas baixas; auto, computers_accessories e furniture_decor se concentram mais alto e com menor dispersão.
- O valor do pedido é extremamente assimétrico à direita (assimetria = 9,37); a média (BRL 159,86) fica bem acima da mediana (BRL 105,28).

---

## Estrutura do Repositório

```text
02_eda_olist_storytelling/
|-- data/                                    # gerado pelo download via Kaggle no notebook (ignorado no git)
|-- notebooks/
|   `-- 02_eda_olist_storytelling.ipynb
|-- requirements.txt
|-- .gitignore
|-- README.md
`-- README_pt-BR.md
```

---

## Como Executar

1. Acesse a pasta do projeto:

```bash
cd 02_eda_olist_storytelling
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
notebooks/02_eda_olist_storytelling.ipynb
```

---

## Observações

- Não versione credenciais (`kaggle.json`) nem pastas de ambiente virtual.
- Os CSVs brutos da Olist (~121 MB) são baixados localmente e excluídos via `.gitignore`; rode o notebook novamente para regerá-los.
- Este projeto prioriza o enquadramento de negócio (hipóteses antes da EDA) e rigor estatístico em vez de uma EDA puramente descritiva.
- Correlação não é causalidade: a relação entre atraso na entrega e nota de avaliação é forte e consistente, mas fatores de confusão (expectativa do cliente, qualidade do produto) não foram descartados.

---

> Voltar ao portfólio: [data-science-portfolio](../README.md)

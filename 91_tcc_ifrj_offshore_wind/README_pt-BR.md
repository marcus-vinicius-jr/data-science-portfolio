# Análise do Potencial Eólico Offshore - Aplicação Web em R Shiny (Bacia de Campos)

> English version: [README.md](README.md)  
> **TCC de Especialização - IFRJ (Gestão de Projetos e Negócios em TI, 2024)**  
> Parte de [data-science-portfolio](../README.md) - seção de trabalhos acadêmicos anteriores.

Este projeto avalia o potencial eólico offshore em plataformas descomissionadas na Bacia de Campos e apresenta os resultados por meio de uma aplicação web interativa em R Shiny.

- **Autor:** Marcus Vinicius Freire Junior  
- **Orientadora:** Shirley Nunes Costa Santos  
- **Curso:** Especialização em Gestão de Projetos e Negócios em TI - IFRJ  
- **Ano:** 2024

---

## Aplicação Online

- **Shiny App (publicado):** https://fboewn-marcus-vinicus.shinyapps.io/Myapp/

---

## Estrutura do Repositório

```text
91_tcc_ifrj_offshore_wind/
├── code/
│   ├── Acesso ERA5 API - Login Marcus.ipynb   # Acesso e pré-processamento ERA5 (Python)
│   └── app.R                                  # Aplicação final em R Shiny
├── data/                                      # Artefatos locais opcionais
├── requirements-python.txt                    # Dependências Python (notebook)
├── requirements-r.txt                         # Dependências R (app Shiny)
├── README.md
└── README_pt-BR.md
```

> Observação: arquivos NetCDF grandes não são versionados no repositório.

---

## Problema e Objetivos

O projeto investiga se o aproveitamento eólico offshore na Bacia de Campos é uma alternativa viável, inclusive com possível reaproveitamento de infraestrutura descomissionada.

Objetivos principais:

1. Estimar o comportamento da velocidade do vento e o potencial eólico em pontos offshore selecionados.
2. Comparar plataformas e identificar localizações de maior potencial.
3. Oferecer uma camada visual para apoio à decisão com uma aplicação Shiny publicada.

---

## Metodologia (orientada ao CRISP-DM)

1. **Aquisição dos dados (ERA5):** coleta dos componentes de vento (`u`, `v`) via API.
2. **Processamento:** cálculo de velocidade e direção do vento para coordenadas das plataformas.
3. **Análise espaço-temporal:** mapas, comportamento sazonal e comparação entre plataformas.
4. **Estimativa de potencial:** cálculo nominal com premissas padrão (`rho`, `R`, `A`, `eta`).
5. **Deploy:** aplicação interativa com mapas e comparações para stakeholders.

---

## Visões da Aplicação

A aplicação (`code/app.R`) inclui:

- Mapa da Bacia e localização das plataformas.
- Velocidade média do vento ao longo do tempo.
- Boxplots sazonais de velocidade.
- Mapas de velocidade e direção do vento.
- Ranking das plataformas por potencial eólico estimado.

> O conteúdo da interface foi mantido em português para preservar o contexto original do TCC.

---

## Como Executar Localmente

### Notebook em Python (opcional, acesso ao ERA5)

```bash
pip install -r requirements-python.txt
jupyter notebook "code/Acesso ERA5 API - Login Marcus.ipynb"
```

### App em R Shiny

```r
install.packages(scan("requirements-r.txt", what = "character", quiet = TRUE))
shiny::runApp("code")
```

Ou abra `code/app.R` no RStudio e clique em **Run App**.

---

## Dados e Privacidade

- Não versionar chaves/tokens de API no GitHub.
- Credenciais do ERA5 devem ficar apenas na configuração local da máquina.
- A estrutura está preparada para publicação pública no portfólio.

---

## Citação

FREIRE JUNIOR, Marcus Vinicius; SANTOS, Shirley Nunes Costa. *Aplicação Web em R para Estudo do Potencial Eólico Offshore nas Plataformas em Descomissionamento da Bacia de Campos*. Trabalho de Conclusão de Curso (Especialização em Gestão de Projetos e Negócios em TI) - Instituto Federal do Rio de Janeiro, 2024.

---

Voltar ao portfólio: [data-science-portfolio](../README.md)

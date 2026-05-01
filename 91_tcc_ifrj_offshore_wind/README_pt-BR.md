# Análise do Potencial Eólico Offshore - Aplicação Web em R Shiny (Bacia de Campos)

> English version: [README.md](README.md)  
> **TCC de Especialização - IFRJ (Gestão de Projetos e Negócios em TI, 2024)**  
> Parte de [data-science-portfolio](../README.md) - seção de trabalhos acadêmicos anteriores.

Este projeto avalia o potencial eólico offshore em plataformas descomissionadas na Bacia de Campos e apresenta os resultados por meio de uma aplicação web interativa em R Shiny.

- **Autores:** Marcus Vinicius Freire Junior; Shirley Nunes Costa Santos  
- **Orientador:** Ricardo Esteves Kneipp  
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
│   ├── era5_data_access_offshore_wind.ipynb   # Acesso, pré-processamento e validação ERA5
│   └── app.R                                  # Aplicação final em R Shiny
├── data/
│   ├── download_3anos.nc                      # Componentes de vento ERA5 processados, 2021-2023
│   └── inmet_2023_sao_tome_campos.csv         # Dados da estação INMET São Tomé, 2023
├── requirements-python.txt                    # Dependências Python (notebook)
├── requirements-r.txt                         # Dependências R (app Shiny)
├── README.md
└── README_pt-BR.md
```

> Observação: o NetCDF processado e compacto usado pela aplicação foi incluído para reprodutibilidade. Grandes arquivos brutos de download não devem ser versionados.

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
5. **Validação:** comparação com observações mensais de vento disponíveis da estação INMET São Tomé.
6. **Deploy:** aplicação interativa com mapas e comparações para stakeholders.

---

## Aquisição dos Dados

### Dados de Reanálise ERA5

Os dados de vento do ERA5 foram obtidos pelo Copernicus Climate Data Store usando o cliente Python `cdsapi`. A requisição utilizou médias mensais em nível de pressão, componentes de vento `u` e `v`, nível de pressão `900 hPa`, período de 2021 a 2023 e uma área geográfica que cobre a Bacia de Campos.

O fluxo de extração está documentado em:

```text
code/era5_data_access_offshore_wind.ipynb
```

Para reproduzir a extração, crie uma conta no Copernicus CDS, instale o `cdsapi` e configure suas credenciais localmente seguindo as instruções oficiais da API do CDS. Não versione `.cdsapirc`, chaves de API, tokens ou dados pessoais de login no repositório.

O arquivo ERA5 processado usado pela aplicação Shiny é:

```text
data/download_3anos.nc
```

### Dados INMET da Estação São Tomé

Os dados observados de vento foram obtidos no portal oficial de dados de estações do INMET para a estação `A620 - Campos dos Goytacazes - São Tomé`. O arquivo incluído neste projeto contém observações mensais de vento de 2023 e é usado como fonte externa de comparação para a análise baseada no ERA5.

```text
data/inmet_2023_sao_tome_campos.csv
```

---

## Visões da Aplicação

A aplicação (`code/app.R`) inclui:

- Mapa da Bacia e localização das plataformas.
- Velocidade média do vento ao longo do tempo.
- Boxplots sazonais de velocidade.
- Mapas de velocidade e direção do vento.
- Ranking das plataformas por potencial eólico estimado.


---

## Resumo dos Resultados

A análise indicou padrões consistentes de vento offshore na Bacia de Campos entre 2021 e 2023, com algumas plataformas em descomissionamento apresentando potencial eólico teórico relevante de acordo com as premissas adotadas no estudo.

Os maiores potenciais estimados por plataforma foram observados para a PETROBRAS 26 (P-26) e a PETROBRAS XIX, ambas acima de 85.000 W no cálculo simplificado de potência eólica. A PETROBRAS XXXIII e a NAMORADO 2 (PNA-2) também apresentaram potencial relevante.

Esses resultados devem ser interpretados como uma estimativa técnica exploratória, e não como um estudo final de viabilidade de engenharia ou financeira. Uma avaliação completa exigiria curvas de potência específicas de aerogeradores, batimetria, conexão à rede, avaliação estrutural, licenciamento ambiental e modelagem econômica.

---

## Como Executar Localmente

### Notebook em Python (opcional, acesso ao ERA5)

```bash
pip install -r requirements-python.txt
jupyter notebook "code/era5_data_access_offshore_wind.ipynb"
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
- O notebook e o README usam instruções genéricas de acesso aos dados e não incluem dados pessoais de login.
- A estrutura está preparada para publicação pública no portfólio.

---

## Citação

FREIRE JUNIOR, Marcus Vinicius; SANTOS, Shirley Nunes Costa. *Aplicação Web em R para Estudo do Potencial Eólico Offshore nas Plataformas em Descomissionamento da Bacia de Campos*. Trabalho de Conclusão de Curso (Especialização em Gestão de Projetos e Negócios em TI) - Instituto Federal do Rio de Janeiro, 2024.

---

Voltar ao portfólio: [data-science-portfolio](../README.md)

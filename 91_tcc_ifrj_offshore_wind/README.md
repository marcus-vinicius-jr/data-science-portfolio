# Offshore Wind Potential Analysis - R Shiny Web Application (Campos Basin)

> Portuguese version: [README_pt-BR.md](README_pt-BR.md)  
> **Specialization Capstone - IFRJ (IT Project & Business Management in IT, 2024)**  
> Part of [data-science-portfolio](../README.md) - Previous Academic Work section.

This project evaluates the offshore wind potential of decommissioned oil platforms in Brazil's Campos Basin and delivers the analysis through an interactive R Shiny web application.

- **Author:** Marcus Vinicius Freire Junior  
- **Advisor:** Shirley Nunes Costa Santos  
- **Program:** Specialization in IT Project & Business Management - IFRJ  
- **Year:** 2024

---

## Live Application

- **Shiny App (deployed):** https://fboewn-marcus-vinicus.shinyapps.io/Myapp/

---

## Repository Structure

```text
91_tcc_ifrj_offshore_wind/
├── code/
│   ├── Acesso ERA5 API - Login Marcus.ipynb   # ERA5 data access and preprocessing (Python)
│   └── app.R                                  # Final R Shiny application
├── data/                                      # Optional local data artifacts
├── requirements-python.txt                    # Python dependencies (notebook)
├── requirements-r.txt                         # R dependencies (Shiny app)
├── README.md
└── README_pt-BR.md
```

> Note: Large NetCDF files are not versioned in the repository.

---

## Problem and Objectives

The project investigates whether offshore wind can be a viable opportunity in the Campos Basin by reusing decommissioned infrastructure.

Main objectives:

1. Estimate wind speed behavior and wind power potential in selected offshore points.
2. Compare platforms and identify high-potential locations.
3. Provide a practical visualization layer for decision support via a deployed Shiny app.

---

## Methodology (CRISP-DM Oriented)

1. **Data acquisition (ERA5):** retrieval of wind components (`u`, `v`) via API.
2. **Data processing:** calculation of wind speed and direction for platform coordinates.
3. **Spatiotemporal analysis:** maps, seasonal behavior, and platform-level comparisons.
4. **Power potential estimate:** nominal potential based on standard assumptions (`rho`, `R`, `A`, `eta`).
5. **Deployment:** interactive app with maps and comparative views for stakeholders.

---

## Application Views

The app (`code/app.R`) includes:

- Basin and platform location maps.
- Mean wind speed over time.
- Seasonal boxplots of wind speed.
- Wind speed spatial maps and wind direction maps.
- Platform ranking by estimated wind power potential.

> UI content remains in Portuguese to match the original capstone audience.

---

## How to Run Locally

### Python notebook (optional, ERA5 access)

```bash
pip install -r requirements-python.txt
jupyter notebook "code/Acesso ERA5 API - Login Marcus.ipynb"
```

### R Shiny app

```r
install.packages(scan("requirements-r.txt", what = "character", quiet = TRUE))
shiny::runApp("code")
```

Or open `code/app.R` in RStudio and click **Run App**.

---

## Data and Privacy Notes

- No private API keys should be committed.
- ERA5 credentials must stay in the local machine configuration only.
- The repository is prepared for public portfolio publication.

---

## Citation

FREIRE JUNIOR, Marcus Vinicius; SANTOS, Shirley Nunes Costa. *Aplicação Web em R para Estudo do Potencial Eólico Offshore nas Plataformas em Descomissionamento da Bacia de Campos*. Trabalho de Conclusão de Curso (Especialização em Gestão de Projetos e Negócios em TI) - Instituto Federal do Rio de Janeiro, 2024.

---

Back to portfolio: [data-science-portfolio](../README.md)

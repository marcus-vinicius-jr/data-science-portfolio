# Offshore Wind Potential Analysis - R Shiny Web Application (Campos Basin)

> Portuguese version: [README_pt-BR.md](README_pt-BR.md)  
> **Specialization Capstone - IFRJ (IT Project & Business Management in IT, 2024)**  
> Part of [data-science-portfolio](../README.md) - Previous Academic Work section.

This project evaluates the offshore wind potential of decommissioned oil platforms in Brazil's Campos Basin and delivers the analysis through an interactive R Shiny web application.

- **Authors:** Marcus Vinicius Freire Junior; Shirley Nunes Costa Santos  
- **Advisor:** Ricardo Esteves Kneipp  
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
│   ├── era5_data_access_offshore_wind.ipynb   # ERA5 data access, preprocessing and validation
│   └── app.R                                  # Final R Shiny application
├── data/
│   ├── download_3anos.nc                      # Processed ERA5 wind components, 2021-2023
│   └── inmet_2023_sao_tome_campos.csv         # INMET Sao Tome station data, 2023
├── requirements-python.txt                    # Python dependencies (notebook)
├── requirements-r.txt                         # R dependencies (Shiny app)
├── README.md
└── README_pt-BR.md
```

> Note: the compact processed NetCDF used by the app is included for reproducibility. Large raw downloads should not be versioned.

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
5. **Validation:** comparison with available monthly wind observations from the INMET Sao Tome station.
6. **Deployment:** interactive app with maps and comparative views for stakeholders.

---

## Data Acquisition

### ERA5 Reanalysis Data

ERA5 wind data were obtained from the Copernicus Climate Data Store using the Python `cdsapi` client. The request used pressure-level monthly means, the `u` and `v` wind components, pressure level `900 hPa`, the 2021-2023 period, and a geographic bounding box covering the Campos Basin.

The extraction workflow is documented in:

```text
code/era5_data_access_offshore_wind.ipynb
```

To reproduce the extraction, create a Copernicus CDS account, install `cdsapi`, and configure your credentials locally according to the official CDS API instructions. Do not commit `.cdsapirc`, API keys, tokens, or personal login data to the repository.

The processed ERA5 file used by the Shiny app is:

```text
data/download_3anos.nc
```

### INMET Sao Tome Station Data

Observed wind data were obtained from the official INMET station data portal for station `A620 - Campos dos Goytacazes - Sao Tome`. The file included in this project contains monthly wind observations for 2023 and is used as an external comparison source for the ERA5-based analysis.

```text
data/inmet_2023_sao_tome_campos.csv
```

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

## Results Summary

The analysis indicated consistent offshore wind patterns in the Campos Basin during 2021-2023, with selected decommissioning platforms showing relevant theoretical wind-power potential under the assumptions used in the study.

The highest estimated platform-level potentials were observed for PETROBRAS 26 (P-26) and PETROBRAS XIX, both above 85,000 W in the simplified turbine-power calculation. PETROBRAS XXXIII and NAMORADO 2 (PNA-2) also showed relevant potential.

These results should be interpreted as an exploratory technical estimate, not as a final engineering or financial feasibility study. A complete feasibility assessment would require turbine-specific power curves, bathymetry, grid connection analysis, structural evaluation, environmental licensing, and economic modeling.

---

## How to Run Locally

### Python notebook (optional, ERA5 access)

```bash
pip install -r requirements-python.txt
jupyter notebook "code/era5_data_access_offshore_wind.ipynb"
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
- The notebook and README use generic data-access instructions and do not include personal login data.
- The repository is prepared for public portfolio publication.

---

## Citation

FREIRE JUNIOR, Marcus Vinicius; SANTOS, Shirley Nunes Costa. *Aplicação Web em R para Estudo do Potencial Eólico Offshore nas Plataformas em Descomissionamento da Bacia de Campos*. Trabalho de Conclusão de Curso (Especialização em Gestão de Projetos e Negócios em TI) - Instituto Federal do Rio de Janeiro, 2024.

---

Back to portfolio: [data-science-portfolio](../README.md)

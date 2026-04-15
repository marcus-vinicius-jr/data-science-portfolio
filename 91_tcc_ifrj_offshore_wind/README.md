# Offshore Wind Potential Analysis — R Shiny Web Application (Campos Basin)

> **Specialization Capstone — IFRJ (IT Project & Business Management in IT, 2024)**  
> Part of [data-science-portfolio](../README.md) — Previous Academic Work section.

This project evaluates the **offshore wind energy potential** of nine decommissioned oil
platforms in Brazil's Campos Basin and exposes the results through an interactive **R Shiny**
web application. It combines Python for **data acquisition and preprocessing** (ERA5 climate
reanalysis) and R for **analysis, visualization and web deployment**, following a **CRISP‑DM**
methodology.

- **Author:** Marcus Vinicius Freire Junior  
- **Advisor:** Shirley Nunes Costa Santos  
- **Program:** Specialization in IT Project & Business Management — IFRJ  
- **Year:** 2024

---

## Repository Structure

```text
91_tcc_ifrj_offshore_wind/
├── python/
│   └── Acesso_ERA5_API.ipynb      # ERA5 data access and preprocessing (Python)
├── r/
│   └── versao_final_publicacao.R  # Final R Shiny application script
├── data/                          # (optional) processed data used by the app
├── figures/                       # (optional) exported plots / maps
└── README.md
```

> Note: Raw ERA5 NetCDF files are large and may not be stored in this repository.
> The notebook documents how they were obtained via the official API.

---

## Problem & Objectives

Brazil is expanding its renewable energy portfolio, and offshore wind has strong potential,
especially in regions with existing infrastructure. The Campos Basin contains several
decommissioned oil platforms that could be reused as bases for offshore wind turbines.

**Main objectives:**

1. Quantify the **offshore wind potential** at selected platforms in the Campos Basin.  
2. Build an **interactive web application** to:
   - visualize wind speed and direction patterns over time,
   - compare platforms in terms of estimated power potential,
   - support decision-making on the reuse of decommissioned structures.  
3. Follow a **data mining lifecycle (CRISP‑DM)**, from business understanding to deployment.

---

## Methodology

### Data Acquisition & Preprocessing (Python)

- **Source:** ERA5 climate reanalysis datasets (wind components u/v at 10 m or 100 m).  
- **Tools:** `cdsapi`, `xarray`, `numpy`, `pandas`.  
- **Steps:**
  - Request ERA5 data for a **spatial window** covering Campos Basin.
  - Extract **u (east–west)** and **v (north–south)** wind components at the locations of nine platforms.
  - Compute **wind speed** and **direction**:
    - Speed: `v = sqrt(u² + v²)`
    - Direction: `θ = arctan2(u, v)` (converted to degrees and compass directions)
  - Aggregate by **hour / day / season** to support temporal and seasonal analysis.
  - Export processed data (CSV/RDS) for use by the R Shiny app.

### Modelling & Analysis (R)

- **Tools:** `shiny`, `ggplot2`, `ncdf4`, `dplyr`, `viridis`, `maps`, `grid`.  
- **Key analyses:**
  - **Time-series** of wind speed at each platform (e.g. 2021–2023).  
  - **Seasonal behaviour**: boxplots and summaries by season (summer, autumn, winter, spring).  
  - **Spatial distribution**: mean wind speed maps over the study area.  
  - **Wind direction fields**: vector maps showing predominant directions.  
  - **Energy potential**:
    - air density: `ρ = 1.225 kg/m³`,
    - rotor radius: `R = 50 m` (example),
    - swept area: `A = πR²`,
    - efficiency factor: `η ≈ 0.4`,
    - estimated power: `P = 0.5 * ρ * A * η * v³`.

### Validation

- Comparison of ERA5-derived statistics with measurements from a nearby **INMET meteorological station**
  (e.g. São Tomé), checking the plausibility of wind speeds and distributions.

---

## R Shiny Application

The web application (script `r/versao_final_publicacao.R`) provides several interactive views:

1. **Study Area Map**  
   - Base map of the Campos Basin.  
   - Platform locations plotted with labels.

2. **Wind Speed Time Series**  
   - Line charts of wind speed by platform over time.  
   - Options to filter by period (year, month).

3. **Seasonal Analysis**  
   - Boxplots of wind speed by season for each platform.  
   - Comparison of seasonal variability between platforms.

4. **Spatial Wind Speed Map**  
   - Raster map of mean wind speed over the region.  
   - Platforms plotted on top of the raster.

5. **Wind Direction Vector Field**  
   - Arrows representing wind direction and relative magnitude over the study area.

6. **Estimated Power Potential**  
   - Bar charts or tables showing estimated nominal power per platform.  
   - Ranking of platforms by potential.

---

## Key Findings

- Platforms **PETROBRAS 26** and **PETROBRAS XIX** exhibit the **highest wind energy potential**,
  with estimated nominal power above 85,000 W under the assumed turbine parameters.
- Offshore wind speeds in the Campos Basin are **consistent and favourable**, often exceeding
  typical thresholds used for onshore wind farms.
- Reusing **decommissioned oil platforms** as bases for wind turbines can significantly reduce
  installation and infrastructure costs, supporting Brazil's energy transition strategy.
- The methodology (ERA5 + Python + R Shiny + CRISP‑DM) is reusable for other offshore regions
  and can be extended with economic feasibility analyses.

---

## How to Run

### 1. Python — ERA5 Data Access (optional)

If you want to reproduce the data extraction:

1. Create and activate a Python environment.
2. Install dependencies (adjust as needed in your environment):

   ```bash
   pip install cdsapi xarray numpy pandas
   ```

3. Open and run the notebook:

   ```bash
   jupyter notebook python/Acesso_ERA5_API.ipynb
   ```

4. Ensure the processed data files are exported to the `data/` folder in a format expected by the R script.

### 2. R — Shiny Application

1. Install R and RStudio (optional but recommended).  
2. Install required packages inside R:

   ```r
   install.packages(c(
     "shiny", "ggplot2", "ncdf4", "dplyr",
     "viridis", "maps", "grid"
   ))
   ```

3. Run the application:

   ```r
   shiny::runApp("r")
   ```

   or open `r/versao_final_publicacao.R` in RStudio and click "Run App".

---

## Citation

FREIRE JUNIOR, Marcus Vinicius; SANTOS, Shirley Nunes Costa. Aplicação Web em R para Estudo do Potencial Eólico Offshore nas Plataformas em Descomissionamento da Bacia de Campos. Trabalho de Conclusão de Curso (Especialização em Gestão de Projetos e Negócios em TI) — Instituto Federal do Rio de Janeiro, 2024.

---

> Back to portfolio: [data-science-portfolio](../README.md)

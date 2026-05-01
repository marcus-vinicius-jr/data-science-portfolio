# PACKAGES
library(shiny)
library(shinythemes)
library(ggplot2)
library(ncdf4)
library(viridis)
library(maps)
library(grid)

# netCDF file processing
file_candidates <- c(
  file.path("..", "data", "download_3anos.nc"),
  file.path("data", "download_3anos.nc"),
  "download.nc"
)
file_path <- file_candidates[file.exists(file_candidates)][1]
if (!file.exists(file_path)) {
  stop("O arquivo não foi encontrado no caminho especificado.")
}

process_nc_data <- function(file_path) {
  
  nc_data <- nc_open(file_path)
  u <- ncvar_get(nc_data, "u")
  v <- ncvar_get(nc_data, "v")
  time <- ncvar_get(nc_data, "time")
  
  # NetCDF dimensions: time, latitude, longitude
  wspd <- sqrt(u^2 + v^2)
  wspd_mean <- apply(wspd, 1, mean, na.rm = TRUE)
  time_posix <- as.POSIXct(time * 3600, origin = "1900-01-01", tz = "UTC")
  
  wind_data <- data.frame(
    time = time_posix,
    wind_speed = wspd_mean
  )
  
  nc_close(nc_data)
  
  return(wind_data)
}

# PLATFORMS
platforms <- list(
  'NAMORADO 2 (PNA-2)' = c(-22.45073, -40.41175),
  'PETROBRAS 26 (P-26)' = c(-22.4684, -40.02869),
  'PETROBRAS 32 (P-32)' = c(-22.2051, -40.1431),
  'PETROBRAS 37 (P-37)' = c(-22.4868, -40.09779),
  'PETROBRAS IX' = c(-22.57358, -40.82192),
  'PETROBRAS XIX' = c(-22.3927, -40.05438),
  'PETROBRAS XXXIII' = c(-22.37, -40.0267),
  'VERMELHO 1 (PVM-1)' = c(-22.16065, -40.27872),
  'VERMELHO 2 (PVM-2)' = c(-22.17535, -40.29147)
)


# CAMPOS BASIN LOCATION FUNCTION
plot_bacia_de_campos_map <- function() {
  world_map <- map_data("world")
  
  lon <- c(-42.5, -40)
  lat <- c(-23.5, -21.5)
  
  bacia_de_campos <- data.frame(
    long = c(lon[1], lon[2], lon[2], lon[1]),
    lat = c(lat[1], lat[1], lat[2], lat[2])
  )
  
  p <- ggplot() +
    geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "black") +
    geom_polygon(data = bacia_de_campos, aes(x = long, y = lat), fill = NA, color = "red", size = 1.5) +
    labs(
      title = "Região da Bacia de Campos",
      x = "Longitude",
      y = "Latitude"
    ) +
    coord_cartesian(xlim = c(-75, -30), ylim = c(-35, 10)) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16)
    )
  
  return(p)
}


# AVERAGE WIND SPEED BY MONTH FUNCTION
plot_wind_mean_graph <- function() {
  wind_data <- process_nc_data(file_path)
  
  ggplot(wind_data, aes(x = time, y = wind_speed)) +
    geom_line(color = "blue") +
    geom_point(color = "blue", size = 2) +
    scale_x_datetime(date_labels = "%b %Y", date_breaks = "1 month") +
    labs(
      #title = "Average Wind Speed 2021 - 2023)",
      x = "Tempo",
      y = "Velocidade do Vento (m/s)"
    ) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}



# BOXPLOT FUNCTION BY SEASON
plot_wind_outliers <- function() {
  wind_data <- process_nc_data(file_path)
  wind_data$season <- factor(format(wind_data$time, "%m"), levels = c("12", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"), 
                             labels = c("Verão", "Verão", "Verão", "Outono", "Outono", "Outono", "Inverno", "Inverno", "Inverno", "Primavera", "Primavera", "Primavera"))
  
  ggplot(wind_data, aes(x = season, y = wind_speed, color = season)) +
    geom_boxplot() +
    labs(
      #title = "Boxplot of Average Wind Intensity by Season",
      x = "Estação do Ano",
      y = "Velocidade Média do Vento (m/s)"
    ) +
    scale_fill_viridis(discrete = TRUE) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16),
      legend.position = "none"
    )
}

# PLATFORM LOCATION AND REGIONAL AVERAGE WIND SPEED
# Function to calculate wind speed at each platform
calculate_wind_speed_for_platforms <- function(file_path, platforms) {
  
  nc_data <- nc_open(file_path)
  u <- ncvar_get(nc_data, "u")
  v <- ncvar_get(nc_data, "v")
  lon <- ncvar_get(nc_data, "longitude")
  lat <- ncvar_get(nc_data, "latitude")
  
  wind_speeds <- sapply(platforms, function(coords) {
    plat_lat <- coords[1]
    plat_lon <- coords[2]
    
    closest_lat_idx <- which.min(abs(lat - plat_lat))
    closest_lon_idx <- which.min(abs(lon - plat_lon))
    
    # NetCDF dimensions: time, latitude, longitude
    u_values <- u[, closest_lat_idx, closest_lon_idx]
    v_values <- v[, closest_lat_idx, closest_lon_idx]
    
    wspd_values <- sqrt(u_values^2 + v_values^2)
    mean_wspd <- mean(wspd_values)
    
    return(mean_wspd)
  })
  
  nc_close(nc_data)
  
  wind_speeds
}

# Compute wind speed for each platform (function call)
platform_wind_speeds <- calculate_wind_speed_for_platforms(file_path, platforms)

# Platform location plot with wind speed in the legend
plot_platforms_map <- function(platform_wind_speeds) {
  world_map <- map_data("world")
  
  platforms_df <- data.frame(
    platform = names(platforms),
    lon = sapply(platforms, "[", 2),
    lat = sapply(platforms, "[", 1),
    wind_speed = platform_wind_speeds,
    color = rainbow(length(platforms))
  )
  
  platforms_df$label <- paste(platforms_df$platform, sprintf(" - %.2f m/s", platforms_df$wind_speed))
  
  p <- ggplot() +
    geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "black") +
    geom_point(data = platforms_df, aes(x = lon, y = lat, color = platform), size = 3) +
    scale_color_manual(values = platforms_df$color, labels = platforms_df$label) +
    labs(
      #title = "Location of Oil and Gas Platforms in Campos Basin",
      x = "Longitude",
      y = "Latitude",
      color = "Plataformas - Velocidade Média do Vento"
    ) +
    coord_cartesian(xlim = c(-42.5, -40), ylim = c(-23.5, -21.5)) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16),
      legend.text = element_text(size = 10)
    )
  
  return(p)
}

# REGIONAL AVERAGE WIND SPEED WITH PLATFORMS (COLOR SCALE)
plot_wind_mean_map <- function(file_path) {
  
  nc_data <- nc_open(file_path)
  u <- ncvar_get(nc_data, "u")
  v <- ncvar_get(nc_data, "v")
  lon <- ncvar_get(nc_data, "longitude")
  lat <- ncvar_get(nc_data, "latitude")
  
  # NetCDF dimensions: time, latitude, longitude
  wspd <- sqrt(u^2 + v^2)
  wspd_mean <- apply(wspd, c(2, 3), mean, na.rm = TRUE)
  
  nc_close(nc_data)
  
  wind_map_data <- expand.grid(lat = lat, lon = lon)
  wind_map_data$wspd_mean <- as.vector(wspd_mean)
  
  platforms_df <- data.frame(
    platform = names(platforms),
    lon = sapply(platforms, "[", 2),
    lat = sapply(platforms, "[", 1)
  )
  
  world_map <- map_data("world")
  
  p <- ggplot() +
    geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "black") +
    geom_raster(data = wind_map_data, aes(x = lon, y = lat, fill = wspd_mean), alpha = 0.7) +
    scale_fill_viridis_c() +
    geom_point(data = platforms_df, aes(x = lon, y = lat), color = "red", size = 3) +
    coord_quickmap(xlim = c(-42.5, -40), ylim = c(-23.5, -21.5)) +
    labs(
      #title = "Average Wind Speed from 2021 to 2023",
      x = "Longitude",
      y = "Latitude",
      fill = "Velocidade Média do Vento (m/s)"
    ) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16)
    )
  
  return(p)
}


# WIND DIRECTION WITH PLATFORMS
plot_wind_mean_map_with_arrows <- function(file_path) {
  
  nc_data <- nc_open(file_path)
  u <- ncvar_get(nc_data, "u")
  v <- ncvar_get(nc_data, "v")
  lon <- ncvar_get(nc_data, "longitude")
  lat <- ncvar_get(nc_data, "latitude")
  
  # NetCDF dimensions: time, latitude, longitude
  wspd <- sqrt(u^2 + v^2)
  wspd_mean <- apply(wspd, c(2, 3), mean, na.rm = TRUE)
  
  nc_close(nc_data)
  
  wind_map_data <- expand.grid(lat = lat, lon = lon)
  wind_map_data$wspd_mean <- as.vector(wspd_mean)
  wind_map_data$u_mean <- as.vector(apply(u, c(2, 3), mean, na.rm = TRUE))
  wind_map_data$v_mean <- as.vector(apply(v, c(2, 3), mean, na.rm = TRUE))
  wind_map_data$potencial <- calcula_potencial(wind_map_data$wspd_mean)
  
  platforms_df <- data.frame(
    platform = names(platforms),
    lon = sapply(platforms, "[", 2),
    lat = sapply(platforms, "[", 1)
  )
  
  world_map <- map_data("world")
  
  p <- ggplot() +
    geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "black") +
    geom_raster(data = wind_map_data, aes(x = lon, y = lat, fill = wspd_mean), alpha = 0.7) +
    geom_segment(data = wind_map_data, aes(x = lon, y = lat, xend = lon + u_mean, yend = lat + v_mean),
                 arrow = arrow(length = unit(0.1, "cm")), color = "red", alpha = 0.7) +
    scale_fill_viridis_c() +
    geom_point(data = platforms_df, aes(x = lon, y = lat), color = "blue", size = 3) +
    coord_quickmap(xlim = c(-42.5, -40), ylim = c(-23.5, -21.5)) +
    labs(
      #title = "Average Wind Speed (m/s) and Wind Flow Direction from 2021 to 2023",
      x = "Longitude",
      y = "Latitude",
      fill = "Velocidade do Vento (m/s)"
    ) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16)
    )
  
  return(p)
}

# PLATFORM POWER POTENTIAL
# The nominal power of a wind turbine represents the maximum power it can generate under ideal wind conditions,
# measured in watts (W). It is not directly related to time, but to the maximum energy generation capacity
# under specific wind conditions.

# Function to calculate wind power potential
densidade_ar <- 1.225  # kg/m³ Nível do Mar
raio_rotor <- 50  # metros (para um aerogerador com diâmetro de 100 metros)
area_pa <- 3.14159 * (raio_rotor^2)  # m²
eficiencia_aerogerador <- 0.4  # 40%

calcula_potencial <- function(wspd_mean) {
  0.5 * densidade_ar * area_pa * (wspd_mean ^ 3) * eficiencia_aerogerador
}


# Function to plot the platform map with wind potential in the legend
plot_platforms_map_with_potential <- function() {
  world_map <- map_data("world")
  
  platform_wind_speed <- calculate_wind_speed_for_platforms(file_path, platforms)
  
  platforms_df <- data.frame(
    platform = names(platforms),
    lon = sapply(platforms, "[", 2),
    lat = sapply(platforms, "[", 1),
    potencial = calcula_potencial(platform_wind_speed),
    color = rainbow(length(platforms))
  )
  
  platforms_df$label <- paste(platforms_df$platform, sprintf(" - %.2f (W)", platforms_df$potencial))
  
  p <- ggplot() +
    geom_polygon(data = world_map, aes(x = long, y = lat, group = group), fill = "lightblue", color = "black") +
    geom_point(data = platforms_df, aes(x = lon, y = lat, color = platform), size = 3) +
    scale_color_manual(values = platforms_df$color, labels = platforms_df$label) +
    labs(
      #title = "Location of Oil and Gas Platforms in Campos Basin",
      #title = "air density = 1.225kg/m³, rotor radius = 50m, blade area = pi * (rotor radius)^2 m², and turbine efficiency = 40%",
      x = "Longitude",
      y = "Latitude",
      color = "Plataformas - Potencial Eólico"
    ) +
    coord_cartesian(xlim = c(-42.5, -40), ylim = c(-23.5, -21.5)) +
    theme_minimal() +
    theme(
      axis.text = element_text(size = 12),
      axis.title = element_text(size = 14),
      plot.title = element_text(size = 16),
      legend.text = element_text(size = 10)
    )
  
  return(p)
}

# Shiny layout
ui <- navbarPage(
  theme = shinytheme("superhero"),
  title = "Estudo da Velocidade do Vento e Potencial Eólico na Bacia de Campos",
  
  tabPanel("Página Inicial",
           fluidPage(
             tags$head(
               tags$style(HTML("
               p {
                 text-align: justify;
               }
             "))
             ),
             titlePanel("Bem-vindo ao Estudo da Velocidade do Vento e Potencial Eólico na Bacia de Campos"),
             mainPanel(
               p("Este aplicativo foi desenvolvido para visualizar a intensidade média do vento e o potencial eólico nas plataformas de petróleo e gás em descomissionamento na Bacia de Campos, com dados de 2021 a 2023. Utilizando componentes u e v do vento, calculamos a intensidade e disponibilizamos essas informações de forma interativa, permitindo que os usuários explorem os dados e compreendam as condições climáticas da região."),
               p("O estudo aqui apresentado é de grande importância para o setor de energia renovável no Brasil. Ele destaca o potencial de transformação das plataformas de petróleo desativadas em infraestruturas para a geração de energia eólica offshore. Isso possibilita a diversificação da matriz energética do país, reduzindo a dependência de fontes fósseis e contribuindo para um futuro mais sustentável."),
               p("Desenvolvido por Marcus Vinicius Freire Junior e Shirley Nunes Costa Santos, este aplicativo oferece uma ferramenta prática para analisar dados essenciais ao planejamento energético e ao estudo do potencial eólico na costa brasileira. Navegue e descubra os dados que podem apoiar a expansão das energias renováveis no Brasil.")
             )
           )
  )
  ,
 # SHINY TABS 
    tabPanel("Mapa da Bacia de Campos",
             plotOutput("baciaDeCamposMap")),
    
    tabPanel("Velocidade Média do Vento",
             fluidPage(
               titlePanel("Velocidade Média do Vento 2021-2023"),
               mainPanel(
                 plotOutput("windMeanGraph")
               )
             )),
    
    tabPanel("Boxplot da Velocidade Média do Vento por estação",
             fluidPage(
               titlePanel("Boxplot da Velocidade Média do Vento por estação 2021-2023"),
               mainPanel(
                 plotOutput("windOutliers")
               )
             )),
    
    tabPanel("Mapa de Localização das Plataformas",
             fluidPage(
               titlePanel("Localização das Plataformas e Velocidade Média do Vento 2021-2023"),
               mainPanel(
                 plotOutput("platformsMap")
               )
             )),
    
    tabPanel("Mapa da Média da Velocidade do Vento",
             fluidPage(
               titlePanel("Média da Velocidade do Vento 2021-2023"),
               mainPanel(
                 plotOutput("windMap")
               )
             )),
    
    tabPanel("Mapa da direção e velocidade média do Vento",
             fluidPage(
               titlePanel("Mapa da direção e velocidade média do Vento 2021-2023"),
               mainPanel(
                 plotOutput("windMeanMap")
               )
             )),
    tabPanel("Potencial Eólico nas Plataformas",
             fluidPage(
               titlePanel("Potencial Eólico nas Plataformas"),
               mainPanel("Densidade do ar = 1.225kg/m³; Raio do rotor = 50m; Área da pa = pi * (raio do rotor) ^2  m²;  Eficiencia do aerogerador = 40%",
                 plotOutput("platformsMapWithPotential")
               )
             )),
    
  )

server <- function(input, output) {
  output$windMeanGraph <- renderPlot({
    plot_wind_mean_graph()
  })
  
  output$platformsMap <- renderPlot({
    plot_platforms_map(platform_wind_speeds)
  })
  
  output$windMeanMap <- renderPlot({
    plot_wind_mean_map_with_arrows(file_path)
  })
  
  output$windMap <- renderPlot({
    plot_wind_mean_map(file_path)
  })
  
  output$platformsMapWithPotential <- renderPlot({
    plot_platforms_map_with_potential()
  })
  
  output$windOutliers <- renderPlot({
    plot_wind_outliers()
  })
  
  output$baciaDeCamposMap <- renderPlot({
    plot_bacia_de_campos_map()
  })
}

shinyApp(ui = ui, server = server)









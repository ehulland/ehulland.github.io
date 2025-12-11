# install.packages("leaflet")
# install.packages("htmlwidgets")

library(leaflet)
library(htmlwidgets)

places <- data.frame(
  name = c(
    "London, Canada",
    "Pittsburgh, PA, USA",
    "University Park, PA, USA",
    'Paris, France',
    "Atlanta, GA, USA",
    "Seattle, WA, USA",
    "Utrecht, Netherlands"
  ),
  role = c(
    "Born and raised (1989-2001)",
    "New chapter in Pittsburgh for middle and high school (2001-2007)",
    "Penn State University for undergrad (2007-2012)",
    "Study abroad in Paris (winter 2010)",
    "MPH studies at Emory University (2012-2014) and work at the CDC (2014-2018)",
    "PhD at UW and IHME (2018-2023) and remote postdoc (2023-2024)",
    "Big move overseas to Utrecht (2024) and a new postdoc (2025-present)"
  ),
  lat = c(42.9849, 40.4406, 40.7982, 48.858387, 33.7490, 47.6062, 52.0907),
  lng = c(-81.2453, -79.9959, -77.8599, 2.0180743,-84.3880, -122.3321, 5.1214)
)

m <- leaflet(places) |>
  addTiles() |>
  addCircleMarkers(
    lng = ~lng,
    lat = ~lat,
    label = ~name,
    popup = ~paste0("<strong>", name, "</strong><br>", role),
    radius = 6
  )

# Save as a self-contained HTML file in your repo folder
htmlwidgets::saveWidget(
  m,
  file = "about_map.html",
  selfcontained = TRUE
)
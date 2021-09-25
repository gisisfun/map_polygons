require(dplyr)
require(jsonlite)
require(foreign)
require(geosphere)
require(sp)
require(leaflet)

point_in_poly_join <- function(ref_data,gj_file,poly_names) {
  data_set <- data.frame()
  #ref_row <- 1
  for (ref_row in 1:length(ref_data)) { # length(ref_data)-
    poly_num_hit <- 0
    poly_list <- gj_file$geometries
    poly_count <- 0
    # check target in boundary set
    for (poly_num in 1:length(poly_list$coordinates)) {
      if (length(poly_list$coordinates[[poly_num]]) > 0) {
        poly_coords <- poly_list$coordinates[[poly_num]]
        poly_types <- poly_list$type
        if (poly_types[poly_num]=='MultiPolygon') {
          for (multi_poly in 1:length(poly_coords)) {
            # poly_count <- poly_count + 1
            poly_gon <- poly_coords[[multi_poly]]
            
            poly_x <- poly_gon[,,1]
            poly_y <- poly_gon[,,2]
            #print(areaPolygon(data.frame(poly_x,poly_y)))
            
            isin <- point.in.polygon(ref_data[ref_row,'target_x'],
                                     ref_data[ref_row,'target_y'],
                                     poly_x,poly_y) 
            
            if (isin == 1) {
              poly_num_hit <- poly_num
            }
            
          }
        } else {
          # poly_gon <- poly_coords
          poly_x <- poly_coords[,,1]
          poly_y <- poly_coords[,,2]
          isin <- point.in.polygon(ref_data[ref_row,'target_x'],
                                   ref_data[ref_row,'target_y'],
                                   poly_x,poly_y) 
          
          if (isin == 1) {
            poly_num_hit <- poly_num
          }
          
        }
        # if (poly_num_hit > 0) {
        #   output_row <- data.frame(ref_data[ref_row,],poly_names[poly_num_hit,])
        #   data_set <- rbind(data_set,output_row)
        # }
      }
      if (poly_num_hit > 0) {
        #print(data.frame(ref_data[ref_row,],poly_names[poly_num_hit,]))
        output_row <- data.frame(ref_data[ref_row,],poly_names[poly_num_hit,])
        poly_num_hit <- 0
        isin <- 0
        data_set <- rbind(data_set,output_row)
      }
    }
  }
  return(data_set)
}


make_shape <- function(gj_file,poly_names) {
  srs_list = list()
  
  crdref <- CRS('+proj=longlat +datum=WGS84')
  
  data_bits <-  data.frame(poly_names)
  
  poly_list <- gj_file$geometries
  for (poly_num in 1:length(poly_list$coordinates)) {
    if (length(poly_list$coordinates[[poly_num]]) > 0) {
      poly_coords <- poly_list$coordinates[[poly_num]]
      poly_types <- poly_list$type
      if (poly_types[poly_num]=='MultiPolygon') {
        x_list <- poly_coords[[1]][, , 1]
        y_list <- poly_coords[[1]][, , 2]
        for (multi_poly in 1:length(poly_coords)) {
          # poly_count <- poly_count + 1
          poly_gon <- poly_coords[[multi_poly]]
          
          poly_x <- poly_gon[,,1]
          poly_y <- poly_gon[,,2]
        }
        sr <- Polygon(coords=cbind(x_list,y_list))
        srs_list[[poly_num]] = 
          Polygons(list(sr), 
                   as.character(poly_num))
        
      } else {
        # poly_gon <- poly_coords
        poly_x <- poly_coords[,,1]
        poly_y <- poly_coords[,,2]
        sr <- Polygon(coords=cbind(poly_x,poly_y))
        srs_list[[poly_num]] = Polygons(list(sr), as.character(poly_num))
      }
    }
  }
  
  
  S4SP = SpatialPolygons(srs_list,1:length(poly_list$coordinates),crdref) 
  S4SPDF = SpatialPolygonsDataFrame(S4SP,data_bits,1:length(poly_list$coordinates))
  centroids <- coordinates(S4SPDF) %>% 
    data.frame() %>% 
    rename('cent_lon'=X1,
           'cent_lat'=X2)
  S4SPDF <- cbind(S4SPDF,centroids)
  return(S4SPDF)
}


make_map <- function(Data) {
  base_map <-  leaflet(Data) %>%
    addTiles() %>% 
    setView(133, -23, 4) #%>%            )  
  base_map
  
  # Create HTML labels for tooltip
  tooltip <- sprintf("name: <b>%s</b> <br> id <b>%s</b>"
                     ,Data$NRM_REGION
                     ,Data$NRM_ID
  ) %>% lapply(htmltools::HTML)
  
  # Display map
  map_with_tooltip <- base_map  %>%
    addPolygons(stroke = TRUE, 
                color = "black",
                fillColor = "white",
                weight="1", 
                smoothFactor = 0.3, 
                fillOpacity = 0.7, 
                #fillColor = ~colorbins(S4SPDF$colname), 
                highlight = highlightOptions(
                  weight = 5, 
                  fillColor = "grey", 
                  fillOpacity = 0.7, 
                  bringToFront = TRUE),
                label = tooltip
    ) 
  #map_with_tooltip
  
  map_with_labels <- map_with_tooltip %>%
    addLabelOnlyMarkers(
      lng = ~cent_lon, lat = ~cent_lat,
      label = ~NRM_REGION,
      labelOptions = labelOptions(noHide = T))
  map_with_labels
  ###########################
  ## SAVE OUTPUT HTML FILE ##
  ###########################
  # Save output as HTML widget (or incorporate into Shiny / Flexdashboard)
  #htmlwidgets::saveWidget(map_with_labels, file="output8.html")
}
# Use mapshaper website to convert shapefile to geojson format
gj_file <- jsonlite::fromJSON(txt='shape//NRM_regions_2020.geojson')
# read polygon tabular data from dbf filegeos
poly_names <- read.dbf('shape//NRM_regions_2020.dbf')

map_of_nrm <- make_shape(gj_file,poly_names)
make_map(map_of_nrm)
ref_data <- data.frame(ref=c('a','b','c'),
                       target_x = c(147.9709,145.5,133),
                       target_y = c(-36.6,-35.6,-23))

data_set <- point_in_poly_join(ref_data,gj_file,poly_names)


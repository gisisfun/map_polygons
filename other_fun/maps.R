require(dplyr)
require(jsonlite)
require(foreign)
require(geosphere)
require(sp)
require(leaflet)
require(ggplot2)
require(purrr)




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


longer_data <- function(gj_file,poly_names) {
  # turn MultPolygon coordinates into Polygon coordinates in geojson format
  raw_length<- map(gj_file$geometries$coordinates, function(x) {length(x)})
  status <- map(gj_file$geometries$type, function(x) {if (x=='MultiPolygon'){y <- 1} else {y <- 0}})
  mult_poly <- data.frame(length=unlist(raw_length),status=unlist(status))
  mult_poly [mult_poly $status==0,'length'] <- 1
  fred <- data.frame(poly_names,multi=mult_poly$length)

  new_df <- data.frame()
  for (row_n in 1:nrow(fred)) {
    for (rep_n in 1:fred[row_n,'multi']) {
      new_df <- rbind(new_df,fred[row_n,])
    }
  }
  return(new_df)
}

longer_shape <- function(gj_file) {
  srs_list = list()

  poly_ref <- 1
  poly_list <- gj_file$geometries
  for (poly_num in 1:length(poly_list$coordinates)) {
    if (length(poly_list$coordinates[[poly_num]]) > 0) {
      poly_coords <- poly_list$coordinates[[poly_num]]
      poly_types <- poly_list$type
      if (poly_types[poly_num]=='MultiPolygon') {

        for (multi_poly in 1:length(poly_coords)) {
          poly_gon <- poly_coords[[multi_poly]]

        
        srs_list[[poly_ref]] <- poly_gon
        poly_ref <- poly_ref + 1
        }
      } else {
        
        srs_list[[poly_ref]] <- poly_coords
        poly_ref <- poly_ref + 1
      }
    }
  }
  #list(type=rep('Polygon',poly_ref),geometries=list(coordinates=srs_list))
  return(list(type='Polygon',
              geometries=list(coordinates=srs_list,
                              type=rep('Polygon',(poly_ref-1)))))
} #longer_shape



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
  
  row.names(data_bits) <- seq(1:length(poly_list$coordinates))
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
  return(map_with_labels)
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
  return(map_with_labels)
}
# Use mapshaper.org website to convert shapefile (shp) to geojson format
gj_file <- jsonlite::fromJSON(txt='shape//NRM_regions_2020.geojson')
long_gj_file <- longer_shape(gj_file)

# read polygon tabular data from dbf file
poly_names <- read.dbf('shape//NRM_regions_2020.dbf')
long_poly_names <- longer_data(gj_file,poly_names)


map_of_nrm <- make_shape(gj_file,poly_names)
long_map_of_nrm <- make_shape(long_gj_file,long_poly_names)

make_map(map_of_nrm)
ref_data <- data.frame(ref=c('a','b','c'),
                       target_x = c(147.9709,145.5,133),
                       target_y = c(-36.6,-35.6,-23))

data_set <- point_in_poly_join(ref_data,gj_file,poly_names)


# leaflet(map_of_nrm) %>% 
#   addWMSTiles("https://data.gov.au/data/dataset/wa-state-boundary-geoscape-administrative-boundaries/resource/b3bb7d1a-ca1f-40d8-b529-95e7b83e5327/",
#               layers="51249941-02c0-43ff-9384-1613eb5246a1",
#               options = WMSTileOptions(format = "image/png", transparent = FALSE),
#               attribution = "")
# making maps

ref_data_sp <- SpatialPoints(cbind(ref_data['target_x'],ref_data['target_y']),crdref)
ref_data_spdf <- SpatialPointsDataFrame(ref_data_sp,ref_data)
points_df <- data.frame(name='Hobart',lon=147.3257,lat=-42.8826)
points_sp <- SpatialPoints(cbind(points_df['lon'],points_df['lat']),crdref)
points_spdf <- SpatialPointsDataFrame(points_sp,points_df)

north_nrm <- subset(long_map_of_nrm,NRM_REGION=='North NRM Region') 
tas <- subset(long_map_of_nrm,STATE=='TAS')

plot(tas,col = "red",
     main="North NRM Region",
     sub="Tasmania", 
     ylim=c(-43.5,-38),
     xlim=c(146,146.5))
plot(north_nrm, col = "green",add=TRUE)


crdref <- CRS('+proj=longlat +datum=WGS84')


plot(points_sp,col="black",add=TRUE,pch=21)
text(points_spdf,labels=points_spdf$name,pos=4,offset=0.5)

print("where is hobart")
print(over(points_spdf,long_map_of_nrm))


points_in_polygons <- long_map_of_nrm %over% 
  ref_data_spdf %>% 
  mutate(pol=row.names(.)) %>%
  select(ref,pol) %>%
  drop_na(ref) %>%
  mutate(name=long_poly_names[pol,'NRM_REGION'])





library(geojsonR)
library(maptools)
library(raster)
library(sp)
##https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt
URL <- "https://raw.githubusercontent.com/gisisfun/map_polygons/master/geojson/aus_hex_57km_layer.json"

basename(URL) # "abc.zip"
if(!file.exists(basename(URL))){
  # downloads to current directory:
  download.file(URL, basename(URL))
}

file_js = FROM_GeoJson(url_file_string = "aus_hex_57km_layer.json")
length(file_js$features)

#plot(pols, border='blue', col='yellow', lwd=3, add=TRUE)

srs_list = list()
crdref <- CRS('+proj=longlat +datum=WGS84')

for (i in 1:length(file_js$features)) {
  locality <- file_js$features[[i]]$properties$Locality
  p <- file_js$features[[i]]$properties$p
  data_bits <- data.frame("p" = p, "Locality" = locality)
  #print(data_bits)
  colnames(data_bits) <- c("p","locality")
  x <- file_js$features[[i]]$geometry$coordinates[,1]
  y <- file_js$features[[i]]$geometry$coordinates[,2]
  sr <- Polygon(cbind(x,y))
  ##pts <- SpatialPoints(lonlat)
  #pols <- spPolygons(lonlat)
  srs_list[[i]] = Polygons(list(sr), as.character(i))

    #points(pts, col='red', pch=20, cex=3)
}
SpP = SpatialPolygons(srs_list, 1:as.integer(length(file_js$features)),crdref)
plot(SpP, border='blue', col='yellow', lwd=1)
#Sr1 = Polygon(cbind(c(2,4,4,1,2),c(2,3,5,4,2)))
#Srs1 = Polygons(list(Sr1), "s1")


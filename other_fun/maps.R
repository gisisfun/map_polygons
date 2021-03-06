library(geojsonR)
library(sp)
#https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt  
#https://firms.modaps.eosdis.nasa.gov/web-services/
#https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-txt
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
data_bits <- "hello"
data_bits <- data.frame(p=integer(),locality=integer())

for (i in 1:length(file_js$features)) {
  l <- file_js$features[[i]]$properties$Locality
  p <- file_js$features[[i]]$properties$p
  data_bits[nrow(data_bits) + 1,] = list(p,l)
  #print(data_bits)
  #colnames(data_bits) <- c("p","locality")
  #data_bits <- file_js$features[[i]]$properties
  x <- file_js$features[[i]]$geometry$coordinates[,1]
  y <- file_js$features[[i]]$geometry$coordinates[,2]
  sr <- Polygon(cbind(x,y))
  ##pts <- SpatialPoints(lonlat)
  #pols <- spPolygons(lonlat)
  srs_list[[i]] = Polygons(list(sr), as.character(i))

    #points(pts, col='red', pch=20, cex=3)
}
S4SP = SpatialPolygons(srs_list,1:1264,crdref) 
S4SPDF = SpatialPolygonsDataFrame(S4SP,data_bits,1:1264)
#, plotOrder: 1:as.integer(length(file_js$features)),proj4string:crdref)
#S4pP = SpatialPolygons(srs_list, 1:as.integer(length(file_js$features)))

plot(S4SPDF, border='blue', col='yellow', lwd=1)
#Sr1 = Polygon(cbind(c(2,4,4,1,2),c(2,3,5,4,2)))
#Srs1 = Polygons(list(Sr1), "s1")


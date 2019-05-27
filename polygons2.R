  library('geosphere')
  #library('geojson')
  library('sp')
  #library('gdalUtils')
  #library('RSQLite')
  #library('rgdal')
  #library('csvread')

  new.point <- function(latlong,dist,angle) {   
    #c <- destPoint(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), b=angle, d=dist*1000, a=6378137, f=1/298.257223563)
    c <- geodesic(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), azi=angle, d=dist*1000, a=6378137, f=1/298.257223563)
    newlatlong <- c(c[1],c[2]) 
    #print(newlatlong)
    return(newlatlong)
  }
  
  points_in_polygon <- function (poly,ref_points,poly_points){
    poly_x <- poly_points[c(TRUE, FALSE)]
    poly_y <- poly_points[c(FALSE, TRUE)]
    p_count <- 0
    i <- 0
    for(row in 1:length(poly_points)) {
      i <- i + 1
      #cat(ref_points$lng[i],ref_points$lat[i],'\n')
      isin <- point.in.polygon(ref_points$lng[i],ref_points$lat[i],poly_x,poly_y) 
      p_count <- p_count + isin
      if (isin == 1) {cat(poly,',',ref_points$city[i],',',ref_points$admin_name[i],',',ref_points$lng[i],',',ref_points$lat[i],'\n')}
      #cat(i,'\n')
    }
    return(p_count)
  }
  
  dist.points <- function(latlong1,latlong2) {   
    dist <- distGeo(cbind(tail(latlong1[1], n=1),tail(latlong1[2], n=1)), cbind(tail(latlong2[1], n=1),tail(latlong2[2], n=1)), a=6378137, f=1/298.257223563)
    return(dist)
  }
  
  horizontal <- function(east,north,west,south,radial,hor_seq) {
    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
    angle <- 180
    new_north <-north
    cat(east,new_north,south,'\n')
    i <- 0
    latitudes <- vector()
    longitudes <- latitudes <- c(north)
    repeat {
      i <- i + 1
      if (i < 5) {i <- i} else {i <- 1}  
      
      latlong <- c(east,new_north)
      p <- new.point(latlong,radial*hor_seq[i],angle)
      
      new_north <- p[2]
      if (new_north <= south){break}
      latitudes <- c(latitudes,p[1])
      longitudes <- c(longitudes,p[2])
    }
    return(longitudes)
  }
  
  vertical <- function(east,north,west,south,radial,vert_seq) {
    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
    angle <- 90
    i <-0
    new_east <- east
    latitudes <- c(east)
    repeat 
    {  
      i <- i + 1
      if (i < 5) {i <- i} else {i <- 1}          
      latlong <- c(new_east,north)
      p <- new.point(latlong,radial*vert_seq[i],angle)
      
      new_east <- p[1]
      if (new_east >= west){ break}
      latitudes <- c(latitudes,p[1])    
    }
    return(latitudes)
  }
  
  
  MyData <- read.csv(file="csv/cities.csv", header=TRUE,colClasses=c("city"="character"), sep=",")
  attach(MyData)
  point_coords <- data.frame(population,city,lng,lat)
  detach(MyData)
  #point_coords
  
  makeHexagon <- function(poly_coords,bounds_e,bounds_n,bounds_s,bounds_w,est_area,centre_lat,centre_lon,hexagon,rowno,colname,colvalue) 
  { 
    templ_hexagon <-'{"geometry": {"coordinates": [[[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x1, y1]]], "type": "Polygon"}, "properties": {"E": be, "N": bn, "S": bs, "W": bw, "est_area": earea, "lat": latc, "lon": lonc, "p": polyn, "row": rown, "colname": colvalue}, "type": "Feature"}, '
    out_hexagon <- gsub("x1", poly_coords[1], templ_hexagon)
    out_hexagon <- gsub("x2", poly_coords[3], out_hexagon)   
    out_hexagon <- gsub("x3", poly_coords[5], out_hexagon) 
    out_hexagon <- gsub("x4", poly_coords[7], out_hexagon)
    out_hexagon <- gsub("x5", poly_coords[9], out_hexagon)    
    out_hexagon <- gsub("x6", poly_coords[11], out_hexagon)
    
    out_hexagon <- gsub("y1", poly_coords[2], out_hexagon)
    out_hexagon <- gsub("y2", poly_coords[4], out_hexagon)   
    out_hexagon <- gsub("y3", poly_coords[6], out_hexagon) 
    out_hexagon <- gsub("y4", poly_coords[8], out_hexagon)
    out_hexagon <- gsub("y5", poly_coords[10], out_hexagon)    
    out_hexagon <- gsub("y6", poly_coords[12], out_hexagon) 
    
    out_hexagon <- gsub("be", bounds_e, out_hexagon)
    out_hexagon <- gsub("bn", bounds_n, out_hexagon)   
    out_hexagon <- gsub("bs", bounds_s, out_hexagon) 
    out_hexagon <- gsub("bw", bounds_w, out_hexagon)
    out_hexagon <- gsub("earea", est_area, out_hexagon)    
    out_hexagon <- gsub("latc", centre_lat, out_hexagon)   
    out_hexagon <- gsub("lonc", centre_lon, out_hexagon)    
    out_hexagon <- gsub("polyn", hexagon, out_hexagon) 
    out_hexagon <- gsub("rown", rowno, out_hexagon) 
    out_hexagon <- gsub("colname", colname, out_hexagon) 
    out_hexagon <- gsub("colvalue", colvalue, out_hexagon) 
    
    return(out_hexagon)
  }
  
  is.even <- function(x) {return(!is.odd(x))}
  
  is.odd <- function(x) {return(intToBits(x)[1] == 1)}
  
  hexagons <- function(east,north,west,south,radial) {
    #
    # New Bit Start
    #
    stringsAsFactors = FALSE
    MyData <- read.csv(file="csv/cities.csv", header=TRUE,colClasses=c("city"="character", "admin_name"="character"), sep=",")
    #sapply(MyData, typeof)
    #attach(MyData)
    #point_coords <- data.frame(city,city_ascii,population,lng,lat)
    #detach(MyData)
    #point_coords$city_ascii
    #
    # New Bit End
    #
    #bbox <- c(113.338953078, -43.6345972634, 153.569469029, -10.6681857235)
    
    #east <- c(bbox[1]) #east
    #north <- c(bbox[4]) #north
    #dist <- 57
    #west <- bbox[3] #west
    #south <- bbox[2] #south
    cat('\nMaking hexagon shapes starting from ',north,',',east,' to ',south,',',west,' with a radial length of ',radial,' km\n')
    #init bits
    top_left <- 1 #R starts at 1 not 0 - yes
    lat_offset <- 4
    
    short_seg <- 0.7071
    long_seg <- 1
    gj_string <- ""
    odd_row <- TRUE
    even_row <- FALSE
    do_log <- FALSE
    hexagon <- 0
    
    #1/7 deriving horizontal list of reference points for longitude or (x axis or north to south) lines
    cat('\n1/7 deriving vertical list of reference points from north to south for longitudes or x axis\n')
    hor_seq =c(short_seg, short_seg, short_seg, short_seg)
    h_list <- horizontal(east,north,west,south,radial,hor_seq)
    len_h <- length(h_list)
    write.csv(h_list,'h_list8.csv')
    
    cat('\n2/7 deriving horizontal list of reference points from east to west for latitudes or y axis\n')
    vert_seq <- c(short_seg, long_seg, short_seg,long_seg) 
    v_list <- vertical(east,north,west,south,radial,vert_seq)
    len_v <- length(v_list)
    write.csv(v_list,'v_list8.csv')
    
    cat('\n3/7 deriving intersection point data between horizontal (latitude or east to west) and vertical (longitude or x axis or north to south) lines\n')
    intersect_df <- expand.grid(v_list,h_list)
    #print(class(intersect_df))
    colnames(intersect_df) <- c("latitude", "longitude")
    #write.csv(intersect_df,'intersect_df8.csv')
    intersect_len <- nrow(intersect_df)# intersect_df is a dataframe
    poly_est_count <- round((len_v*len_h)/length(hor_seq)+4,0)
    poly_row_count <- round((len_v/length(hor_seq)),0)
    #cat(poly_est_count,poly_row_count,'\n')
    
    last_lat_row <-0 
    inc_by_rem <- TRUE
    inc_adj <- 0
    rem_lat <- len_v%%(lat_offset+4)
    if (rem_lat == 2 | rem_lat == 5 | rem_lat == 6 | rem_lat == 7){
      inc_by_rem <- TRUE
      inc_adj <- -4}
    if (rem_lat == 1 | rem_lat == 3){
      inc_by_rem <- TRUE
      inc_adj <- 0}
    if (rem_lat == 0 | rem_lat == 4){
      inc_by_rem <- FALSE
      inc_adj <- 0}
    
    cat('\n4/7 deriving polygons from intersection points\n')
    rowno <- 1
    last_row <- 1
    
    len_val <- ((len_h)*(len_v-3))-(len_h*0.3)
    while (top_left < len_val)
    {     
      vertex <- c(1, 2, len_v+3, (len_v*2)+2, (len_v*2)+1, len_v+0)+top_left  
      poly_coords <- c(intersect_df[vertex[1], 1], intersect_df[vertex[1], 2], intersect_df[vertex[2], 1], 
  intersect_df[vertex[2], 2], intersect_df[vertex[3], 1], intersect_df[vertex[3], 2],intersect_df[vertex[4], 1], 
  intersect_df[vertex[4], 2], intersect_df[vertex[5], 1], intersect_df[vertex[5], 2],intersect_df[vertex[6], 1], 
  intersect_df[vertex[6], 2], intersect_df[vertex[1], 1], intersect_df[vertex[1], 2])
      
      poly_points <- matrix(poly_coords, ncol=2, byrow=TRUE)
      centre_lat <- poly_coords[2] + (poly_coords[12] - poly_coords[2])/2
      centre_lon <- poly_coords[1] + (poly_coords[11] - poly_coords[1])/2
      dist_check <- dist.points(intersect_df[vertex[1], ],intersect_df[vertex[2], ])
      
      #if ((centre_lat != last_lat_row) || (last_lat_row == 0))  #are we on the first or current row of polygons?
      #{
      bounds_n <- poly_coords[2] #intersect_df[vertex[0]][1]
      bounds_s <- poly_coords[6] #intersect_df[vertex[2]][1]
      bounds_e <- poly_coords[5] #intersect_df[vertex[2]][0]
      bounds_w <- poly_coords[11] #intersect_df[vertex[5]][0]
      last_lat_row <- centre_lat
      
      hexagon <- hexagon + 1
      #cat(hexagon,bounds_e,bounds_w,'\n')
      start <- c(poly_coords[2],poly_coords[1] )
      end <- c(poly_coords[4],poly_coords[3])
      est_area <- 0.945 * ((3 * sqrt(3))/2)*(radial^2) #estimate polygon area
      #
      # New Bit Start
      #
      
      ref_points <- subset(MyData, lat >= bounds_s & lat <= bounds_n & lng <= bounds_e & lng >= bounds_w)
      #ref_points <- na.omit(points_df)
      p_count <- points_in_polygon(hexagon,ref_points,poly_coords)
      
      #
      # New Bit End
      #
      
      geopoly <- makeHexagon(poly_coords,bounds_e,bounds_n,bounds_s,bounds_w,est_area,centre_lat,centre_lon,hexagon,rowno,'test',p_count)
      
      #if ((poly_coords[1] > poly_coords[11])) 
      if (bounds_e > bounds_w) 
      {
        #print(top_left)
        gj_string <- paste(gj_string, geopoly,"")                    
      }             
      #}#end last centre lat check if statement 
      
      #last_centre_lat <- centre_lat
      
      last_row <- rowno
      last_lat_row <- centre_lat
      rowno <- round(0.51+(hexagon/(poly_row_count)),0)
      top_left <- top_left + lat_offset
      
      if (rowno != last_row && rowno != 1)
      {
        top_left <- top_left + inc_adj 
        if (inc_by_rem == TRUE) {top_left <-  top_left + rem_lat}
        if (rowno %% 2 == 0) 
        {
          top_left <-  top_left + 2
          even_row <- TRUE
          odd_row <- FALSE
        }#for even row
        else 
        {
          top_left <-  top_left - 2
          even_row <- FALSE
          odd_row <- TRUE
        }#for odd row  
      }
      
    }#end while loop
    cat('\n5/7 geojson dataset of',hexagon,' derived hexagon polygons')
    gj_prefix <- '{"features": ['
    gj_suffix <- '], "type": "FeatureCollection"}'
    gj_string <- paste(gj_prefix, substr(gj_string,1,nchar(gj_string)-3),"")
    gj_string <- paste(gj_string, gj_suffix,"")
    
    print('the end')
    return(gj_string)
  }#end function hexagon

  otherbits <- function()
  {
    poly_points <- matrix(poly_coords, ncol=2, byrow=TRUE)
    poly_x <- poly_coords[c(TRUE, FALSE)]
    poly_y <- poly_coords[c(FALSE, TRUE)]
    isok <- point.in.polygon(cent[1],cent[2],poly_x,poly_y)
    
    
    #area in square km
    print(areaPolygon(poly_points))
    
    print(centroid(poly_points))
    cent <- centroid(poly_points)
    
    print(perimeter(poly_points))
    print(isok) #1 result is ok
    rem_lat <- len_v+1%%(lat_offset+4)
    print(rem_lat)
    
    cat('\npoly_x is:',poly_x,'\n')
    cat('\npoly_y is:',poly_y,'\n')
    
    cat('\ncentroid is of hexagon is:',centroid(poly_points),'\n')
    cat('\nperimeter is of hexagon is:',perimeter(poly_points),'\n')
    
    p = Polygon(poly_points)
    ps = Polygons(list(p),1)
    sps = SpatialPolygons(list(ps))
    plot(sps)
    
    #print(class(poly_points))
    ##matrix to dataframe
    #poly_points_df <- data.frame(x = poly_x, y = poly_y)
    #print(class(poly_points_df))
    #sp1 <- SpatialPoints(coords = poly_points_df)
    #sp1 <- Polygon(cbind(poly_x,poly_y))
    #print(class(sp1))
    #sps1 <- Polygons(list(sp1),"1")
    #print(class(sp1))
    #dfr <- data.frame(id = "1", use = "road", cars_per_hour = 10) # note how we use the ID from above!
    #sp_lns_dfr <- SpatialPolygonsDataFrame(sps1, dfr, match.ID = "id")
    #str(sp_lns_dfr)
  }
  
  #MyData <- read.csv(file="/home/pi/Downloads/map_polygons-master/csv/cities.csv", header=TRUE, sep=",")
  #attach(MyData)
  #point_coords <- data.frame(city,lng,lat)
  #detach(MyData)
  #point_coords
  
  output <- hexagons(96,  -8,168,  -45,34)
#point_coords

fileConn<-file('output8.json')
writeLines(output, fileConn)
close(fileConn)
#convert and reproject
#ogr2ogr(src_datasource_name='output8.json',f='ESRI Shapefile',dst_datasource_name='output8.shp',t_srs="EPSG:4283",verbose=TRUE)
#run query
#ogr2ogr(src_datasource_name='all.vrt',dialect='sqlite',sql='select * from shapes',dst_datasource_name='output8_q1.csv',verbose=TRUE)

#ogr2ogr(src_datasource_name='all.vrt',dialect='sqlite',sql='select * from fred',dst_datasource_name='output8_q2.csv',verbose=TRUE)

#ogr2ogr(src_datasource_name='output8.shp',t_srs="EPSG:4283",dst_datasource_name='output8_q2.csv',layer='track+points',verbose=TRUE)

#ogr2ogr -F "SQLite" -t_srs '+proj=utm +zone=10 +datum=NAD83' trip1_track_points.db trip1.gpx track_points
#dbfile="Path/To/field.sqlite"

#sqlite=dbDriver("SQLite")
#con=dbConnect(sqlite,dbfile, loadable.extensions=TRUE )

#vectorImport <- readOGR(dsn="NUTS_BN_03M_2013.sqlite", layer="nuts_bn_03m_2013")
#myShapeInR<-readOGR(".","output8")
#plot(myShapeInR)
#point_coords
  
  
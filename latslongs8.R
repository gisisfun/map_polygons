library('geosphere')
library('sp')
library('geojson')

#Create a function to print squares of numbers in sequence.

new.point <- function(latlong,dist,angle) {   
    #c <- destPoint(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), b=angle, d=dist*100, a=6378137, f=1/298.257223563)
    c <- geodesic(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), azi=angle, d=dist*100, a=6378137, f=1/298.257223563)
    newlatlong <- c(c[1],c[2]) 
    #print(newlatlong)
    return(newlatlong)
}

lats.list <- function(latitudes,longitudes,dist,maxlat,lats_seq) {
    angle <- 90
    i <- 0
    repeat {
        if (i>6){i <- 0}
        i <- i + 1
        latlong <- c(tail(latitudes, n=1),tail(longitudes, n=1))
        p <- new.point(latlong,dist*lats_seq[i],angle)
        if (p[1] >= maxlat){
            break
         }
        latitudes <- c(latitudes,p[1])
        longigitudes <- c(longitudes,p[2])
        
     }
    return(latitudes)
    }


longs.list <- function(latitudes,longitudes,dist,maxlong,short_gap) {
    angle <- 180
    longid <- 0
    gap <- short_gap
    repeat {
        latlong <- c(tail(latitudes, n=1),tail(longitudes, n=1))
        p <- new.point(latlong,dist*gap,angle)
        if (p[2] <= maxlong){
            break
         }
        latitudes <- c(latitudes,p[1])
        longitudes <- c(longitudes,p[2])
        
     }
    return(longitudes)
}

hexagons <- function(minlat,maxlong,maxlat,minlong,dist) {
    #bbox <- c(113.338953078, -43.6345972634, 153.569469029, -10.6681857235)

    #minlat <- c(bbox[1])
    #minlong <- c(bbox[4])
    #dist <- 57
    #maxlat <- bbox[3]
    #maxlong <- bbox[2]
    lat_offset <- 4
    short_seg <- 0.7071
    long_seg <- 1
        

    cat('\n1/7 deriving horizontal longitude (latitude or y axis) lines\n')
    lats_seq <- c(long_seg,short_seg,short_seg,long_seg,short_seg,short_seg,long_seg)
    latslist <- lats.list(minlat,minlong,dist,maxlat,lats_seq)
    

    cat('\n2/7 deriving vertical longitude (longitude or x axis) lines\n')
    longslist <- longs.list(minlat,minlong,dist,maxlong,short_seg)
    

    cat('\n3/7 deriving intersection point data between horizontal (latitude or y axis) and vertical (longitude or x axis) lines\n')
    intersect_list <- expand.grid(latslist,longslist)
    colnames(intersect_list) <- c("latitude", "longitude")
    
    cat('\n4/7 deriving polygons from intersection points\n')
    rem_lat <- max_v%%(lat_offset+4)
    if (rem_lat == 2 | rem_lat == 5 | rem_lat == 6 | rem_lat == 7){
            inc_by_rem <- TRUE
            inc_adj <- -4}
    if (rem_lat == 1 | rem_lat == 3){
            inc_by_rem <- TRUE
            inc_adj <- 0}
     if (rem_lat == 0 | rem_lat == 4){
            inc_by_rem <- FALSE
            inc_adj <- 0}
    print(inc_by_rem)
    print(inc_adj)
    top_left <- 1
    row <- 1
    last_lat_row <- 0
    hexagon <- 0
    max_v <- length(latslist)
    max_h <- length(longslist)
    
    while (top_left < (max_h)*(max_v))
        {
            vertex <- c(1,2,max_v+3,(max_v*2)+2,(max_v*2)+1,max_v)  
            vertex <- vertex + top_left
            poly_coords <- c(
            intersect_list[vertex[1], 1],
            intersect_list[vertex[1], 2], 
            intersect_list[vertex[2], 1],
            intersect_list[vertex[2], 2],
            intersect_list[vertex[3], 1],
            intersect_list[vertex[3], 2],
            intersect_list[vertex[4], 1],
            intersect_list[vertex[4], 2],
            intersect_list[vertex[5], 1],
            intersect_list[vertex[5], 2],
            intersect_list[vertex[6], 1],
            intersect_list[vertex[6], 2],
            intersect_list[vertex[1], 1],
            intersect_list[vertex[1], 2]
            )
            centre_lat <- intersect_list[vertex[0], 1] + (intersect_list[vertex[5], 1] - intersect_list[vertex[0], 1])/2
            centre_lon=intersect_list[vertex[0], 0] + (intersect_list[vertex[5], 0] - intersect_list[vertex[0], 0])/2
            if ((centre_lat != last_lat_row) or (last_lat_row == 0)) 
                {
                    bounds_n <- intersect_list[vertex[0], 1]
                    bounds_s <- intersect_list[vertex[2], 1]
                    bounds_e <- intersect_list[vertex[2], 0]
                    bounds_w <- intersect_list[vertex[5], 0]
                    last_lat_row <- centre_lat
                    geopoly = Polygon([poly_coords])       
                    hexagon+=1
                    start=(intersect_list[vertex[0]][1],intersect_list[vertex[0]][0])
                    end=(intersect_list[vertex[1]][1],intersect_list[vertex[1]][0])
##                    len_radial = geodesic(start,end).km
                    est_area = (((3 * sqrt(3))/2)*pow(radial,2))*.945 #estimate polygon area}
            }
    #intersect_list[1]
    
    #vertex = [1+top_left, 2+top_left, max_v+3+top_left, (max_v*2)+2+top_left, (max_v*2)+1+top_left, max_v+top_left]
    
    
    
    
    poly_points <- matrix(poly_coords, ncol=2, byrow=TRUE)
    poly_x <- poly_coords[c(TRUE, FALSE)]
    poly_y <- poly_coords[c(FALSE, TRUE)]

    #area in square km
    print(areaPolygon(poly_points))

    print(centroid(poly_points))
    cent <- centroid(poly_points)

    print(perimeter(poly_points))
    isok <- point.in.polygon(cent[1],cent[2],poly_x,poly_y)
    print(isok) #1 result is ok
    rem_lat <- max_v%%(lat_offset+4)
    print(rem_lat)

    cat('\npoly_x is:',poly_x,'\n')
    cat('\npoly_y is:',poly_y,'\n')
    cat('\narea is of hexagon is:',areaPolygon(poly_points),' meters squared \n')
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

    print('the end')

}

hexagons(113.338953078, -43.6345972634, 153.569469029, -10.6681857235, 57)

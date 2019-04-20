library('geosphere')
library('sp')

#Create a function to print squares of numbers in sequence.

new.point <- function(latlong,dist,angle) {   
    #c <- destPoint(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), b=angle, d=dist*100, a=6378137, f=1/298.257223563)
    c <- geodesic(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), azi=angle, d=dist*100, a=6378137, f=1/298.257223563)
    newlatlong <- c(c[1],c[2]) 
    #print(newlatlong)
    return(newlatlong)
}

lats.list <- function(lats,longs,dist,maxlat,long_gap,short_gap) {
    angle <- 90
gap <- 
    repeat {
        latlong <- c(tail(lats, n=1),tail(longs, n=1))
        p <- new.point(latlong,dist,angle)
        if (p[1] >= maxlat){
            break
         }
        lats <- c(lats,p[1])
        longs <- c(longs,p[2])
        
     }
    return(lats)
    }


longs.list <- function(latitudes,longitudes,dist,maxlong,short_gap,long_gap) {
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
hexagons <- function() {
    bbox <- c(113.338953078, -43.6345972634, 153.569469029, -10.6681857235)

    minlat <- c(bbox[1])
    minlong <- c(bbox[4])
    dist <- 57
    maxlat <- bbox[3]
    maxlong <- bbox[2]
    lat_offset <- 4
    
    print('lats')
    latslist <- lats.list(minlat,minlong,dist,maxlat,0.7071,1)
    latslist

    print('longs')
    longslist <- longs.list(minlat,minlong,dist,maxlong,0.7071,0.7071)
    longslist

    latslongslist <- expand.grid(latslist,longslist)
    colnames(latslongslist) <- c("latitude", "longitude")
    latslongslist

    top_left <- 1
    max_v <- length(latslist)
    #latslongslist[1]
    plisttemp <- c(1,2,max_v+3,(max_v*2)+2,(max_v*2)+1,max_v)  
    plist <- plisttemp + ((top_left+4)*2) 
    #vertex = [1+top_left, 2+top_left, max_v+3+top_left, (max_v*2)+2+top_left, (max_v*2)+1+top_left, max_v+top_left]
    poly_xy <- c(
    latslongslist[plist[1], 1],
    latslongslist[plist[1], 2], 
    latslongslist[plist[2], 1],
    latslongslist[plist[2], 2],
    latslongslist[plist[3], 1],
    latslongslist[plist[3], 2],
    latslongslist[plist[4], 1],
    latslongslist[plist[4], 2],
    latslongslist[plist[5], 1],
    latslongslist[plist[5], 2],
    latslongslist[plist[6], 1],
    latslongslist[plist[6], 2],
    latslongslist[plist[1], 1],
    latslongslist[plist[1], 2]
    )
    
    poly_points <- matrix(poly_xy, ncol=2, byrow=TRUE)
    poly_x <- poly_xy[c(TRUE, FALSE)]
    poly_y <- poly_xy[c(FALSE, TRUE)]

    #area in square km
    print(areaPolygon(poly_points))

    print(centroid(poly_points))
    cent <- centroid(poly_points)

    print(perimeter(poly_points))
    isok <- point.in.polygon(cent[1],cent[2],poly_x,poly_y)
    print(isok) #1 result is ok
    rem_lat <- max_v%%(lat_offset+4)
    print(rem_lat)

    if (rem_lat == 2 | rem_lat == 5 | rem_lat == 6 | rem_lat == 7){
            inc_by_rem <- 1
            inc_adj <- -4}
    if (rem_lat == 1 | rem_lat == 3){
            inc_by_rem <- 1
            inc_adj <- 0}
     if (rem_lat == 0 | rem_lat == 4){
            inc_by_rem <- 0
            inc_adj <- 0}
    print(inc_by_rem)
    print(inc_adj)

    p = Polygon(poly_points)
    ps = Polygons(list(p),1)
    sps = SpatialPolygons(list(ps))
    plot(sps)
    print('the end')
}

hexagons()

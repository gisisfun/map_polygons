library('geosphere')
#library('geojson')
library('sp')


#Create a function to print squares of numbers in sequence.

new.point <- function(latlong,dist,angle) {   
    #c <- destPoint(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), b=angle, d=dist*100, a=6378137, f=1/298.257223563)
    c <- geodesic(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), azi=angle, d=dist*100, a=6378137, f=1/298.257223563)
    newlatlong <- c(c[1],c[2]) 
    #print(newlatlong)
    return(newlatlong)
}

dist.points <- function(latlong1,latlong2) {   
    dist <- distGeo(cbind(tail(latlong1[1], n=1),tail(latlong1[2], n=1)), cbind(tail(latlong2[1], n=1),tail(latlong2[2], n=1)), a=6378137, f=1/298.257223563)
    return(dist)
}

horizontal <- function(east,south,west,north,radial,hor_seq) {
    #1/7 deriving horizontal list of reference points for longitude or (x axis or north to south) lines
    angle <- 180
    new_north <-north
    cat(east,new_north,south,'\n')
    i <- 0
    latitudes <- vector()
    longitudes <- vector()
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

 vertical <- function(east,south,west,north,radial,vert_seq) {
    #2/7 deriving vertical list of reference points for latitude lines or (y axis or east to west) lines
    angle <- 90
    i <-0
    new_east <- east
    latitudes <- vector()
    longitudes <- vector()
    repeat 
        {  
           i <- i + 1
           if (i < 5) {i <- i} else {i <- 1}          
           latlong <- c(new_east,north)
           p <- new.point(latlong,radial*vert_seq[i],angle)
           new_east <- p[1]
           if (new_east >= west){ break}
           latitudes <- c(latitudes,p[1])
           longitudes <- c(longitudes,p[2])      
        }
    return(latitudes)
    }


makeHexagon <- function(poly_coords,bounds_e,bounds_n,bounds_s,bounds_w,est_area,centre_lat,centre_lon,hexagon,row) 
{ 
    templ_hexagon <-'{"geometry": {"coordinates": [[[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x1, y1]]], "type": "Polygon"}, "properties": {"E": be, "N": bn, "S": bs, "W": bw, "est_area": earea, "lat": latc, "lon": lonc, "p": polyn, "row": rown}, "type": "Feature"}, '
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
    out_hexagon <- gsub("rown", row, out_hexagon) 
    
    return(out_hexagon)
}

is.even <- function(x) {return(!is.odd(x))}
 
is.odd <- function(x) {return(intToBits(x)[1] == 1)}

hexagons <- function(east,south,west,north,radial) {
    #bbox <- c(113.338953078, -43.6345972634, 153.569469029, -10.6681857235)

    #east <- c(bbox[1]) #east
    #north <- c(bbox[4]) #north
    #dist <- 57
    #west <- bbox[3] #west
    #south <- bbox[2] #south
    cat('\nMaking hexagon shapes starting from ',north,',',west,',',' to ',south,',',east,' with a radial length of ',radial,' km\n')
    #init bits
    top_left <- 0 #R starts at 1 not 0
    lat_offset <- 4
    short_seg <- 0.7071
    long_seg <- 1
    gj_string <- ""
    odd_row <- TRUE
    even_row <- FALSE
    do_log <- FALSE

    #1/7 deriving horizontal list of reference points for longitude or (x axis or north to south) lines
    cat('\n1/7 deriving horizontal list of reference points for longitude or (x axis or north to south) lines\n')
    hor_seq =c(short_seg, short_seg, short_seg, short_seg)

    h_list <- horizontal(east,south,west,north,radial,hor_seq)
    max_h <- length(h_list)
    
    cat('\n2/7 deriving vertical list of reference points for latitude lines or (y axis or east to west) lines\n')
    vert_seq <- c(short_seg, long_seg, short_seg,long_seg) 
    v_list <- vertical(east,south,west,north,radial,vert_seq)
    max_v <- length(v_list)
    print(v_list)

    cat('\n3/7 deriving intersection point data between horizontal (latitude or east to west) and vertical (longitude or x axis or north to south) lines\n')
    intersect_list <- expand.grid(v_list,h_list)
    colnames(intersect_list) <- c("latitude", "longitude")
    
#not working    

    inc_by_rem <- TRUE
    inc_adj <- 0
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

    cat('\n4/7 deriving polygons from intersection points\n')
    row <- 1

    intersect_len <- nrow(intersect_list)# intersect_list is a dataframe
    last_lat_row <- 0
    hexagon <- 0
    poly_row_count <- round((max_v/max_h),0)
                
    max_val <- ((max_h)*(max_v-3))-(max_h*0.5)
    while (top_left < max_val)
 
        {
            
            vertex <- c(1, 2, max_v+3, (max_v*2)+2, (max_v*2)+1, max_v+0)+top_left
 
            
            poly_coords <- c(intersect_list[vertex[1], 1], intersect_list[vertex[1], 2], intersect_list[vertex[2], 1], 
                intersect_list[vertex[2], 2], intersect_list[vertex[3], 1], intersect_list[vertex[3], 2],intersect_list[vertex[4], 1], 
                intersect_list[vertex[4], 2], intersect_list[vertex[5], 1], intersect_list[vertex[5], 2],intersect_list[vertex[6], 1], 
                intersect_list[vertex[6], 2], intersect_list[vertex[1], 1], intersect_list[vertex[1], 2])

            poly_points <- matrix(poly_coords, ncol=2, byrow=TRUE)
            centre_lat <- poly_coords[2] + (poly_coords[12] - poly_coords[2])/2
            centre_lon <- poly_coords[1] + (poly_coords[11] - poly_coords[1])/2
            dist_check <- dist.points(intersect_list[vertex[1], ],intersect_list[vertex[2], ])

            
            if (do_log == TRUE)
                {
                    cat('\npoly:',hexagon,'top_left:',top_left,'max_val:', max_val)
                    cat('\npoly:',hexagon,'row:',row,'odd_row:',odd_row,'even_row:',even_row)
                    cat('\npoly:',hexagon,'top_left:',top_left,'intersect_list len:',intersect_len)
                    cat('\npoly:',hexagon,'centre_lat:',centre_lat,' centre_lon:',centre_lon)
                    cat('\npoly:',hexagon,'lat_last_row:',last_centre_lat,'dist_check:',dist_check)
                    cat('\npoly:',hexagon,'point 1:x',poly_coords[1],',y',poly_coords[2],'point 2:x',poly_coords[3],',y',poly_coords[4])
                    cat('\npoly:',hexagon,'area:',areaPolygon(poly_points),' m^2')
                    cat('\npoly:',hexagon,'vertex:',vertex)
                    cat('\npoly:',hexagon,'points:',poly_coords)
                    cat('\npoly:',hexagon,'lat 1:',poly_coords[1],'lat 3:',poly_coords[5],'lat 6:',poly_coords[11])
                }
            
            if ((centre_lat != last_lat_row) || (last_lat_row == 0))  #are we on the first or current row of polygons?
                {
                    bounds_n <- poly_points[1,2] #intersect_list[vertex[0]][1]
                    bounds_s <- poly_points[3,2] #intersect_list[vertex[2]][1]
                    bounds_e <- poly_points[3,1] #intersect_list[vertex[2]][0]
                    bounds_w <- poly_points[6,1] #intersect_list[vertex[5]][0]

                    last_lat_row <- centre_lat
                    
                    
                    hexagon <- hexagon + 1
                    start <- c(poly_coords[2],poly_coords[1] )
                    end <- c(poly_coords[4],poly_coords[3])
                    est_area <- 0.945 * ((3 * sqrt(3))/2)*(radial^2) #estimate polygon area
                    geopoly <- makeHexagon(poly_coords,bounds_e,bounds_n,bounds_s,bounds_w,est_area,centre_lat,centre_lon,hexagon,row)

                    if (do_log == TRUE)
                        {
                            cat('\npoly:',hexagon,'lat 1 is greater than lat 6 is',(poly_coords[1] > poly_coords[11]))
                            cat('\npoly:',hexagon,'lat 1 is less than lat 3 is',(poly_coords[1] < poly_coords[5]),'\n')
                        }

                    #if ((poly_coords[1] > poly_coords[11])) 
                    if (bounds_e > bounds_w) 
                        {
                            #print(top_left)
                            gj_string <- paste(gj_string, geopoly,"")                    
                        }             
                }#end last centre lat check if statement 
        last_row <- row
        last_centre_lat <- centre_lat
        row <- round(hexagon/poly_row_count,0)+1
        top_left <- top_left + lat_offset

        if (row != last_row)
            {
                top_left <- top_left + inc_adj
                if (inc_by_rem == TRUE) {top_left <-  top_left + rem_lat}
                if (row %% 2 == 0) 
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
                    }
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

output <- hexagons(113.338953078, -43.6345972634, 153.569469029, -10.6681857235, 57)
fileConn<-file("output8.json")
writeLines(output, fileConn)
close(fileConn)

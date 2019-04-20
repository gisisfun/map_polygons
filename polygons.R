library('geosphere')


#Create a function to print squares of numbers in sequence.

new.point <- function(latlong,dist,angle) {
    
    c <- destPoint(cbind(tail(latlong[1], n=1),tail(latlong[2], n=1)), b=angle, d=dist*100, a=6378137, f=1/298.257223563)
    newlatlong <- c(c[1],c[2]) 
    #print(newlatlong)
    return(newlatlong)
}

lats.list <- function(lats,longs,dist,maxlat) {
    angle <- 90
    #for (i in  1:10){
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


longs.list <- function(lats,longs,dist,maxlong) {
    angle <- 180
    longid <- 0
    repeat {
        latlong <- c(tail(lats, n=1),tail(longs, n=1))
        p <- new.point(latlong,dist,angle)
        if (p[2] <= maxlong){
            break
         }
        lats <- c(lats,p[1])
        longs <- c(longs,p[2])
        
     }
    return(longs)
}

bbox <- c(113.338953078, -43.6345972634, 153.569469029, -10.6681857235)

minlat <- c(bbox[1])
minlong <- c(bbox[4])
dist <- 1000
maxlat <- bbox[3]
maxlong <- bbox[2]

print('lats')
latslist <- lats.list(minlat,minlong,dist,maxlat)
latslist

print('longs')
longslist <- longs.list(minlat,minlong,dist,maxlong)
longslist

latslongslist <- expand.grid(latslist,longslist)
colnames(latslongslist) <- c("latitude", "longitude")
latslongslist



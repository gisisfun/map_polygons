#Include libraries
library(dggridR)
library(dplyr)
library(maps)
#Construct a global grid with cells approximately 1000 miles across
dggs <- dgconstruct(spacing=200, metric=FALSE, resround='down')

#Load included test data set
#data(dgquakes)

#Get the corresponding grid cells for each earthquake epicenter (lat-long pair)
MyData <- world.cities[world.cities$country.etc == "Australia",]
MyData$cell <- dgGEO_to_SEQNUM(dggs,MyData$long,MyData$lat)$seqnum

#Converting SEQNUM to GEO gives the center coordinates of the cells
cellcenters   <- dgSEQNUM_to_GEO(dggs,MyData$cell)

#Get the number of earthquakes in each cell
datacounts   <- MyData %>% group_by(cell) %>% summarise(count=n())

#Get the grid cell boundaries for cells which had quakes
grid          <- dgcellstogrid(dggs,MyData$cell,frame=TRUE,wrapcells=TRUE)

#Update the grid cells' properties to include the number of earthquakes
#in each cell
grid          <- merge(grid,datacounts,by.x="cell",by.y="cell")

#Make adjustments so the output is more visually interesting
grid$count    <- log(grid$count)
cutoff        <- quantile(grid$count,0.9)
grid          <- grid %>% mutate(count=ifelse(count>cutoff,cutoff,count))

#Get polygons for each country of the world
countries <- map_data("world")

# Plot everything on a flat map

p<- ggplot() + 
    geom_polygon(data=countries, aes(x=long, y=lat, group=group), fill=NA, color="black")   +
    geom_polygon(data=grid,      aes(x=long, y=lat, group=group, fill=count), alpha=0.4)    +
    geom_path   (data=grid,      aes(x=long, y=lat, group=group), alpha=0.4, color="white") +
#    geom_point  (aes(x=cellcenters$lon_deg, y=cellcenters$lat_deg)) +
    scale_fill_gradient(low="blue", high="red")
    
p

#Replot on a spherical projection
#p+coord_map("ortho", orientation = c(-33.49831, 133.9223, 0)) #+
#  xlab('')+ylab('')+
#  theme(axis.ticks.x=element_blank())+
#  theme(axis.ticks.y=element_blank())+
#  theme(axis.text.x=element_blank())+
#  theme(axis.text.y=element_blank())+
#  ggtitle('Your data could look like this')

p+coord_cartesian(xlim = c(96,168), ylim = c(-8,-45)) +
  ggtitle('Your data could look like this')

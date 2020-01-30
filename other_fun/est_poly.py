from geopy import distance
from math import sqrt
width = distance.geodesic((-8,96),(-8,168)).km
height = distance.geodesic((-8,96),(-45,96)).km
bound_area = height*width
#Area = (3 √3(n)2 ) / 2
radius = 47
area = round((((3 * sqrt(3)) / 2) * (radius** 2)) * 0.9296869521917159,0)



print('area',area)
count = bound_area/area
print(int(count))

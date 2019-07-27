import sys
import pandas as pd
import numpy as np
import json
from geopy.distance import distance,geodesic
from geojson import Polygon,Feature,FeatureCollection
from math import pow,sqrt
import pandas as pd
import subprocess
import urllib.request
from pyunpack import Archive
import os
import itertools


def myexpand_grid(x, y):
    xG, yG = np.meshgrid(x, y) # create the actual grid
    xG = xG.flatten() # make the grid 1d
    yG = yG.flatten() # same
    return ( xG, yG)


def horizontal_lines(b_lat_min, b_lat_max, b_lon_min, b_lon_max, hor_seq,
radial):
    print('\n1/7 deriving horizontal longitude lines')
    #lines of latitude from north to south
    #across min and max bounds latitude
    #min and max longitude from west to east
    hor_line_list = []
    hor_line_points = []
    seq = 0
    line = [[b_lat_min, b_lon_min], [b_lat_min, b_lon_max]]
    hor_line_list.append(line)
    ref_point = [b_lat_min, b_lon_min]
    hor_line_points.append([b_lon_min, b_lat_min])
    offset = point_radial_distance(ref_point, 180, radial * hor_seq[0])
    hor_line_points.append([offset[1], offset[0]])
    ref_lat = offset[0]
    ref_lon = offset[1]
    while (ref_lat > b_lat_max):
        if seq < 3:
            seq += 1
        else:
            seq = 0
        line = [[ref_lat, b_lon_min], [ref_lat, b_lon_max]]
        hor_line_list.append(line)
        ref_point = [ref_lat, ref_lon]
        offset = point_radial_distance(ref_point, 180, radial * hor_seq[seq])
        hor_line_points.append([offset[1], offset[0]])
        ref_lat = offset[0]
        ref_lon = offset[1]
    num_h = len(hor_line_list)
    print('derived {0} longitudinal lines'.format(num_h))
    return hor_line_list


def vertical_lines(b_lat_min, b_lat_max, b_lon_min, b_lon_max, vert_seq
, radial):
    print('\n2/7 deriving vertical latitude lines ')
    #lines of longitude from west to east
    #across min and max bounds from longitude
    #min to max latitude north to south
    vert_line_list = []
    vert_line_points = []
    # ns_dist = geodesic([b_lat_min,b_lon_min],[b_lat_max],[b_lon_max]]).kilometers
    line = [[b_lat_min, b_lon_min], [b_lat_max, b_lon_min]]
    vert_line_list.append(line)
    seq = 0
    ref_point = [b_lat_min, b_lon_min]
    vert_line_points.append([b_lon_min, b_lat_min, vert_seq[seq]])
    offset = point_radial_distance(ref_point, 90, radial * vert_seq[seq])
    vert_line_points.append([offset[1], offset[0], vert_seq[seq]])
    ref_lon = offset[1]
    ref_lat = offset[0]
    while (ref_lon < b_lon_max):
        if seq < 3:
            seq += 1
        else:
            seq = 0
        line = [[b_lat_min, ref_lon], [b_lat_max, ref_lon]]
        vert_line_list.append(line)
        ref_point = [ref_lat, ref_lon]
        offset = point_radial_distance(ref_point, 90, radial * vert_seq[seq])
        vert_line_points.append([offset[1], offset[0], vert_seq[seq]])
        ref_lon = offset[1]
        ref_lat = offset[0]

    num_v = len(vert_line_list)
    # max_v = (num_v)  # -1)##-((num_v-1) % 4)
    print('derived {0} latitude lines'.format(num_v))
    return vert_line_list

def point_radial_distance(self,brng,radial):
    return geodesic(kilometers=radial).destination(point = self, bearing = brng)

def line_intersection(line1, line2):
    #source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
    

def params(shape,north,south,east,west,radial):
    print('Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km'.format(shape, north, west, south, east, radial))

def intersectionsnew(hor_line_list, vert_line_list):
    #print("hor_max",hor_line_list[-1][0][0],hor_max,"vert_max",vert_line_list[-1][1][1,vert_max)
    print('\n3/7 deriving intersection point data between horizontal and \
    vertical lines')
    intersect_list = []
    for h in hor_line_list:
        for v in vert_line_list:
            intersect_list.append((h,v))

    print('derived {0} points of intersection'.format(len(intersect_list)))
    return intersect_list

def intersections(hor_line_list, hor_max, vert_line_list, vert_max):
    #print("hor_max",hor_line_list[-1][0][0],hor_max,"vert_max",vert_line_list[-1][1][1,vert_max)
    print('\n3/7 deriving intersection point data between horizontal and \
    vertical lines')
    intersect_list = []
    for h in range(0, hor_max):
        for v in range(0, vert_max):
            intersect_point = line_intersection(hor_line_list[h],
            vert_line_list[v])
            intersect_data = [intersect_point[1], intersect_point[0]]
            intersect_list.append(intersect_data)

    print('derived {0} points of intersection'.format(len(intersect_list)))
    return intersect_list


def expand_grid(x, y):
    xG, yG = np.meshgrid(x, y) # create the actual grid
    xG = xG.flatten() # makeimport sys
    yG = yG.flatten() # same
    return pd.DataFrame({'x':xG, 'y':yG})

def horizontal(east,north,west,south,hor_seq,radial):
    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
    angle = 180
    new_north = north
    #print(east,new_north,south,'\n')
    i = 0
    longitudes = []
    longitudes.append([[north,west],[north,east]])

    while new_north >= south:
        if i > 3:
            i = 0
            
        latlong = [new_north,east]
        p = point_radial_distance(latlong,angle,radial * hor_seq[i]) 
        new_north = p[0]
        longitudes.append([[p[0],west],[p[0],east]])
        i += 1
    del longitudes[-1]
    return longitudes


def vertical(east,north,west,south,vert_seq,radial):
    print('east {0} west {1}'.format(east,west))
    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
    angle = 90

    i = 0
    new_west = west
    latitudes =[]
    latitudes.append([[north,west],[south,west]])
    while new_west <= east:
        if i > 3:
            i = 0

        latlong = [north,new_west]
        p = point_radial_distance(latlong,angle,radial*vert_seq[i])
        new_west = p[1]
        latitudes.append([[north,p[1]],[south,p[1]]])    
        i += 1
        
    del latitudes[-1]
    return latitudes

def horizontalnew(east,north,west,south,hor_seq,radial):
    #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
    angle = 180
    new_north = north
    #print(east,new_north,south,'\n')
    i = 0
    longitudes = []
    longitudes.append(north)

    while new_north >= south:
        if i > 3:
            i = 0
            
        latlong = [new_north,east]
        p = point_radial_distance(latlong,angle,radial * hor_seq[i]) 
        new_north = p[0]
        longitudes.append(p[0])
        i += 1
    #del longitudes[-1]
    return longitudes


def verticalnew(east,north,west,south,vert_seq,radial):
    print('east {0} west {1}'.format(east,west))
    #2/7 deriving horizontal list of reference points from east to west for latitudes or y axis
    angle = 90

    i = 0
    new_west = west
    latitudes =[]
    latitudes.append(west)
    while new_west <= east:
        if i > 3:
            i = 0

        latlong = [north,new_west]
        p = point_radial_distance(latlong,angle,radial*vert_seq[i])
        new_west = p[1]
        latitudes.append(p[1])    
        i += 1
    del latitudes[-1]
    #del latitudes[-1]
    
    return latitudes


def hexagonsnew(north,south,east,west,radial,outfile):   

    params('hexagons',north,south,east,west,radial)
    
    if (os.name is 'posix'):
        cmd_text='/usr/bin/ogr2ogr'
        slash='/'
    else:
        cmd_text='ogr2ogr.exe'
        slash='\/'    
    #init bits
    poly_list = []
    point_list =[]
    g_array=[] #array of geojson formatted geometry elements
    tabular_list=[] #array of all polygons and tabular columns
    layer_dict={'Bounds':{'Australia':{'North': north ,'South': south,'West': west,'East': east}}}
    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4326
    layer_dict['Param']['shape'] = 'hexagon'  
    layer_dict['Hexagon']={}
    layer_dict['Hexagon']['short'] = 0.707108
    layer_dict['Hexagon']['long'] = 1
    
    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west
    #east,north,west,south
    #bounds_lon_max,bounds_lat_min,bounds_lon_min,bounds_lat_max
    hor_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short']]
    
    vert_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']]
    #
    # New Bit Start
    #
    
    h_line_list = horizontalnew(bounds_lon_max, bounds_lat_min, bounds_lon_min, bounds_lat_max,hor_seq, radial)
    max_h = len(h_line_list)    
    #print(h_line_list)
    v_line_list = verticalnew(bounds_lon_max, bounds_lat_min, bounds_lon_min, bounds_lat_max, vert_seq, radial)
    #print(v_line_list)
    
    max_v = len(v_line_list)
    #fred = intersections(h_line_list, max_h, v_line_list, max_v)
    i_list = []
    for i in range((max_h-1)*(max_v)):
        h_pointer = int(i/max_v)
        v_pointer = (i% max_v)
        i_list.append([v_line_list[v_pointer],h_line_list[h_pointer]])
    print('new')
    print(len(i_list))
    
    print(i_list[len(i_list)-1])
    print(i_list[2000])
    print(i_list[4000])

    #intersect_list = intersections(h_line_list, max_h, v_line_list, max_v)
    #print(len(fred))
    print('this is it')
    #print(len(list_x),len(list_y),list_x[1],list_y[1])
    #
    # New Bit End
    #



    print('\n')
    print('The End')# hexagonsnew

def hexagons(north, south, east, west, radial, outfile):

    params('hexagons', north, south, east, west, radial)
    my_os = os.name
    if (my_os is 'posix'):
        # cmd_text = '/usr/bin/ogr2ogr'
        slash = '/'
    else:
        # cmd_text = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
        slash = '\\'
    # init bits
    point_list = []
    g_array = []  # array of geojson formatted geometry elements
    tabular_list = []  # array of all polygons and tabular columns
    layer_dict = {'Bounds': {'Australia': {'North': north, 'South': south,
        'West': west, 'East': east}}}
    layer_dict['Param'] = {}
    layer_dict['Param']['side_km'] = radial
    layer_dict['Param']['epsg'] = 4326
    layer_dict['Param']['shape'] = 'hexagon'
    layer_dict['Hexagon'] = {}
    layer_dict['Hexagon']['short'] = 0.707108
    layer_dict['Hexagon']['long'] = 1

    bounds_lat_min = north
    bounds_lat_max = south
    bounds_lon_max = east
    bounds_lon_min = west

    hor_seq = [layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'],
    layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short']]

    vert_seq = [layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'],
    layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']]

    h_line_list = horizontal_lines(bounds_lat_min, bounds_lat_max,
    bounds_lon_min, bounds_lon_max, hor_seq, radial)
    max_h = len(h_line_list)
    print(len(h_line_list))
    v_line_list = vertical_lines(bounds_lat_min, bounds_lat_max,
    bounds_lon_min, bounds_lon_max, vert_seq, radial)
    max_v = len(v_line_list)
    
    print(len(v_line_list))
    #intersect_list = intersections(h_line_list, max_h, v_line_list, max_v)
    intersect_list_new = intersectionsnew(h_line_list, v_line_list)
    
    print(len(intersect_list))
    #array output
    print(intersect_list_new[164],intersect_list_new[165])
    print(intersect_list_new[328],intersect_list_new[329])
    #
    
    print('\n',
          h_line_list[0][0][0],
          v_line_list[1][1][1],
          '\n',
          h_line_list[1][0][0],
          v_line_list[1][1][1])
          
    i_list = []
    for i in range(len(h_line_list)*len(v_line_list)):
        h_pointer = int(i/max_v)
        v_pointer = (i% max_v)
        i_list.append([v_line_list[v_pointer][1][1],h_line_list[h_pointer][0][0]])    
       
    print('*** old-new bit ***')
    print(len(intersect_list)-1,len(i_list)-1,intersect_list[len(intersect_list)-1],i_list[len(i_list)-1])
    print(2000,intersect_list[2000],i_list[2000])
    print(4000,intersect_list[4000],i_list[4000])
    print('this is it')

(shape, b_north, b_south, b_east, b_west, radial_d, f_name) = ['hex', -8, -45, 168, 96, 57, 'hex_57km']
print('***old***')
hexagons(b_north, b_south, b_east, b_west, radial_d, f_name)
print('***new bits***')
hexagonsnew(b_north, b_south, b_east, b_west, radial_d, f_name)

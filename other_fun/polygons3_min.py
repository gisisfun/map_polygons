
import pandas as pd
import json
from geopy.distance import geodesic
from geojson import Feature,FeatureCollection
import shapely.geometry as shply
import geojson as gj
from math import pow,sqrt
import random

#1 deg longitude is about 88 km, 1 deg latitude  is about 110 km
#http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.001July%202016?OpenDocument
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
    return latitudes

def intersections(hor_line_list,hor_max,vert_line_list,vert_max):
    print('\n3/5 deriving intersection point data between horizontal and vertical lines')
    intersect_list=[]
    for h in range(0,hor_max):
        for v in range(0,vert_max):
            intersect_point=line_intersection(hor_line_list[h],vert_line_list[v])            
            intersect_data = [intersect_point[1],intersect_point[0]]
            intersect_list.append(intersect_data)          

    print('derived {0} points of intersection'.format(len(intersect_list)))  
    return intersect_list

def params(shape,north,south,east,west,radial):
    print('Making {0} hex shapes starting from {1},{2} to {3},{4} with a radial length of {5} km'.format(shape, north, west, south, east, radial))

def point_in_polygon(coords_list,point_x,point_y):  
    poly = shply.Polygon(coords_list)
    p1=shply.Point(point_x, point_y)
    return p1.within(poly)

def points_in_polygon(poly_coords,poly_id,bound_points_df):
    p_count=0
    poly = shply.Polygon(poly_coords)
    i=0
    for index, row in bound_points_df.iterrows():
        #p1 = shply.Point(query_points_list[i][0],query_points_list[i][1])
        p1 = shply.Point(row['longitude'], row['latitude'])
        
        if poly.contains(p1) is True:
            p_count += 1 
        i += 1        
    return poly_id,p_count

def hexagons(north,south,east,west,radial,col_name,lat_longs):
#def hexagons(north,south,east,west,radial,outfile):   
    params('hexagons',north,south,east,west,radial)
    lat_longs_df=pd.DataFrame(lat_longs)
    lat_longs_df.columns = ['longitude','latitude']
    

    #init bits
    poly_list = []
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

    #1/5 deriving horizontal list of reference points from north to south for longitudes or x axis
    hor_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['short']]
    h_line_list = horizontal(east,north,west,south, hor_seq,radial)
    max_h = len(h_line_list)

    #2/5 deriving horizontal list of reference points from east to west for latitudes or y axis
    vert_seq =[layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long'], layer_dict['Hexagon']['short'], layer_dict['Hexagon']['long']]
    v_line_list = vertical(east,north,west,south, vert_seq,radial)    
    max_v = len(v_line_list)

    #3/5 deriving intersection point data between horizontal and vertical lines
    intersect_list = intersections(h_line_list,max_h,v_line_list,max_v)
    intersect_df = pd.DataFrame(intersect_list) #convert intersect array to tabular data frame
    intersect_df.columns = ['lat','long']
    #intersect_df.to_csv('csv{slash}intersect_dataset.csv'.format(outfile=outfile,slash=slash), sep=',')
    lat_offset = 4
    top_left = 0
    poly_row_count =int(max_v/ (len(hor_seq)))
    rem_lat = max_v % (lat_offset+len(hor_seq))
    layer_dict['Row_1']={}
    layer_dict['Row_1']['lat_offset'] = lat_offset
    layer_dict['Row_1']['poly_row_count'] = poly_row_count
    layer_dict['Row_1']['remain_lat'] = rem_lat
            
    print('first row of hexagons starting from {0}, {1} hexagons, {2} latitude line(s) remaining'.format(top_left,poly_row_count,rem_lat))

    inc_by_rem = True
    inc_adj = 0
        
    if rem_lat is 2 or rem_lat is 5 or rem_lat is 6 or rem_lat is 7:
        inc_by_rem = True
        inc_adj = -4
    if rem_lat is 1 or rem_lat is 3:
        inc_by_rem = True
        inc_adj = 0
    if rem_lat is 0 or rem_lat is 4:
        inc_by_rem = False
        inc_adj = 0

    print('\n4/5 deriving polygons from intersection data')
    row=1
    last_lat_row=0
    hexagon=0
    #max_val=((max_h)*(max_v-3))-(max_h*0.255)
    while (top_left < (max_h)*(max_v)):
        vertex = [1+top_left, 2+top_left, max_v+3+top_left, (max_v*2)+2+top_left, (max_v*2)+1+top_left, max_v+top_left]
        try:
            poly_coords = [intersect_list[vertex[0]], intersect_list[vertex[1]], intersect_list[vertex[2]], intersect_list[vertex[3]], intersect_list[vertex[4]], intersect_list[vertex[5]], intersect_list[vertex[0]]]
             
            centre_lat=intersect_list[vertex[0]][1] + (intersect_list[vertex[5]][1 ] - intersect_list[vertex[0]][1])/2
            centre_lon=intersect_list[vertex[0]][0] + (intersect_list[vertex[5]][0] - intersect_list[vertex[0]][0])/2
         
            if (centre_lat is not last_lat_row) or last_lat_row is 0:
                bounds_n = intersect_list[vertex[0]][1]
                bounds_s = intersect_list[vertex[2]][1]
                bounds_e = intersect_list[vertex[2]][0]
                bounds_w = intersect_list[vertex[5]][0]
                last_lat_row=centre_lat

                #geopoly = gj.Polygon([poly_coords])       
                hexagon+=1
                #start=(intersect_list[vertex[0]][1],intersect_list[vertex[0]][0])
                #end=(intersect_list[vertex[1]][1],intersect_list[vertex[1]][0])

                est_area = (((3 * sqrt(3))/2)*pow(radial,2))*.945 #estimate polygon area

                #geo_poly = Feature(geometry=geo_poly, properties={"p": hexagon,"row": row, "lat": centre_lat, "lon": centre_lon, "N": bounds_n, "S": bounds_s, "E": bounds_e, "W": bounds_w, "est_area": est_area})
                if  (bounds_e>bounds_w):
                    #append geojson geometry definition attributes to list
                    #*** new bit here ***
                    
                    points_df=lat_longs_df[(lat_longs_df['latitude'] >= bounds_s) & \
                                              (lat_longs_df['latitude'] <= bounds_n)  & \
                                              (lat_longs_df['longitude'] <= bounds_e) & \
                                              (lat_longs_df['longitude'] >= bounds_w)]

                    total_rows = len(points_df)                    
                    pcount=0
                    if (total_rows >= 1):
                        (poly,pcount)=points_in_polygon(poly_coords,hexagon,points_df)

                    #*** new bit here ***
                    template='''{"geometry": {"coordinates": [[[x0, y0], [x1, y1],\
[x2, y2], [x3, y3], [x4, y4], [x5, y5], [x0, y0]]], "type": "Polygon"}, \
"properties": {"p": polyval, "col_name": colval, "est-area": areaval}, \
"type": "Feature"}'''

                    geopoly=template.replace('x0',str(intersect_list[vertex[0]][0]))\
                             .replace('y0',str(intersect_list[vertex[0]][1]))\
                             .replace('x1',str(intersect_list[vertex[1]][0]))\
                             .replace('y1',str(intersect_list[vertex[1]][1]))\
                             .replace('x2',str(intersect_list[vertex[2]][0]))\
                             .replace('y2',str(intersect_list[vertex[2]][1]))\
                             .replace('x3',str(intersect_list[vertex[3]][0]))\
                             .replace('y3',str(intersect_list[vertex[3]][1]))\
                             .replace('x4',str(intersect_list[vertex[4]][0]))\
                             .replace('y4',str(intersect_list[vertex[4]][1]))\
                             .replace('x5',str(intersect_list[vertex[5]][0]))\
                             .replace('y5',str(intersect_list[vertex[5]][1]))\
                             .replace('polyval',str(hexagon))\
                             .replace('colval',str(pcount))\
                             .replace('areaval',str(est_area))
                    g_array.append(geopoly)   
                    
                    #tabular dataset
                    tabular_line = [top_left, row, centre_lat, centre_lon, bounds_n, bounds_s, \
                                    bounds_e, bounds_w, est_area]
                    tabular_list.append(tabular_line) #array of polygon and tabular columns
            else:#centre_not last_row or last_lat_row is not 0
                donothing=True  
                
        except IndexError:
            donothing=True
        
        last_row = row
        last_lat_row=centre_lat
        row=int(1+int(hexagon/poly_row_count))
        top_left += lat_offset

        if row is not last_row:
            top_left += inc_adj
            if inc_by_rem:
                top_left += rem_lat
            if row % 2 is 0: # is even
                top_left += 2
            if row & 1:# is odd
                top_left += -2    
    print('\n5/5 geojson dataset of {0} derived hexagon polygons'.format(len(g_array)))
    hextext=', '.join(g_array)
    hexagons_geojson='{"features": ['+hextext+'], "type": "FeatureCollection"}'
    g_array=[] #release g_array - array of geojson geometry elements

    print('\n')
    print('The End')# hexagons
    return hexagons_geojson
    
def test_hexagons():
    bounds_n=-8
    bounds_s=-45
    bounds_e=168
    bounds_w=96
    file = open('geojson_layer.json', 'w') #open file for writing geojson layer in geojson format
    file.write(str(hexagons(bounds_n,bounds_s,bounds_e,bounds_w, 57,'random',random_points(bounds_n,bounds_s,bounds_e,bounds_w,1000)))) #write geojson layer to open file
    file.close() #close file
    
def random_points(bounds_n,bounds_s,bounds_e,bounds_w,numpoints):
    layer_dict={'Bounds':{'Australia':{'North': bounds_n ,'South': bounds_s,'West': bounds_w,'East': bounds_e}}}
    layer_dict['Param']={}
    layer_dict['Param']['side_km'] = {}
    layer_dict['Param']['epsg'] = 4326
    layer_dict['Param']['shape'] = 'hexagon'
    layer_dict['Column']={}
    layer_dict['Column']['Random']={}
    layer_dict['Column']['Random']['X_Coord']={}
    layer_dict['Column']['Random']['Y_Coord']={}
    
    
    ns_range = bounds_n - bounds_s
    ew_range = bounds_e - bounds_w
    coord_list=[]

    x_coords_list=[]
    y_coords_list=[]
    
    for i in range(0,numpoints):
        y_coord = bounds_s+random.randrange(0, ns_range*10000)/10000
        x_coord = bounds_w+random.randrange(0, ew_range*10000)/10000
        coord=[x_coord,y_coord]
        coord_list.append(coord)
        x_coords_list.append(x_coord)
        y_coords_list.append(y_coord)
        
    layer_dict['Column']['Random']['X_Coord']=x_coords_list
    layer_dict['Column']['Random']['Y_Coord']=y_coords_list
    layer_json=json.dumps(layer_dict)
    print(layer_json)
    return coord_list    
   
#print(random_points(-8,-45,168,96,2))
test_hexagons()


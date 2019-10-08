from geopy.distance import distance,geodesic
from isotiles.Tools import next_point
import numpy as np

class Fred:
    """
    Define Tile shape and extent
    North: maximum Latitude value 
    East: minimum longitude value
    South: minimum latitude value
    West: maximum longitude value
    Shape: either 'hex' or 'box'
    """


    def dump(self):

        print(self.North, self.East, self.South, 
              self.West, self.Shape, self.Radial,'\n')


    def __init__(self, Bounds_North: float = -8,
                 Bounds_West: float = 96,
                 Bounds_South: float = -45,
                 Bounds_East: float = 168,
                 Shape: str = 'hex',
                 Radial_km: float = 45):
        
        self.North = Bounds_North
        self.East = Bounds_East
        self.South = Bounds_South
        self.West = Bounds_West
        self.Shape = Shape
        self.Radial = Radial_km

        
        if Shape is 'hex':
            self.Hor_Seq = [0.7071,1,0.7071,1]
            self.Vert_Seq = [0.7071,0.7071,0.7071,0.7071]
            self.Pattern = np.array( [[0,1,1,0],[1,0,0,1],[0,1,1,0],[1,0,0,1]])
            self.inc_by_rem = True
            self.inc_adj = 0
            #if self.rem_lat is in [0, 1, 2, 3, 4, 5, 6, 7]:
            lat_offset = 4
            self.H_List = self.horizontal()
            self.V_List = self.vertical()                        
            self.V_Len = len(self.V_List)

            rem_lat = self.V_Len % (lat_offset + len(self.Hor_Seq))
            
            if rem_lat in [2, 5, 6, 7]:
                self.inc_by_rem = True
                self.inc_adj = -4
            if rem_lat in [1, 3]:
                self.inc_by_rem = True
                self.inc_adj = 0
            if rem_lat in [0, 4]:
                self.inc_by_rem = False
                self.inc_adj = 0

        else:
            #box
            self.Hor_Seq = [1,1,1,1]
            self.Vert_Seq = [1,1,1,1]
            self.Pattern = np.array( [[1,1,1,1],[1,0,1,0],[1,1,1,1],[1,0,1,0]])



        
        self.PatternGrid = np.tile(A = self.Pattern, reps = [int(self.V_Len/4),int(((self.H_Len/3)/1.333333333333334))])
        self.Intersect_List = self.intersections()


    def line_intersection(self,line1,line2):
        # source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-between-two-lines-in-python
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

    def intersections(self):
        print('\n3/7 deriving intersection point data between horizontal and \
        vertical lines')
        intersect_list = []
        for h in range(0, self.H_Len):
            for v in range(0, self.V_Len):
                #print(self.H_List[h],self.V_List[v])
                intersect_point = self.line_intersection(self.H_List[h],self.V_List[v])
                intersect_data = [intersect_point[1], intersect_point[0]]
                intersect_list.append(intersect_data)

        print('derived {0} points of intersection'.format(len(intersect_list)))
        return intersect_list
        

    def horizontal(self):
        """
        horizontal function derives a list of vertical reference points from north to south for longitudes or x axis
    """
        print(self.Hor_Seq)
        angle = 180
        new_north = self.North
        new_east = self.East
        #print(self.east,new_north,self.south,'\n')
        i = 0
        longitudes = []
        longitudes.append([[self.North,self.West],[self.North,self.East]])

        while new_north >= self.South:
            if i > 3:
                i = 0
            
            latlong = [new_north,new_east]
            p = next_point(latlong,angle,self.Radial * self.Hor_Seq[i]) 
            new_north = p[0]
            new_east = p[1]
            longitudes.append([[latlong[0],latlong[1]],[p[0],p[1]]])
            i += 1
        
        self.H_Len = len(longitudes)
        self.H_List = longitudes
        return longitudes


    def vertical(self):
        """
        vertical funtion derives a list of horizontal reference points from east to west for latitudes or y axis
        
        """

        print('east {0} west {1}'.format(self.East,self.West))

        angle = 90

        i = 0
        new_north = self.North
        new_west = self.West
        latitudes =[]
        latitudes.append([[self.North,self.West],[self.South,self.East]])
        while new_west <= self.East:
            if i > 3:
                i = 0
            latlong = [new_north,new_west]
            p = next_point(latlong,angle,self.Radial*self.Vert_Seq[i])
            new_north = p[0]
            new_west = p[1]
            latitudes.append([[latlong[0],latlong[1]],[p[0],p[1]]])    
            i += 1
        
        self.V_Len = len(latitudes)
        self.V_List = latitudes
        return latitudes
    
    
    def poly_array_box(self):
        max_h = self.H_Len - 1
        max_v = self.H_Len - 1
        intersect_list = self.Intersect_List
        g_array = []  # array of geojson formatted geometry elements
        tabular_list = []  # array of all polygons and tabular columns
        print('\n4/7 deriving boxes polygons from intersection data')
        top_left = 0
        vertex = [top_left + 0, top_left + 1, top_left + max_v + 1,
                  top_left + max_v]

        while (vertex[2] < (max_h) * (max_v)):
            poly_coords = [intersect_list[vertex[0]],
                intersect_list[vertex[1]], intersect_list[vertex[2]],
                intersect_list[vertex[3]], intersect_list[vertex[0]]]
            centre_lat = intersect_list[vertex[0]][1] + \
                         (intersect_list[vertex[2]][1] - intersect_list[vertex[0]][1]) / 2
            centre_lon = intersect_list[vertex[0]][0] \
                         + (intersect_list[vertex[2]][0] - intersect_list[vertex[0]][0]) / 2
            bounds_n = intersect_list[vertex[0]][1]
            bounds_s = intersect_list[vertex[3]][1]
            bounds_e = intersect_list[vertex[1]][0]
            bounds_w = intersect_list[vertex[0]][0]
            if bounds_e > bounds_w:
                geopoly = Polygon([poly_coords])
                geopoly = Feature(geometry=geopoly,
                properties={"p": top_left, "lat": centre_lat, "lon": centre_lon, \
                            "N": bounds_n, "S": bounds_s, "E": bounds_e, "W": bounds_w})
                g_array.append(geopoly)
                #append geojson geometry definition attributes to list
                #tabular dataset
                tabular_line = [top_left, centre_lat, centre_lon, \
                                bounds_n, bounds_s, bounds_e, bounds_w]
                tabular_list.append(tabular_line)
                #array of polygon and tabular columns

            #increment values
            top_left += 1
            vertex = [top_left + 0, top_left + 1, top_left + max_v + 1, top_left \
                      + max_v]
        return g_array

    def poly_array_hex(self):
        max_h = self.H_Len - 1
        max_v = self.H_Len - 1
        intersect_list = self.Intersect_List
        lat_offset = 4
        top_left = 0
        poly_row_count = int(max_v / (len(hor_seq)))
        rem_lat = max_v % (lat_offset + len(hor_seq))
        print('first row starting from {0}, {1} hexagons, {2} latitude line(s) remaining'.format(top_left, poly_row_count, rem_lat))

        inc_by_rem = self.inc_by_rem
        inc_adj = self.inc_adj
        
        print('\n4/7 deriving hexagon polygons from intersection data')
        row = 1
        last_lat_row = 0
        hexagon = 0
        row = 1
        while (top_left < (max_h) * (max_v)):
            vertex = [1 + top_left, 2 + top_left, max_v + 3 + top_left, \
                      (max_v * 2) + 2 + top_left, (max_v * 2) + 1 + top_left, max_v \
                      + top_left]
            try:
                poly_coords = [intersect_list[vertex[0]], \
                                intersect_list[vertex[1]], intersect_list[vertex[2]], \
                                intersect_list[vertex[3]], intersect_list[vertex[4]], \
                                intersect_list[vertex[5]], intersect_list[vertex[0]]]
                centre_lat = intersect_list[vertex[0]][1] + (intersect_list[vertex[5]][1] \
                                                             - intersect_list[vertex[0]][1]) / 2
                centre_lon = intersect_list[vertex[0]][0] + (intersect_list[vertex[5]][0] \
                                                             - intersect_list[vertex[0]][0]) / 2
                # if (centre_lat is not last_lat_row) or last_lat_row is 0:
                
                bounds_n = intersect_list[vertex[0]][1]
                bounds_s = intersect_list[vertex[2]][1]
                bounds_e = intersect_list[vertex[2]][0]
                bounds_w = intersect_list[vertex[5]][0]
                last_lat_row = centre_lat
                geopoly = Polygon([poly_coords])
                hexagon += 1
                # start = (intersect_list[vertex[0]][1],
                # intersect_list[vertex[0]][0])
                # end = (intersect_list[vertex[1]][1],
                # intersect_list[vertex[1]][0])
                # len_radial = geodesic(start,end).km
                est_area = (((3 * sqrt(3)) / 2) * pow(radial, 2)) * 0.945
                #estimate polygon area
                geopoly = Feature(geometry = geopoly, properties = \
                                  {"p": hexagon,"row": row, "lat": centre_lat \
                                   , "lon": centre_lon, "N": bounds_n, "S": bounds_s \
                                   , "E": bounds_e, "W": bounds_w, "est_area": est_area})
                if  (bounds_e > bounds_w):
                    for i in range(0, 5):
                        point_list.append([hexagon, str(intersect_list[vertex[i]][0]) \
                                           + str(intersect_list[vertex[i]][1])])
                        g_array.append(geopoly)
                        #append geojson geometry definition attributes to list
                        #tabular dataset
                        tabular_line = [top_left, row, centre_lat, centre_lon, \
                                        bounds_n, bounds_s, bounds_e, bounds_w, est_area]
                        tabular_list.append(tabular_line)
                        #array of polygon and tabular columns
                else:
                    donothing = True

            except IndexError:
                donothing = True

            last_row = row
            last_lat_row = centre_lat
            row = int(1 + int(hexagon / poly_row_count))
            top_left += lat_offset
            if row is not last_row:
                top_left += inc_adj
                if inc_by_rem:
                    top_left += rem_lat
                if row % 2 is 0:
                    top_left += 2
                if row & 1:
                    top_left += -2

        return g_array
    
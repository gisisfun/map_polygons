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
        else:
            self.Hor_Seq = [1,1,1,1]
            self.Vert_Seq = [1,1,1,1]
            self.Pattern = np.array( [[1,1,1,1],[1,0,1,0],[1,1,1,1],[1,0,1,0]])

        self.H_List = self.horizontal()
        self.V_List = self.vertical()

        self.H_Len = len(self.H_List)
        self.V_Len = len(self.V_List)

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
        return latitudes


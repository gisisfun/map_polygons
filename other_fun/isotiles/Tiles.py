from geopy.distance import distance,geodesic
from isotiles.Tools import next_point

class Fred:
    """
    Define Tile shape and extent

    North: maximum Latitude value 
    East: minimum longitude value
    South: minimum latitude value
    West: maximum longitude value
    Shape: either 'hex' or 'box'


    """

    def __init__(self, Bounds_North: float = -8,
                 Bounds_East: float = 96,
                 Bounds_South: float = -45,
                 Bounds_West: float = 168,
                 Shape: str = 'hex',
                 Radial_km: float = 45):
        
        self.North = Bounds_North
        self.East = Bounds_East
        self.South = Bounds_South
        self.West = Bounds_West
        self.Shape = Shape
        self.Radial = Radial_km
        if Shape is 'hex':
            self.hor_seq = [0.7071,1,0.7071,1]
            self.vert_seq = [0.7071,0.7071,0.7071,0.7071]
        else:
            self.hor_seq = [1,1,1,1]
            self.vert_seq = [1,1,1,1]


    def dump(self):
        print(self.North, self.East, self.South, self.West, self.Shape, self.Radial)


    def horizontal(self):
        #1/7 deriving vertical list of reference points from north to south for longitudes or x axis
        angle = 180
        new_north = self.North
        #print(self.east,new_north,self.south,'\n')
        i = 0
        longitudes = []
        longitudes.append([[self.North,self.West],[self.North,self.East]])

        while new_north >= self.South:
            if i > 3:
                i = 0
            
            latlong = [new_north,self.East]
            p = next_point(latlong,angle,self.Radial * self.hor_seq[i]) 
            new_north = p[0]
            longitudes.append([[p[0],self.West],[p[0],self.East]])
            i += 1
        return longitudes
    
        

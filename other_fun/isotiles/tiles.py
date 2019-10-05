class tiles:
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




    def dump(self):
        print(self.North, self.East, self.South, self.West, self.Shape, self.Radial)
        
        
    
        

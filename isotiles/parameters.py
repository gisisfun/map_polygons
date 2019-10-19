class Bounding_Box:
    """
    Parameters for request to create tessilating shapes
    """
    ...
    class Australia:
        __slots__ = ("North","South","East","West","Radial","Shape")
    
        def __init__(self):
            """
            Init
            """
            self.North = -8
            self.South = -45
            self.East = 168
            self.West = 96
            self.Radial = 57
            self.Shape = 'hex'

class Offsets:
    """
    Offset ratios for underlying points grid
    """

    __slots__ = ("Short","Long")
    def __init__(self):
        self.Short = 0.7071
        self.Long = 1

class OSVars:
    """
    Operating System Dependant values for 'posix' and 'nt'
    """

    class posix:
        __slots__ = ("Slash","ogr2ogr")
        def __init__(self):
            self.Slash = '/'
            self.ogr2ogr = '/usr/bin/ogr2ogr'
        

    class nt:
        __slots__ = ("Slash","ogr2ogr")
        def __init__(self):
            self.Slash = '\\'
            self.ogr2ogr = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'

class DataSets:
    

    class Australia:
        """
        ABS Australian Boundary
        """    
        ...
    
    
        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}AUS_2016_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_aus_2016_aust_shape.zip'
                
    
        class TabFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Tab'
                self.FilePath = 'tabfiles{slash}AUS_2016_AUST.tab'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
                self.ZipDir = 'tabfiles'
                self.ZipPath ='tabfiles{slash}1270055001_aus_2016_aust_tab.zip'
                
                
                
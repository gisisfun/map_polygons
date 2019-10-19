class Defaults:
    """
    Parameters for request to create tessilating shapes
    """
    ...
    
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


class Australia:
    """
    Operating System Dependant values for 'posix' and 'nt'
    """    
    ...
    
    
    class ShapeFormat:
        __slots__= ('FilePath', 'DownPrompt', 'DownURL', 'ZipDir', 'ZipPath', 'ZipPrompt')
        def __init__(self):
            self.FilePath = 'shapefiles{slash}AUS_2016_AUST.shp'
            self.DownPrompt = 'Downloading ABS Australia file in Shape file format'
            self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
            self.ZipDir = 'shapefiles'
            self.ZipPath ='shapefiles{slash}1270055001_aus_2016_aust_shape.zip'
            self.ZipPrompt = 'Unzipping ABS Australia file in Shape file format'
        
    
    class TabFormat:
        __slots__= ('FilePath', 'DownPrompt', 'DownURL', 'ZipDir', 'ZipPath', 'ZipPrompt')
        def __init__(self):
            self.FilePath = 'tabfiles{slash}AUS_2016_AUST.tab'
            self.DownPrompt = 'Downloading ABS Australia file in Tab file format'
            self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
            self.ZipDir = 'tabfiles'
            self.ZipPath ='tabfiles{slash}1270055001_aus_2016_aust_tab.zip'
            self.ZipPrompt = 'Unzipping ABS Australia file in Tab file format'
        
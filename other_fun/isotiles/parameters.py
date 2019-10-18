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

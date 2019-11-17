class Defaults:
    """
    """
    ...
    __slots__ = ("Radial","Shape","ShapefilesPath","TabfilesPath", "MetaDataPath", \
                 "GeoJSONPath","CSVPath","ImagesPath","SQLPath","SpatialitePath", \
                 "VRTPath","Weight")
    
    def __init__(self):
        self.Radial = 57
        self.Shape = 'hex'
        self.ShapefilesPath = 'shapefiles'
        self.TabfilesPath  = 'tabfiles'
        self.MetaDataPath = 'metadata'
        self.GeoJSONPath = 'geojson'
        self.CSVPath = 'csv'
        self.ImagesPath = 'images'
        self.SQLPath = 'sql'
        self.SpatialitePath = 'spatialite_db'
        self.VRTPath = 'vrt'
        self.Weight = "place"

class Projection:
    """
    Project Values
    """
    class WGS84:
        """
        WGS 84 Projection
        World Geodectic System 1984, used in GPS
        """
        __slots__ = ("EPSG","name","Perimeter","invFlat")
        def __init__(self):
            self.EPSG = '4326'
            self.Name = 'WGS 84'
            self.Perimeter = 6378137
            self.invFlat = 298.257223563
            
    class GDA94:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("EPSG","name","Perimeter","Flatness")
        def __init__(self):
            self.EPSG = '4283'
            self.Name = 'GDA 84'
            self.Perimeter = 6378137
            self.invFlat = 298.257222101         
            
    class GDA2020:
        """
        GDA 94 Projection
        Geocentric Datum of Australia 1994
        """
        __slots__ = ("EPSG","name","Perimeter","invFlat")
        def __init__(self):
            self.EPSG = '7844'
            self.Name = 'GDA 2020'
            self.Perimeter = 6378137
            self.invFlat = 298.257222101  

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
        __slots__ = ("Slash","Ogr2ogr","Spatialite")
        def __init__(self):
            self.Slash = '/'
            self.Ogr2ogr = '/usr/bin/ogr2ogr'
            self.Spatialite = 'spatialite'
        

    class nt:
        __slots__ = ("Slash","Ogr2ogr","Spatialite")
        def __init__(self):
            self.Slash = '\\'
            self.Ogr2ogr = 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Spatialite = 'c:\\OSGeo4W64\\bin\\sqlite3.exe'

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
                
    class Statistical_Areas_Level_1_2011:

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            def __init__(self):
                self.Description = '2011 ABS Statistical Areas Level 1'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
    class Statistical_Areas_Level_1_2016:

        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'ABS Australia'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.DownURL = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_tab.zip&1270.0.55.001&Data%20Cubes&39A556A0197D8C02CA257FED00140567&0&July%202016&12.07.2016&Latest'
                self.ZipDir = 'shapefiles'
                self.ZipPath ='shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'
                
    class AGIL_Dataset:
        
        class CSVFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'AGIL DataSet'
                self.Format = 'CSV'
                self.FilePath = 'csv{slash}agil_locations20190208.csv'
                self.DownURL = 'https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv'                
                self.ZipDir = 'csv'
                self.ZipPath =''
                
    class OpenStreetMaps:
        
        class ShapeFormat:
            __slots__= ('Description','Format','FilePath', 'DownURL', 'ZipDir', 'ZipPath')
            
            def __init__(self):
                self.Description = 'OpenStreetMaps'
                self.Format = 'Shape'
                self.FilePath = 'shapefiles{slash}gis_osm_places_free_1.shp'
                self.DownURL = 'https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip'
                self.ZipDir = 'shapefiles'
                self.ZipPath = 'shapefiles{slash}australia-latest-free.shp.zip'

    class GNAFLocality:
        class List:

	    def __init__(self):
                self.headings = ['locality_name','state_abbreviation','postcode','latitude','longitude']
		
    class GeoNames:

        class Cities:

            def __init__(self):
                self.headings = ['city','city_ascii','lat','lng','country','iso2','iso3','admin_name','capital','population','id']
                self.Items = [
['Kingoonya','Kingoonya',-30.8996,135.3,'Australia','AU','AUS','South Australia','',50,1036942792],
['Port Denison','Port Denison',-29.2828,114.9166,'Australia','AU','AUS','Western Australia','',1213,1036873405], 
['Cairns','Cairns',-16.8878,145.7633,'Australia','AU','AUS','Queensland','',154225,1036016939],  
['Kwinana','Kwinana',-32.2394,115.7702,'Australia','AU','AUS','Western Australia','',20086,1036753478], 
['Cranbourne','Cranbourne',-38.0996,145.2834,'Australia','AU','AUS','Victoria','',460491,1036639986],  
['Port Hedland','Port Hedland',-20.3104,118.606,'Australia','AU','AUS','Western Australia','',14288,1036509606], 
['Port Lincoln','Port Lincoln',-34.7332,135.8666,'Australia','AU','AUS','South Australia','',13630,1036558150],  
['Port Macquarie','Port Macquarie',-31.445,152.9187,'Australia','AU','AUS','New South Wales','',48547,1036051032], 
['Port Pirie','Port Pirie',-33.1911,137.99,'Australia','AU','AUS','South Australia','',12506,1036571606],  
['Portland','Portland',-38.34,141.59,'Australia','AU','AUS','Victoria','',11808,1036439594], 
['Proserpine','Proserpine',-20.4162,148.5835,'Australia','AU','AUS','Queensland','',3976,1036150859],  
['Busselton','Busselton',-33.6564,115.3487,'Australia','AU','AUS','Western Australia','',10214,1036911902], 
['Caboolture','Caboolture',-27.083,152.95,'Australia','AU','AUS','Queensland','',31513,1036273434], 
['Cooma','Cooma',-36.2396,149.12,'Australia','AU','AUS','New South Wales','',6520,1036070931], 
['Streaky Bay','Streaky Bay',-32.8119,134.2149,'Australia','AU','AUS','South Australia','',1060,1036134944], 
['Sunbury','Sunbury',-37.5696,144.71,'Australia','AU','AUS','Victoria','',29925,1036519781], 
['Sydney','Sydney',-33.92,151.1852,'Australia','AU','AUS','New South Wales','admin',4630000,1036074917], 
['Karumba','Karumba',-17.4833,140.8334,'Australia','AU','AUS','Queensland','',173,1036926106], 
['Esperance','Esperance',-33.8573,121.8889,'Australia','AU','AUS','Western Australia','',7888,1036299314], 
['Exmouth','Exmouth',-21.9311,114.1233,'Australia','AU','AUS','Western Australia','',1085,1036006022], 
['Forbes','Forbes',-33.3896,148.02,'Australia','AU','AUS','New South Wales','',4838,1036523834], 
['Morawa','Morawa',-29.2163,116,'Australia','AU','AUS','Western Australia','',259,1036194388], 
['Moree','Moree',-29.4699,149.8301,'Australia','AU','AUS','New South Wales','',8203,1036377829], 
['Katherine','Katherine',-14.4666,132.2666,'Australia','AU','AUS','Northern Territory','',10141,1036323110], 
['Katoomba','Katoomba',-33.7069,150.32,'Australia','AU','AUS','New South Wales','',22076,1036674004], 
['Launceston','Launceston',-41.4498,147.1302,'Australia','AU','AUS','Tasmania','',72458,1036170383], 
['Laverton','Laverton',-28.627,122.404,'Australia','AU','AUS','Western Australia','',316,1036624366], 
['Leeton','Leeton',-34.5449,146.3973,'Australia','AU','AUS','New South Wales','',7299,1036102538], 
['Leonara','Leonara',-28.8815,121.328,'Australia','AU','AUS','Western Australia','',227,1036140404], 
['Seymour','Seymour',-37.0342,145.1273,'Australia','AU','AUS','Victoria','',3693,1036919223], 
['Singleton','Singleton',-32.5695,151.16,'Australia','AU','AUS','New South Wales','',13813,1036947514], 
['Newcastle','Newcastle',-32.8453,151.815,'Australia','AU','AUS','New South Wales','',1134616,1036468001], 
['Norseman','Norseman',-32.2,121.7666,'Australia','AU','AUS','Western Australia','',1004,1036257263], 
['Batemans Bay','Batemans Bay',-35.6896,150.2073,'Australia','AU','AUS','New South Wales','',10557,1036272805], 
['Bathurst','Bathurst',-33.4196,149.57,'Australia','AU','AUS','New South Wales','',6111,1036446465], 
['Griffith','Griffith',-34.29,146.04,'Australia','AU','AUS','New South Wales','',15455,1036563313], 
['Whyalla','Whyalla',-33.025,137.5614,'Australia','AU','AUS','South Australia','',22559,1036961366], 
['Wilcannia','Wilcannia',-31.5662,143.3833,'Australia','AU','AUS','New South Wales','',442,1036134474], 
['Katanning','Katanning',-33.6996,117.5501,'Australia','AU','AUS','Western Australia','',3934,1036411379], 
['Bongaree','Bongaree',-27.0787,153.1509,'Australia','AU','AUS','Queensland','',13649,1036269345], 
['Bordertown','Bordertown',-36.3162,140.7666,'Australia','AU','AUS','South Australia','',2583,1036115980], 
['Boulia','Boulia',-22.8996,139.9,'Australia','AU','AUS','Queensland','',600,1036512474], 
['Bourke','Bourke',-30.1,145.9333,'Australia','AU','AUS','New South Wales','',2475,1036074667], 
['Mackay','Mackay',-21.1439,149.15,'Australia','AU','AUS','Queensland','',75922,1036507374], 
['Southern Cross','Southern Cross',-31.2161,119.3167,'Australia','AU','AUS','Western Australia','',187,1036931490], 
['Ulladulla','Ulladulla',-35.3495,150.47,'Australia','AU','AUS','New South Wales','',9250,1036687220], 
['Victor Harbor','Victor Harbor',-35.5596,138.6173,'Australia','AU','AUS','South Australia','',7760,1036536547], 
['Andamooka','Andamooka',-30.431,137.1656,'Australia','AU','AUS','South Australia','',528,1036260794], 
['Hervey Bay','Hervey Bay',-25.2887,152.8409,'Australia','AU','AUS','Queensland','',25114,1036833938], 
['Gunnedah','Gunnedah',-30.987,150.2623,'Australia','AU','AUS','New South Wales','',7148,1036500021], 
['Gympie','Gympie',-26.1886,152.6709,'Australia','AU','AUS','Queensland','',11649,1036391013], 
['Halls Creek','Halls Creek',-18.2667,127.7667,'Australia','AU','AUS','Western Australia','',1209,1036444511], 
['Hamilton','Hamilton',-37.7312,142.0234,'Australia','AU','AUS','Victoria','',8869,1036699883], 
['Winton','Winton',-22.3996,143.0333,'Australia','AU','AUS','Queensland','',1157,1036031036], 
['Mudgee','Mudgee',-32.5896,149.5801,'Australia','AU','AUS','New South Wales','',5391,1036213564], 
['Ivanhoe','Ivanhoe',-32.8996,144.3,'Australia','AU','AUS','New South Wales','',265,1036571526], 
['Pannawonica','Pannawonica',-21.6366,116.325,'Australia','AU','AUS','Western Australia','',686,1036914573], 
['Dubbo','Dubbo',-32.26,148.5973,'Australia','AU','AUS','New South Wales','',31574,1036855042], 
['Tom Price','Tom Price',-22.6935,117.7931,'Australia','AU','AUS','Western Australia','',2723,1036464109], 
['Parkes','Parkes',-33.1296,148.17,'Australia','AU','AUS','New South Wales','',11137,1036977270], 
['Sale','Sale',-38.1096,147.06,'Australia','AU','AUS','Victoria','',22486,1036960753], 
['Bendigo','Bendigo',-36.76,144.28,'Australia','AU','AUS','Victoria','',81657,1036537913], 
['Berri','Berri',-34.2829,140.6,'Australia','AU','AUS','South Australia','',4716,1036554717], 
['Adelaide','Adelaide',-34.935,138.6,'Australia','AU','AUS','South Australia','admin',1145000,1036538171], 
['Adelaide River','Adelaide River',-13.2495,131.1,'Australia','AU','AUS','Northern Territory','',237,1036136750], 
['Albany','Albany',-35.0169,117.8916,'Australia','AU','AUS','Western Australia','',26445,1036047365], 
['Burketown','Burketown',-17.7161,139.5666,'Australia','AU','AUS','Queensland','',200,1036956849], 
['Burnie','Burnie',-41.0666,145.9167,'Australia','AU','AUS','Tasmania','',19972,1036394657], 
['Penola','Penola',-37.383,140.8167,'Australia','AU','AUS','South Australia','',1514,1036121853], 
['Perth','Perth',-31.955,115.84,'Australia','AU','AUS','Western Australia','admin',1532000,1036178956], 
['Peterborough','Peterborough',-32.9662,138.8333,'Australia','AU','AUS','South Australia','',1689,1036104272], 
['Scone','Scone',-32.0796,150.8501,'Australia','AU','AUS','New South Wales','',4624,1036918224], 
['Scottsdale','Scottsdale',-41.1495,147.5167,'Australia','AU','AUS','Tasmania','',2468,1036807079], 
['Narrabri','Narrabri',-30.3319,149.7874,'Australia','AU','AUS','New South Wales','',7082,1036714493], 
['Narrogin','Narrogin',-32.9329,117.1666,'Australia','AU','AUS','Western Australia','',4238,1036221961], 
['Townsville','Townsville',-19.25,146.77,'Australia','AU','AUS','Queensland','',138954,1036500020], 
['Traralgon','Traralgon',-38.1996,146.53,'Australia','AU','AUS','Victoria','',18226,1036938861], 
['Central Coast','Central Coast',-33.42,151.3,'Australia','AU','AUS','New South Wales','',3026,1036067845], 
['Broome','Broome',-17.9618,122.2308,'Australia','AU','AUS','Western Australia','',13218,1036047905], 
['Bunbury','Bunbury',-33.3443,115.6502,'Australia','AU','AUS','Western Australia','',26998,1036561011], 
['Wyndham','Wyndham',-15.374,128.3601,'Australia','AU','AUS','Western Australia','',800,1036474435], 
['Yamba','Yamba',-29.423,153.3533,'Australia','AU','AUS','New South Wales','',1806,1036259324], 
['Tumby Bay','Tumby Bay',-34.3829,136.0833,'Australia','AU','AUS','South Australia','',1791,1036529327], 
['Forster-Tuncurry','Forster-Tuncurry',-32.1931,152.5266,'Australia','AU','AUS','New South Wales','',17591,1036846186], 
['Bundaberg','Bundaberg',-24.8791,152.3509,'Australia','AU','AUS','Queensland','',52472,1036377333], 
['Yulara','Yulara',-25.2405,130.9889,'Australia','AU','AUS','Northern Territory','',930,1036245584], 
['Richmond','Richmond',-33.5995,150.74,'Australia','AU','AUS','New South Wales','',13880,1036934091], 
['Richmond','Richmond',-20.7163,143.1333,'Australia','AU','AUS','Queensland','',296,1036156498], 
['Rockhampton','Rockhampton',-23.3639,150.52,'Australia','AU','AUS','Queensland','',65850,1036768986], 
['Roebourne','Roebourne',-20.7829,117.1333,'Australia','AU','AUS','Western Australia','',19260,1036752479], 
['Roma','Roma',-26.5594,148.7907,'Australia','AU','AUS','Queensland','',5496,1036698836], 
['Cloncurry','Cloncurry',-20.7,140.5,'Australia','AU','AUS','Queensland','',1202,1036672657], 
['Cobram','Cobram',-35.9196,145.65,'Australia','AU','AUS','Victoria','',4659,1036438159], 
['Coffs Harbour','Coffs Harbour',-30.3071,153.1123,'Australia','AU','AUS','New South Wales','',62978,1036320442], 
['Colac','Colac',-38.3395,143.58,'Australia','AU','AUS','Victoria','',9089,1036633113], 
['Alice Springs','Alice Springs',-23.701,133.88,'Australia','AU','AUS','Northern Territory','',27710,1036830397], 
['Ararat','Ararat',-37.2795,142.91,'Australia','AU','AUS','Victoria','',6110,1036674088], 
['Carnarvon','Carnarvon',-24.8998,113.6501,'Australia','AU','AUS','Western Australia','',7392,1036344209], 
['Ceduna','Ceduna',-32.0991,133.6623,'Australia','AU','AUS','South Australia','',1586,1036725988], 
['Charleville','Charleville',-26.4,146.25,'Australia','AU','AUS','Queensland','',1900,1036575498], 
['Charters Towers','Charters Towers',-20.0809,146.2587,'Australia','AU','AUS','Queensland','',9573,1036733088], 
['Kalbarri','Kalbarri',-27.6662,114.1667,'Australia','AU','AUS','Western Australia','',1537,1036429141], 
['Kununurra','Kununurra',-15.7666,128.7333,'Australia','AU','AUS','Western Australia','',5679,1036556231], 
['Dalby','Dalby',-27.1939,151.2657,'Australia','AU','AUS','Queensland','',9847,1036053707], 
['Lithgow','Lithgow',-33.4961,150.1528,'Australia','AU','AUS','New South Wales','',11128,1036591538], 
['Manjimup','Manjimup',-34.2333,116.15,'Australia','AU','AUS','Western Australia','',4240,1036022434], 
['Maitland','Maitland',-32.721,151.555,'Australia','AU','AUS','New South Wales','',18625,1036034945], 
['Mandurah','Mandurah',-32.5235,115.7471,'Australia','AU','AUS','Western Australia','',73356,1036773118], 
['Karratha','Karratha',-20.7304,116.87,'Australia','AU','AUS','Western Australia','',16796,1036951388], 
['Gawler','Gawler',-34.6074,138.7264,'Australia','AU','AUS','South Australia','',16362,1036309493], 
['Geelong','Geelong',-38.1675,144.3956,'Australia','AU','AUS','Victoria','',160991,1036870987], 
['Georgetown','Georgetown',-18.3,143.5333,'Australia','AU','AUS','Queensland','',818,1036412066], 
['Geraldton','Geraldton',-28.7666,114.6,'Australia','AU','AUS','Western Australia','',27258,1036811875], 
['Maryborough','Maryborough',-37.0496,143.73,'Australia','AU','AUS','Victoria','',7046,1036781601], 
['Maryborough','Maryborough',-25.5491,152.7209,'Australia','AU','AUS','Queensland','',20678,1036205623], 
['McMinns Lagoon','McMinns Lagoon',-12.5329,131.05,'Australia','AU','AUS','Northern Territory','',5025,1036673821], 
['Toowoomba','Toowoomba',-27.5645,151.9555,'Australia','AU','AUS','Queensland','',92800,1036765315], 
['Onslow','Onslow',-21.6576,115.0963,'Australia','AU','AUS','Western Australia','',573,1036255184], 
['Orange','Orange',-33.28,149.1,'Australia','AU','AUS','New South Wales','',39329,1036760396], 
['Stawell','Stawell',-37.0596,142.76,'Australia','AU','AUS','Victoria','',6991,1036073093], 
['Echuca','Echuca',-36.1296,144.75,'Australia','AU','AUS','Victoria','',19457,1036292989], 
['Eidsvold','Eidsvold',-25.3662,151.1333,'Australia','AU','AUS','Queensland','',459,1036235197], 
['Emerald','Emerald',-23.5122,148.1673,'Australia','AU','AUS','Queensland','',9398,1036124660], 
['Tamworth','Tamworth',-31.1026,150.9171,'Australia','AU','AUS','New South Wales','',38551,1036233388], 
['Taree','Taree',-31.8976,152.4618,'Australia','AU','AUS','New South Wales','',44182,1036855717], 
['Ballarat','Ballarat',-37.5596,143.84,'Australia','AU','AUS','Victoria','',85109,1036567186], 
['Ballina','Ballina',-28.8614,153.568,'Australia','AU','AUS','New South Wales','',14242,1036040102], 
['Barcaldine','Barcaldine',-23.5662,145.2834,'Australia','AU','AUS','Queensland','',1068,1036284609], 
['Mount Barker','Mount Barker',-34.6328,117.6666,'Australia','AU','AUS','Western Australia','',1781,1036651498], 
['Mount Gambier','Mount Gambier',-37.8313,140.765,'Australia','AU','AUS','South Australia','',23209,1036932780], 
['Mount Isa','Mount Isa',-20.7239,139.49,'Australia','AU','AUS','Queensland','',33200,1036386100], 
['Mount Magnet','Mount Magnet',-28.0662,117.8167,'Australia','AU','AUS','Western Australia','',424,1036327720], 
['Kempsey','Kempsey',-31.0874,152.822,'Australia','AU','AUS','New South Wales','',11840,1036897003], 
['Queanbeyan','Queanbeyan',-35.3546,149.2113,'Australia','AU','AUS','New South Wales','',32602,1036846465], 
['Queenstown','Queenstown',-42.0829,145.55,'Australia','AU','AUS','Tasmania','',2352,1036082142], 
['Quilpie','Quilpie',-26.6166,144.25,'Australia','AU','AUS','Queensland','',560,1036696232], 
['Ravensthorpe','Ravensthorpe',-33.5829,120.0333,'Australia','AU','AUS','Western Australia','',1101,1036878618], 
['Warrnambool','Warrnambool',-38.38,142.47,'Australia','AU','AUS','Victoria','',29928,1036291219], 
['Warwick','Warwick',-28.2292,152.0203,'Australia','AU','AUS','Queensland','',12347,1036412726], 
['Weipa','Weipa',-12.6666,141.8666,'Australia','AU','AUS','Queensland','',2830,1036501067], 
['Ouyen','Ouyen',-35.0662,142.3167,'Australia','AU','AUS','Victoria','',1400,1036764173], 
['Wollongong','Wollongong',-34.4154,150.89,'Australia','AU','AUS','New South Wales','',260914,1036502269], 
['Wonthaggi','Wonthaggi',-38.6095,145.59,'Australia','AU','AUS','Victoria','',5985,1036415078], 
['Kiama','Kiama',-34.7096,150.84,'Australia','AU','AUS','New South Wales','',10379,1036754695], 
['Kimba','Kimba',-33.1496,136.4334,'Australia','AU','AUS','South Australia','',636,1036035341], 
['Kingaroy','Kingaroy',-26.539,151.8406,'Australia','AU','AUS','Queensland','',8573,1036463308], 
['Pine Creek','Pine Creek',-13.8162,131.8167,'Australia','AU','AUS','Northern Territory','',665,1036858004], 
['Hobart','Hobart',-42.85,147.295,'Australia','AU','AUS','Tasmania','admin',80870,1036679838], 
['Darwin','Darwin',-12.4254,130.85,'Australia','AU','AUS','Northern Territory','admin',93080,1036497565], 
['Gingin','Gingin',-31.3496,115.9,'Australia','AU','AUS','Western Australia','',1446,1036686561], 
['Meekatharra','Meekatharra',-26.6,118.4833,'Australia','AU','AUS','Western Australia','',654,1036608457], 
['Melbourne','Melbourne',-37.82,144.975,'Australia','AU','AUS','Victoria','admin',4170000,1036533631], 
['Woomera','Woomera',-31.1496,136.8,'Australia','AU','AUS','South Australia','',450,1036392822], 
['Moranbah','Moranbah',-22.0016,148.038,'Australia','AU','AUS','Queensland','',10000,1036916453], 
['Port Augusta','Port Augusta',-32.49,137.77,'Australia','AU','AUS','South Australia','',13897,1036945368], 
['Port Douglas','Port Douglas',-16.4846,145.4587,'Australia','AU','AUS','Queensland','',3000,1036053723], 
['Gladstone','Gladstone',-23.8533,151.2467,'Australia','AU','AUS','Queensland','',30489,1036070755], 
['Gold Coast','Gold Coast',-28.0815,153.4482,'Australia','AU','AUS','Queensland','',527660,1036153217], 
['Horsham','Horsham',-36.7096,142.19,'Australia','AU','AUS','Victoria','',12830,1036654340], 
['Hughenden','Hughenden',-20.85,144.2,'Australia','AU','AUS','Queensland','',421,1036738932], 
['Northam','Northam',-31.6566,116.6534,'Australia','AU','AUS','Western Australia','',5855,1036868267], 
['Nowra','Nowra',-34.8828,150.6,'Australia','AU','AUS','New South Wales','',94781,1036984536], 
['Shepparton','Shepparton',-36.3746,145.3914,'Australia','AU','AUS','Victoria','',33550,1036030548], 
['Yeppoon','Yeppoon',-23.1329,150.7567,'Australia','AU','AUS','Queensland','',10769,1036180170], 
['Young','Young',-34.3096,148.29,'Australia','AU','AUS','New South Wales','',7501,1036073044], 
['Caloundra','Caloundra',-26.8,153.1333,'Australia','AU','AUS','Queensland','',38706,1036266942], 
['Ingham','Ingham',-18.6496,146.1666,'Australia','AU','AUS','Queensland','',6127,1036238542], 
['Innisfail','Innisfail',-17.5313,146.0387,'Australia','AU','AUS','Queensland','',10143,1036930229], 
['Inverell','Inverell',-29.7668,151.1126,'Australia','AU','AUS','New South Wales','',8561,1036652902], 
['Kingston','Kingston',-42.9911,147.3084,'Australia','AU','AUS','Tasmania','',14371,1036297213], 
['Kingston South East','Kingston South East',-36.8328,139.8501,'Australia','AU','AUS','South Australia','',206,1036261175], 
['Clare','Clare',-33.8329,138.6,'Australia','AU','AUS','South Australia','',3061,1036842122], 
['Bowen','Bowen',-20.0013,148.2087,'Australia','AU','AUS','Queensland','',10983,1036979225], 
['Melton','Melton',-37.6895,144.57,'Australia','AU','AUS','Victoria','',32368,1036007778], 
['Meningie','Meningie',-35.6995,139.3333,'Australia','AU','AUS','South Australia','',1501,1036445634], 
['Merimbula','Merimbula',-36.8996,149.9,'Australia','AU','AUS','New South Wales','',6367,1036933197], 
['Merredin','Merredin',-31.4828,118.2667,'Australia','AU','AUS','Western Australia','',2668,1036578320], 
['Mildura','Mildura',-34.185,142.1514,'Australia','AU','AUS','Victoria','',47867,1036624348], 
['Thargomindah','Thargomindah',-28,143.8167,'Australia','AU','AUS','Queensland','',203,1036793708], 
['Theodore','Theodore',-24.9495,150.0833,'Australia','AU','AUS','Queensland','',246,1036423364], 
['Three Springs','Three Springs',-29.5333,115.75,'Australia','AU','AUS','Western Australia','',190,1036669084], 
['Oatlands','Oatlands',-42.2996,147.3666,'Australia','AU','AUS','Tasmania','',1157,1036926323], 
['Wagin','Wagin',-33.2996,117.35,'Australia','AU','AUS','Western Australia','',1598,1036851354], 
['Armidale','Armidale',-30.5123,151.6675,'Australia','AU','AUS','New South Wales','',22673,1036975829], 
['Atherton','Atherton',-17.2703,145.4694,'Australia','AU','AUS','Queensland','',6959,1036456869], 
['Ayr','Ayr',-19.5702,147.3995,'Australia','AU','AUS','Queensland','',9078,1036228772], 
['Bairnsdale','Bairnsdale',-37.8296,147.61,'Australia','AU','AUS','Victoria','',11005,1036432237], 
['Camooweal','Camooweal',-19.9167,138.1167,'Australia','AU','AUS','Queensland','',187,1036815011], 
['Canberra','Canberra',-35.283,149.129,'Australia','AU','AUS','Australian Capital Territory','primary',327700,1036142029], 
['Longreach','Longreach',-23.4496,144.25,'Australia','AU','AUS','Queensland','',2894,1036622618], 
['Brisbane','Brisbane',-27.455,153.0351,'Australia','AU','AUS','Queensland','admin',1860000,1036192929], 
['Devonport','Devonport',-41.1927,146.3311,'Australia','AU','AUS','Tasmania','',19317,1036033175], 
['Wallaroo','Wallaroo',-33.9329,137.6333,'Australia','AU','AUS','South Australia','',2779,1036743246], 
['Wangaratta','Wangaratta',-36.36,146.3,'Australia','AU','AUS','Victoria','',14022,1036395326], 
['Cowell','Cowell',-33.6829,136.9166,'Australia','AU','AUS','South Australia','',537,1036921929], 
['Cowra','Cowra',-33.8296,148.68,'Australia','AU','AUS','New South Wales','',6795,1036204877], 
['Goondiwindi','Goondiwindi',-28.5548,150.3253,'Australia','AU','AUS','Queensland','',4251,1036452066], 
['Goulburn','Goulburn',-34.7496,149.7102,'Australia','AU','AUS','New South Wales','',20940,1036347537], 
['Grafton','Grafton',-29.712,152.9377,'Australia','AU','AUS','New South Wales','',9955,1036615468], 
['Murray Bridge','Murray Bridge',-35.1296,139.26,'Australia','AU','AUS','South Australia','',18194,1036345943], 
['Muswellbrook','Muswellbrook',-32.2696,150.89,'Australia','AU','AUS','New South Wales','',11630,1036253543], 
['Windorah','Windorah',-25.4332,142.6502,'Australia','AU','AUS','Queensland','',158,1036272226], 
['Bedourie','Bedourie',-24.3496,139.4666,'Australia','AU','AUS','Queensland','',142,1036680924], 
['Newman','Newman',-23.3666,119.7333,'Australia','AU','AUS','Western Australia','',5138,1036587511], 
['Birdsville','Birdsville',-25.8996,139.3666,'Australia','AU','AUS','Queensland','',283,1036830335], 
['Kalgoorlie','Kalgoorlie',-30.7354,121.46,'Australia','AU','AUS','Western Australia','',36852,1036087904], 
['Biloela','Biloela',-24.3936,150.4961,'Australia','AU','AUS','Queensland','',6309,1036014905], 
['Smithton','Smithton',-40.8329,145.1167,'Australia','AU','AUS','Tasmania','',4202,1036207188], 
['Bicheno','Bicheno',-41.8784,148.2886,'Australia','AU','AUS','Tasmania','',177,1036189642], 
['Deniliquin','Deniliquin',-35.5296,144.95,'Australia','AU','AUS','New South Wales','',8024,1036325219], 
['Broken Hill','Broken Hill',-31.95,141.4331,'Australia','AU','AUS','New South Wales','',17395,1036216956], 
['Swan Hill','Swan Hill',-35.3396,143.54,'Australia','AU','AUS','Victoria','',9276,1036220501], 
['Albury','Albury',-36.06,146.92,'Australia','AU','AUS','New South Wales','',104258,1036076542], 
['Wagga Wagga','Wagga Wagga',-35.1222,147.34,'Australia','AU','AUS','New South Wales','',55381,1036273188], 
['Tumut','Tumut',-35.3096,148.22,'Australia','AU','AUS','New South Wales','',6526,1036777587], 
['Lismore','Lismore',-28.8167,153.2931,'Australia','AU','AUS','New South Wales','',31430,1036024174], 
['Byron Bay','Byron Bay',-28.6565,153.6129,'Australia','AU','AUS','New South Wales','',6764,1036606974], 
['Tweed Heads','Tweed Heads',-28.1826,153.5466,'Australia','AU','AUS','New South Wales','',33065,1036571941]]
     
     

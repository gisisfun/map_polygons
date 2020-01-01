"""
File containing data set definitions
"""
class DataSets:
    """
    Data set defintions
    """

    class Australia:
        """
        ABS Australian Boundary
        """

        class ShapeFormat:
            """
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                        'zip_dir', 'zip_path')
            def __init__(self):
                self.description = 'ABS Australia'
                self.format = 'Shape'
                self.file_path = 'shapefiles{slash}AUS_2016_AUST.shp'
                self.down_url = 'http://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_aus_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&5503B37F8055BFFECA2581640014462C&0&July%202016&24.07.2017&Latest'
                self.zip_dir = 'shapefiles'
                self.zip_path = 'shapefiles{slash}1270055001_aus_2016_aust_shape.zip'

    class StatisticalAreasLevel12011:
        """
        2011 ABS Statistical Areas Level 1
        """
        class ShapeFormat:
            """
            2011 ABS Statistical Areas Level 1 in shape format
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                        'zip_dir', 'zip_path')
            def __init__(self):
                self.description = '2011 ABS Statistical Areas Level 1'
                self.format = 'Shape'
                self.file_path = 'shapefiles{slash}SA1_2011_AUST.shp'
                self.down_url = 'https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_sa1_2011_aust_shape.zip&1270.0.55.001&Data%20Cubes&24A18E7B88E716BDCA257801000D0AF1&0&July%202011&23.12.2010&Latest'
                self.zip_dir = 'shapefiles'
                self.zip_path = 'shapefiles{slash}1270055001_sa1_2011_aust_shape.zip'

    class StatisticalAreasLevel12016:
        """
        2016 ABS Statistical Areas Level 1
        """
        class ShapeFormat:
            """
            2016 ABS Statistical Areas Level 1 in shape format
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                         'zip_dir', 'zip_path')

            def __init__(self):
                self.description = '2016 ABS Statistical Areas Level 1'
                self.format = 'Shape'
                self.file_path = 'shapefiles{slash}SA1_2016_AUST.shp'
                self.down_url = 'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa1_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&6F308688D810CEF3CA257FED0013C62D&0&July%202016&12.07.2016&Latest'
                self.zip_dir = 'shapefiles'
                self.zip_path = 'shapefiles{slash}1270055001_sa1_2016_aust_shape.zip'
    class MBSP:
        """
        Round 4 Mobile Black Spot Program
        """
        class CSVFormat:
            """
            Round 4 Mobile Black Spot Program in csv format
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                        'zip_dir', 'zip_path')

            def __init__(self):
                self.description = 'mbsp database'
                self.format = 'CSV'
                self.file_path = 'csv{slash}mbsp_database.csv'
                self.down_url = 'https://data.gov.au/dataset/7be6e3ee-043a-4c47-a6eb-a97702419ccd/resource/c6b211ad-3aa2-4f53-8427-01b52a6433a7/download/mbsp_database.csv'
                self.zip_dir = 'csv'
                self.zip_path = 'csv{slash}mbsp_database.csv'

    class AGILDataset:
        """
        Australian Government Indigenous Locations Dataset (AGIL)
        """

        class CSVFormat:
            """
            Australian Government Indigenous Locations Dataset (AGIL) in csv format
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                         'zip_dir', 'zip_path')

            def __init__(self):
                self.description = 'AGIL DataSet'
                self.format = 'CSV'
                self.file_path = 'csv{slash}agil_locations20190208.csv'
                self.down_url = 'https://data.gov.au/dataset/34b1c164-fbe8-44a0-84fd-467dba645aa7/resource/625e0a41-6a30-4c11-9a20-ac64ba5a1d1f/download/agil_locations20190208.csv'
                self.zip_dir = 'csv'
                self.zip_path = 'csv{slash}agil_locations20190208.csv'

    class OpenStreetMaps:
        """
        OpenStreetMaps Sourced from ...
        """
        class ShapeFormat:
            """
            OpenStreetMaps Sourced from ... in shape file format
            """
            __slots__ = ('description', 'format', 'file_path', 'down_url', \
                         'zip_dir', 'zip_path')

            def __init__(self):
                self.description = 'OpenStreetMaps'
                self.format = 'Shape'
                self.file_path = 'shapefiles{slash}gis_osm_places_free_1.shp'
                self.down_url = 'https://download.geofabrik.de/australia-oceania/australia-latest-free.shp.zip'
                self.zip_dir = 'shapefiles'
                self.zip_path = 'shapefiles{slash}australia-latest-free.shp.zip'


    class NASAActiveFireData:
        """
        """
        class VIIRS375m:
            """
            """
            class ShapeFormat:
                """
                """
                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data VIIRS 375m'
                    self.format = 'Shape'
                    self.file_path = 'shapefiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.shp'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/shapes/zips/VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.zip'
                    self.zip_dir = 'shapefiles'
                    self.zip_path = 'shapefiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.zip'

            class CSVFormat:
                """
                """
                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data VIIRS 375 m'
                    self.format = 'CSV'
                    self.file_path = 'csv{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/text/VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'
                    self.zip_dir = 'csv'
                    self.zip_path = 'csv{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.csv'

            class KMLFormat:
                """
                """

                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data VIIRS 375m'
                    self.format = 'KML'
                    self.file_path = 'kmlfiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/kml/MODIS_C6_Australia_and_New_Zealand_24h.kml'
                    self.zip_dir = 'kmlfiles'
                    self.zip_path = 'kmlfiles{slash}VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.kml'


        class ModisC61km:
            """
            """

            class ShapeFormat:
                """
                """
                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data Modis C6 1km'
                    self.format = 'Shape'
                    self.file_path = 'shapefiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.shp'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/shapes/zips/MODIS_C6_Australia_and_New_Zealand_24h.zip'
                    self.zip_dir = 'shapefiles'
                    self.zip_path = 'shapefiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.zip'

            class CSVFormat:
                """
                """

                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data Modis C6 1km'
                    self.format = 'CSV'
                    self.file_path = 'csv{slash}MODIS_C6_Australia_and_New_Zealand_24h.csv'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_Australia_and_New_Zealand_24h.csv'
                    self.zip_dir = 'csv'
                    self.zip_path = 'csv{slash}MODIS_C6_Australia_and_New_Zealand_24h.csv'

            class KMLFormat:
                """
                """
                __slots__ = ('description', 'format', 'file_path', 'down_url', \
                             'zip_dir', 'zip_path')

                def __init__(self):
                    self.description = 'NASA Active Fire Data Modis C6 1km'
                    self.format = 'KML'
                    self.file_path = 'kmlfiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.kml'
                    self.down_url = 'https://firms.modaps.eosdis.nasa.gov/active_fire/c6/kml/MODIS_C6_Australia_and_New_Zealand_24h.kml'
                    self.zip_dir = 'kmlfiles'
                    self.zip_path = 'kmlfiles{slash}MODIS_C6_Australia_and_New_Zealand_24h.kml'


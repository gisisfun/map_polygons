#all
import os
import pandas as pd

#PostProcess
import urllib.request
from pyunpack import Archive
import sqlite3
import subprocess

from isotiles.parameters import Bounding_Box, OSVars, Offsets, DataSets, Defaults

class PostProcess():

    defaults = Defaults()

    def __init__(self,radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 metadata: Defaults = defaults.MetaDataPath,
                 tabfiles: Defaults = defaults.TabfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath,
                 geojson: Defaults = defaults.GeoJSONPath,
                 vrt: Defaults = defaults.VRTPath,
                 csv: Defaults = defaults.CSVPath,
                 spatialite: Defaults = defaults.SpatialitePath,
                 sql: Defaults = defaults.SQLPath):
        posixvars = OSVars.posix()
        ntvars = OSVars.nt()
        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.Radial = radial
        self.Shape = shape
        self.Charset = 'CP1252'

        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.ImagesPath = images
        self.MetaDataPath = metadata
        self.TabfilesPath= tabfiles
        self.ShapefilesPath = shapefiles
        self.GeoJSONPath = geojson
        self.VRTPath = vrt
        self.CSVPath = csv 
        self.SpatialitePath = spatialite
        self.SQLPath = sql
        
        my_os = str(os.name)
        if (my_os is 'posix'):
            self.Ogr2ogr = posixvars.Ogr2ogr # '/usr/bin/ogr2ogr'
            self.Slash = posixvars.Slash # '/'
            self.Extn = "SELECT load_extension('mod_spatialite.so');"
            self.Spatialite = posixvars.Spatialite
        else:
            self.Ogr2ogr = ntvars.Ogr2ogr # 'c:\\OSGeo4W64\\bin\\ogr2ogr.exe'
            self.Slash = ntvars.Slash # '\\'
            Gdal_vars = {'GDAL_DATA': 'C:\OSGeo4W64\share\gdal'}
            os.environ.update(Gdal_vars)
            self.Extn = "SELECT load_extension('mod_spatialite.dll');"
            self.Spatialite = ntvars.Spatialite

        
    def file_deploy(self,RData):
        """
        Deploy downloaded files
        
        Prerequisites:
        ref_files
        
        Input variables:
        """
        if not os.path.isfile(RData.FilePath.format(slash = self.Slash)):
            print('Downloading {descr} file in {fmt} file format'\
                  .format(fmt = RData.Format, descr = RData.Description))
            if RData.DownURL is not '':
                urllib.request.urlretrieve(RData.DownURL, RData.ZipPath.format(slash = self.Slash))
                print('Unzipping {descr} file in {fmt} file format'\
                      .format(descr = RData.Description, fmt = RData.Format ))
                Archive(RData.ZipPath.format(slash = self.Slash)).extractall(RData.ZipDir\
                                                                             .format(slash = self.Slash))
        else:
            print('{descr} file in {fmt} file format exists'\
                  .format(descr = RData.Description, fmt = RData.Format))


    def ref_files(self):
        """
        Get reference files
        Prerequisites:
        
        Input variables:
        """
        RefData = DataSets.Australia.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Australia.TabFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2011.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.Statistical_Areas_Level_1_2016.ShapeFormat()
        self.file_deploy(RefData)

        RefData = DataSets.AGIL_Dataset.CSVFormat()
        self.file_deploy(RefData)

        RefData = DataSets.OpenStreetMaps.ShapeFormat()
        self.file_deploy(RefData)


        
    def vrt_shape_and_size (self,dirname, file, newfile):
        infile = open("{dirname}{slash}{file}".\
                      format(dirname = dirname,\
                             file = file,\
                             slash=self.Slash), "r")
        infiletext = infile.read()
        infile.close()
    
        outfile = open("{dirname}{slash}{file}".\
                       format(dirname = dirname,\
                              file = newfile,\
                              slash = self.Slash),"w")
        outfiletext = infiletext.\
                      replace('57', str(self.Radial)).\
                      replace('hex', self.Shape).\
                      replace('*slash*', self.Slash)
        outfile.write(outfiletext)
        outfile.close() 
        return outfiletext


    def shape_and_size (self,dirname, file, newfile):
        infile = open("{dirname}{slash}{file}".\
                      format(dirname = dirname,\
                             file = file,\
                             slash = self.Slash), "r")
        infiletext = infile.read()
        infile.close()
    
        outfile = open("{dirname}{slash}{file}".\
                       format(dirname = dirname,\
                              file = newfile,\
                              slash = self.Slash),"w")
        outfiletext = infiletext.replace('57', str(self.Radial)).\
                      replace('hex', self.Shape).\
                      replace('/', self.Slash)
        outfile.write(outfiletext)
        outfile.close() 
        return outfiletext


    def do_spatialite (self,sqlfile, dbfile):
        db_text = '{SplitePath}{slash}{dbfile}.sqlite'.\
                  format(dbfile = dbfile,\
                         slash = self.Slash,
                         SplitePath = self.SpatialitePath)   
        sql_text = "{SplitePath}{slash}{sqlfile}".\
                   format(sqlfile = sqlfile,\
                          slash=self.Slash,
                          SplitePath = self.SpatialitePath)
        p1 = subprocess.Popen(["cat", sql_text], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([self.Spatialite, db_text], stdin= p1.stdout)
        p2.communicate()
      
        
    def geojson_to_shp (self,geojsonfile,shapefile,srid):
    
        shapefiles_text = '{SFiles}{slash}{shapefile}.shp'.\
                          format(shapefile = shapefile, \
                                 slash = self.Slash, \
                                 SFiles = self.ShapefilesPath)
        geojson_text = '{gFiles}{slash}{geojsonfile}.json'.\
                       format(geojsonfile = geojsonfile,\
                              slash = self.Slash,\
                              gfiles = self.GeoJSONPath)
        epsg_text = 'EPSG:{srid}'.format(srid=srid)  
        shp_options = [cmd_text, '-f', 'ESRI Shapefile', shapefiles_text, '-t_srs', epsg_text, geojson_text]
        try:
            # record the output!        
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')

        
    def sql_to_ogr (self,sqlfile, vrtfile, shapefile):
        print('sqlfile: {0} vrt: {1} shapefile: {2}'.format(sqlfile,vrtfile,shapefile))
        
        shapefiles_text = '{SFiles}{slash}{shapefile}.shp'.\
                          format(shapefile = shapefile,\
                                 slash = self.Slash,\
                                 SFiles = self.ShapefilesPath)
        vrt_text = '{VPath}{slash}{vrtfile}.vrt'.\
                   format(vrtfile = vrtfile,\
                          slash = self.Slash,\
                          VPath = self.VRTPath)
        sql_text = '@{SqlPath}{slash}{sqlfile}.sql'.\
                   format(sqlfile = sqlfile,\
                          slash = self.Slash, \
                          SqlPath = self.SQLPath)

        shp_options = [self.Ogr2ogr,'-f', 'ESRI Shapefile', shapefiles_text , vrt_text , \
                       '-dialect', 'sqlite','-sql', sql_text ]
        #shp_options = [options_text]
        try:
            # record the output!        
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')

        
    def sql_to_db (self,sqlfile,db):
        file  = open("{SplitePath}{slash}{file}.txt".\
                             format(db = db,\
                                    slash = self.Slash,
                                    SplitePath = self.SpatialitePath\
                                    ),"r")
        sqltext = file.read()
        file.close()
        
        thesql  = str(sqltext)
            
        subprocess.check_output(
                ["sqlite3",
                 "{Splite}{slash}{db}.sqlite".\
                 format(db = db,\
                        slash = self.Slash,\
                        Splite = self.SpatialitePath)], input=bytes(thesql.encode("utf-8")))
#        with sqlite3.connect("{SplitePath}{slash}{db}.sqlite".\
#                             format(db = db,\
#                                    slash = self.Slash,
#                                    SplitePath = self.SpatialitePath\
#                                    )) as conn:
#            conn.enable_load_extension(True)
#            c = conn.cursor()
#            c.execute(self.Extn)
#            #c.execute("SELECT InitSpatialMetaData(1)")
#            c.execute(sqltext)
#            conn.commit()

        
    def shp_to_db (self,filename, db, tblname, srid):
        with sqlite3.connect("{SplitePath}{slash}{db}.sqlite".\
                             format(db = db,\
                                    slash = self.Slash,
                                    SplitePath = self.SpatialitePath)\
                             ) as conn:
            conn.enable_load_extension(True)
            c = conn.cursor()
            c.execute(self.Extn)
            #c.execute("SELECT InitSpatialMetaData(1)")
            sql_statement="""DROP TABLE IF EXISTS "{table}";""".\
                           format(table = tblname)
            c.execute(sql_statement)
            ## LOADING SHAPEFILE
            sql_statement = """SELECT ImportSHP('{SFiles}{slash}{filename}', '{table}', '{charset}', {srid});""". \
                            format(filename = filename,\
                            table = tblname,\
                            charset = self.Charset,\
                            srid = srid,\
                            slash = self.Slash,\
                            SFiles = self.ShapefilesPath)
            c.execute(sql_statement)
            conn.commit()

        
    def csv_to_db (self,filename, db, tblname):
        cnx = sqlite3.connect('{SplitePath}{slash}{db}.sqlite'.\
                              format(db = db,\
                                     slash=self.Slash,\
                                     SplitePath = self.SpatialitePath))
        with sqlite3.connect("{SplitePath}{slash}{db}.sqlite".\
                             format(db = db,\
                                    slash = self.Slash,
                                    SplitePath = self.SpatialitePath\
                                    )) as conn:
            c = conn.cursor()
            sql_statement="""DROP TABLE IF EXISTS "{table}";""".\
                           format(table = tblname)
            c.execute(sql_statement)
            df = pd.read_csv('{csvPath}{slash}{filename}.csv'.\
                             format(filename = filename,\
                                    slash = self.Slash,\
                                    csvPath = self.CSVPath))
            df.to_sql(tblname, cnx)

        
    def cmds_to_db (self,cmdfile, db):
        db_text = '{SplitePath}{slash}{db}.sqlite'.\
                  format(db = db,\
                         slash = self.Slash,\
                         SplitePath = self.SpatialitePath)
                                                      
        cmd_text = '{vrtPath}{slash}{cmdfile}.vrt'.\
                   format(cmdfile = cmdfile,\
                          slash = self.Slash,\
                          vrtPath = self.VRTPath)
        options = [cmd_text,  db_text ,'<', cmd_text]

        try:
            # record the output!        
            subprocess.check_output(options)
            print('\ncommands successful')
        except FileNotFoundError:
            print('No commands processed')
 

    def sql_to_db (self,sqlfile, db):
        file  = open("{SplitePath}{slash}{sqlfile}.txt".\
                     format(sqlfile = sqlfile, \
                            slash=self.Slash,
                            SplitePath = SpatialitePath), "r")
        sqltext = file.read()
        file.close()
        with sqlite3.connect("{Splite}{slash}{db}.sqlite".\
                             format(db = db,\
                                    slash = self.Slash,\
                                    Splite = self.SpatialitePath)) as conn:
            conn.enable_load_extension(True)
            c = conn.cursor()
            c.execute(self.Extn)
            #c.execute("SELECT InitSpatialMetaData(1)")
            c.execute(sqltext)
            conn.commit()
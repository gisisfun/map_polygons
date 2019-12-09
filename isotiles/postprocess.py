##all
import os
import pandas as pd

#PostProcess
import sqlite3
import subprocess

from isotiles.parameters import Bounding_Box, OSVars, Offsets, Defaults

class PostProcess():

    defaults = Defaults()

    def __init__(self,radial: Defaults = defaults.Radial,
                 shape: Defaults = defaults.Shape,
                 images: Defaults = defaults.ImagesPath,
                 metadata: Defaults = defaults.MetaDataPath,
                 logfiles: Defaults = defaults.LogfilesPath,
                 kmlfiles: Defaults = defaults.KMLfilesPath,
                 shapefiles: Defaults = defaults.ShapefilesPath,
                 geojson: Defaults = defaults.GeoJSONPath,
                 vrt: Defaults = defaults.VRTPath,
                 csv: Defaults = defaults.CSVPath,
                 spatialite: Defaults = defaults.SpatialitePath,
                 sql: Defaults = defaults.SQLPath,
		 slash: Defaults = defaults.Slash,
		 ogr2ogr_com: Defaults = defaults.Ogr2ogr,
		 spatialite_com: Defaults = defaults.Spatialite,
		 extn: Defaults = defaults.Extn):

        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.Radial = radial
        self.Shape = shape
        self.Charset = 'CP1252'

        self.SpatialitePath = spatialite
        self.SQLPath = sql
        self.ImagesPath = images
        self.MetaDataPath = metadata
        self.LogfilesPath= logfiles
        self.ShapefilesPath = shapefiles
        self.KMLfilesPath= kmlfiles
        self.GeoJSONPath = geojson
        self.VRTPath = vrt
        self.CSVPath = csv 
        self.SpatialitePath = spatialite
        self.SQLPath = sql
        

        self.Ogr2ogr = ogr2ogr_com # '/usr/bin/ogr2ogr'
        self.Slash = slash # '/'
        self.Extn = extn
        self.Spatialite = spatialite_com

        
 
        
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
    
        shapefiles_text = '{sFiles}{slash}{shapefile}.shp'.\
                          format(shapefile = shapefile, \
                                 slash = self.Slash, \
                                 sFiles = self.ShapefilesPath)
        geojson_text = '{gFiles}{slash}{geojsonfile}.json'.\
                       format(geojsonfile = geojsonfile,\
                              slash = self.Slash,\
                              gFiles = self.GeoJSONPath)
        epsg_text = 'EPSG:{srid}'.format(srid=srid)  
        shp_options = [self.Ogr2ogr, '-f', 'ESRI Shapefile', shapefiles_text, '-t_srs', epsg_text, geojson_text]
        try:
            # record the output!        
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')

    def reproject_shp (self,shape_in,shape_out,srid):
    
        shape_in_text = '{SFiles}{slash}{shape_in}.shp'.\
                          format(shapefile = shape_in, \
                                 slash = self.Slash, \
                                 SFiles = self.ShapefilesPath)
        shape_out_text = '{SFiles}{slash}{shape_out}.shp'.\
                          format(shapefile = shape_out, \
                                 slash = self.Slash, \
                                 SFiles = self.ShapefilesPath)
        epsg_text = 'EPSG:{srid}'.format(srid=srid)  
        shp_options = [cmd_text, '-f', 'ESRI Shapefile', shape_out_text, '-t_srs', epsg_text, shape_in_text]
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

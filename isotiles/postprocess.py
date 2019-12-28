"""
Support module PostProcess for poly_wt.py

This code uses comnd line resources from the Gesopatial Dara Abstraction
Library (GDAL) available for Linux, Mac OS x and Windows.

This module is primarily used for adding data items to output from different
shaped regions with data to be used in the polygon mapping layer.
"""
import os
import sqlite3
import subprocess
import pandas as pd


from isotiles.parameters import Defaults

class PostProcess():
    """
    A set of methods supporting the poly_wt.py code

    Performs shell access to ogr2ogr, sqlite3 and spatialite commands
    sqlite3 module for pure sql queries
    """

    defaults = Defaults()

    def __init__(self, radial: Defaults = defaults.radial,
                 shape: Defaults = defaults.shape,
                 images: Defaults = defaults.images_path,
                 metadata: Defaults = defaults.metadata_path,
                 logfiles: Defaults = defaults.log_files_path,
                 kmlfiles: Defaults = defaults.kml_files_path,
                 shapefiles: Defaults = defaults.shape_files_path,
                 geojson: Defaults = defaults.geojson_path,
                 vrt: Defaults = defaults.vrt_files_path,
                 csv: Defaults = defaults.csv_files_path,
                 spatialite: Defaults = defaults.spatialite_path,
                 sql: Defaults = defaults.sql_files_path,
                 slash: Defaults = defaults.slash,
                 ogr2ogr_com: Defaults = defaults.ogr2ogr,
                 spatialite_com: Defaults = defaults.spatialite,
                 extn: Defaults = defaults.extn):

        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.radial = radial
        self.shape = shape
        self.charset = 'CP1252'

        self.spatialite_path = spatialite
        self.sql_files_path = sql
        self.image_files_path = images
        self.metadata_path = metadata
        self.log_files_path = logfiles
        self.shape_files_path = shapefiles
        self.kml_files_path = kmlfiles
        self.geojson_path = geojson
        self.vrt_files_path = vrt
        self.csv_files_path = csv
        self.spatialite_path = spatialite
        self.sql_files_path = sql


        self.ogr2ogr = ogr2ogr_com # '/usr/bin/ogr2ogr'
        self.slash = slash # '/'
        self.extn = "SELECT load_extension('"+extn+"');"
        self.spatialite = spatialite_com


    def vrt_shape_and_size(self, dir_name, template_file, new_file):
        """
        Customise Virtual File Format (VRT) File for shape and size

        dir_name:
        template_file:
        new_file:
        """
        file_templ = '{dirname}{slash}{file}'
        in_file = open(file_templ.\
                      format(dirname=dir_name,\
                             file=template_file,\
                             slash=self.slash), "r")
        in_file_text = in_file.read()
        in_file.close()

        outfile = open(file_templ.\
                       format(dirname=dir_name,\
                              file=new_file,\
                              slash=self.slash), "w")
        out_file_text = in_file_text.\
                      replace('57', str(self.radial)).\
                      replace('hex', self.shape).\
                      replace('*slash*', self.slash)
        outfile.write(out_file_text)
        outfile.close()
        #return out_file_text


    def shape_and_size(self, dir_name, template_file, new_file):
        """
        Customise shape and size for spatialite command files

        dir_name:
        template_file:        dir_name:
        template_file:
        new_file:
        new_file:
        """
        file_templ = '{dirname}{slash}{file}'
        in_file = open(file_templ.\
                      format(dirname=dir_name,\
                             file=template_file,\
                             slash=self.slash), "r")
        in_file_text = in_file.read()
        in_file.close()

        out_file = open(file_templ.\
                       format(dirname=dir_name,\
                              file=new_file,\
                              slash=self.slash), "w")
        out_file_text = in_file_text.replace('57', str(self.radial)).\
                      replace('hex', self.shape).\
                      replace('/', self.slash)
        out_file.write(out_file_text)
        out_file.close()
        return out_file_text


    def do_spatialite(self, sql_file, db_file):
        """
        Shell access to spatialite command to process spatialite commands

        sql_file:
        db_file:
        """
        db_text = '{SplitePath}{slash}{dbfile}.sqlite'.\
                  format(dbfile=db_file,\
                         slash=self.slash,
                         SplitePath=self.spatialite_path)
        sql_text = "{SplitePath}{slash}{sqlfile}".\
                   format(sqlfile=sql_file,\
                          slash=self.slash,
                          SplitePath=self.spatialite_path)
        process_1 = subprocess.Popen(["cat", sql_text], stdout=subprocess.PIPE)
        process_2 = subprocess.Popen([self.spatialite, db_text], \
                                     stdin=process_1.stdout)
        process_2.communicate()


    def geojson_to_shp(self, geojson_file, shape_file, srid):
        """
        Reproject geojson file to shape file using the GDAL ogr2ogr shell command

        ogr2ogr -f 'ESRI Shapefile' out.shp file.vrt -dialect sqlite -sql sql file

        geojson_file: geojson file at old projection
        shape_file: shape file at new projection
        srid: EPSG value for reprojection
        """
        shape_files_text = '{sFiles}{slash}{shapefile}.shp'.\
                          format(shapefile=shape_file, \
                                 slash=self.slash, \
                                 sFiles=self.shape_files_path)
        geojson_text = '{gFiles}{slash}{geojsonfile}.json'.\
                       format(geojsonfile=geojson_file,\
                              slash=self.slash,\
                              gFiles=self.geojson_path)
        epsg_text = 'EPSG:{srid}'.format(srid=srid)
        shp_options = [self.ogr2ogr, '-f', 'ESRI Shapefile', \
                       shape_files_text, '-t_srs', epsg_text, geojson_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')

    def reproject_shp(self, shape_in, shape_out, srid):
        """
        Reproject shape file to shape file using the GDAL ogr2ogr shell command

        ogr2ogr -f 'ESRI Shapefile' out.shp file.vrt -dialect sqlite -sql sql file

        shape_in:shape file at old projection
        shape_out: shape file at new projection
        srid: EPSG value for reprojection
        """
        shape_templ = '{SFiles}{slash}{shapefile}.shp'
        shape_in_text = shape_templ.format(shapefile=shape_in, \
                                           slash=self.slash, \
                                           SFiles=self.shape_files_path)
        shape_out_text = shape_templ.format(shapefile=shape_out, \
                                            slash=self.slash, \
                                            SFiles=self.shape_files_path)

        epsg_text = 'EPSG:{srid}'.format(srid=srid)
        shp_options = [self.ogr2ogr, '-f', 'ESRI Shapefile', shape_out_text, \
                       '-t_srs', epsg_text, shape_in_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')

    def sql_to_ogr(self, sql_file, vrt_file, shape_file):
        """
        execute SQLite code using the GDAL ogr2ogr shell command

        ogr2ogr -f 'ESRI Shapefile' out.shp file.vrt -dialect sqlite -sql sql file

        sql_file:
        vrt_file:
        shape_file:
        """
        print('sqlfile: {0} vrt: {1} shapefile: {2}'.format(sql_file, vrt_file, \
              shape_file))

        shapefiles_text = '{SFiles}{slash}{shapefile}.shp'.\
                          format(shapefile=shape_file,\
                                 slash=self.slash,\
                                 SFiles=self.shape_files_path)
        vrt_text = '{VPath}{slash}{vrtfile}.vrt'.\
                   format(vrtfile=vrt_file,\
                          slash=self.slash,\
                          VPath=self.vrt_files_path)
        sql_text = '@{SqlPath}{slash}{sqlfile}.sql'.\
                   format(sqlfile=sql_file,\
                          slash=self.slash, \
                          SqlPath=self.sql_files_path)

        shp_options = [self.ogr2ogr, '-f', 'ESRI Shapefile', shapefiles_text \
                       , vrt_text, '-dialect', 'sqlite', '-sql', sql_text]
        #shp_options = [options_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nquery successful')
        except FileNotFoundError:
            print('No files processed')


    def sql_to_db(self, sql_file, db_name):
        """
        Execute SQLite code using the sqlite3 shell command

        sqlite3 spatialite_path/db_name.sqlite < spatialite_path/sql_file.txt

        sql_file:
        db_name:
        """
        file = open("{SplitePath}{slash}{file}.txt".\
                             format(slash=self.slash,
                                    SplitePath=self.spatialite_path,\
                                    file=sql_file), "r")
        sql_text = file.read()
        file.close()

        the_sql = str(sql_text)

        subprocess.check_output( \
                                ["sqlite3", \
                                 "{Splite}{slash}{db}.sqlite".\
                                 format(db=db_name,\
                                        slash=self.slash,\
                                        Splite=self.spatialite_path)], \
                                        input=bytes(the_sql.encode("utf-8")))


    def shp_to_db(self, filename, db_name, tbl_name, srid):
        """

        db_name:
        tbl_name:
        srid:
        """
        with sqlite3.connect("{SplitePath}{slash}{db}.sqlite".\
                             format(db=db_name,\
                                    slash=self.slash,
                                    SplitePath=self.spatialite_path)\
                             ) as conn:
            conn.enable_load_extension(True)
            sql_con = conn.cursor()
            sql_con.execute(self.extn)
            #c.execute("SELECT InitSpatialMetaData(1)")
            sql_statement = """DROP TABLE IF EXISTS "{table}";""".\
                           format(table=tbl_name)
            sql_con.execute(sql_statement)
            ## LOADING SHAPEFILE
            sql_statement = """SELECT ImportSHP('{SFiles}{slash}{filename}', \
            '{table}', '{charset}', {srid});""". \
            format(filename=filename,\
                   table=tbl_name,\
                   charset=self.charset,\
                   srid=srid,\
                   slash=self.slash,\
                   SFiles=self.shape_files_path)

            sql_con.execute(sql_statement)
            conn.commit()


    def csv_to_db(self, filename, db_name, tbl_name):
        """

        db_name:
        tbl_name:
        """
        cnx = sqlite3.connect('{SplitePath}{slash}{db}.sqlite'.\
                              format(db=db_name,\
                                     slash=self.slash,\
                                     SplitePath=self.spatialite_path))
        with sqlite3.connect("{SplitePath}{slash}{db}.sqlite".\
                             format(db=db_name,\
                                    slash=self.slash,
                                    SplitePath=self.spatialite_path\
                                    )) as conn:
            sql_con = conn.cursor()
            sql_statement = """DROP TABLE IF EXISTS "{table}";""".\
                           format(table=tbl_name)
            sql_con.execute(sql_statement)
            csv_df = pd.read_csv('{csvPath}{slash}{filename}.csv'.\
                             format(filename=filename,\
                                    slash=self.slash,\
                                    csvPath=self.csv_files_path))
            csv_df.to_sql(tbl_name, cnx)


    def cmds_to_db(self, cmd_file, db_name):
        """

        cmd_file:
        db_name:
        """
        db_text = '{SplitePath}{slash}{db}.sqlite'.\
                  format(db=db_name,\
                         slash=self.slash,\
                         SplitePath=self.spatialite_path)

        cmd_text = '{vrtPath}{slash}{cmdfile}.vrt'.\
                   format(cmdfile=cmd_file,\
                          slash=self.slash,\
                          vrtPath=self.vrt_files_path)
        options = [cmd_text, db_text, '<', cmd_text]

        try:
            # record the output!
            subprocess.check_output(options)
            print('\ncommands successful')
        except FileNotFoundError:
            print('No commands processed')

    def shp_to_geojson(self, shape_file, geojson_file):
        """
        shape_file:
        geojson_file:
        """
        shape_files_text = '{sFiles}{slash}{shapefile}.shp'.\
                          format(shapefile=shape_file, \
                                 slash=self.slash, \
                                 sFiles=self.shape_files_path)
        geojson_text = '{gFiles}{slash}{geojsonfile}.json'.\
                       format(geojsonfile=geojson_file,\
                              slash=self.slash,\
                              gFiles=self.geojson_path)
        #epsg_text = 'EPSG:{srid}'.format(srid=srid)
        shp_options = [self.ogr2ogr, '-f', 'GeoJSON', geojson_text, \
                       shape_files_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nGeoJSON file processed')
        except FileNotFoundError:
            print('No files processed')

    def shp_to_kml(self, shape_file, kml_file):
        """
        shape_file:
        kml_file:
        """
        shape_files_text = '{sFiles}{slash}{shapefile}.shp'.\
                          format(shapefile=shape_file, \
                                 slash=self.slash, \
                                 sFiles=self.shape_files_path)
        kml_text = '{kFiles}{slash}{kmlfile}.kml'.\
                       format(kmlfile=kml_file,\
                              slash=self.slash,\
                              kFiles=self.kml_files_path)
        #epsg_text = 'EPSG:{srid}'.format(srid=srid)
        shp_options = [self.ogr2ogr, '-f', 'KML', kml_text, shape_files_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nKML file processed')
        except FileNotFoundError:
            print('No files processed')

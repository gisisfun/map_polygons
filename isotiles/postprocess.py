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


from isotiles.__init__ import Defaults

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
                 kmlfiles: Defaults = defaults.kml_files_path,
                 shapefiles: Defaults = defaults.shape_files_path,
                 geojson: Defaults = defaults.geojson_path,
                 vrt: Defaults = defaults.vrt_files_path,
                 csv: Defaults = defaults.csv_files_path,
                 spatialite: Defaults = defaults.spatialite_path,
                 sql: Defaults = defaults.sql_files_path):

        os.environ['SPATIALITE_SECURITY'] = 'relaxed'
        self.radial = radial
        self.shape = shape


        self.spatialite_path = spatialite
        self.sql_files_path = sql
        self.image_files_path = images
        self.shape_files_path = shapefiles
        self.kml_files_path = kmlfiles
        self.geojson_path = geojson
        self.vrt_files_path = vrt
        self.csv_files_path = csv
        self.spatialite_path = spatialite
        self.sql_files_path = sql
        my_os = str(os.name)
        if my_os == 'nt':
            gdal_vars = {'GDAL_DATA': 'C:\\OSGeo4W64\\share\\gdal'}
            os.environ.update(gdal_vars)

    @property
    def ogr2ogr(self):
        """
        Long interval to next reference point
        """
        defaults = Defaults()
        return defaults.ogr2ogr

    @property
    def slash(self):
        """
        Long interval to next reference point
        """
        defaults = Defaults()
        return defaults.slash


    @property
    def json_files_path(self):
        """
        Shape filespath
        """
        return "jsonfiles"

    @property
    def extn(self):
        """
        Long interval to next reference point
        """
        defaults = Defaults()
        return "SELECT load_extension('"+defaults.extn+"');"

    @property
    def spatialite(self):
        """
        Long interval to next reference point
        """
        defaults = Defaults()
        return defaults.spatialite

    @property
    def charset(self):
        """
        Long interval to next reference point
        """
        return 'CP1252'


    def vrt_shape_and_size(self, dir_name, template_file, new_file):
        """
        Customise Virtual File Format (VRT) File for shape and size

        dir_name:
        template_file:
        new_file:
        """
        in_file = open(dir_name+self.slash+template_file, "r")
        in_file_text = in_file.read()
        in_file.close()

        outfile = open('{}{}{}'.format(dir_name, self.slash, new_file), "w")
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
        template_file:
        new_file:
        """
        in_file = open('{}{}{}'.format(dir_name, self.slash, template_file), "r")
        in_file_text = in_file.read()
        in_file.close()

        out_file = open('{}{}{}'.format(dir_name, self.slash, new_file), "w")
        out_file_text = in_file_text.replace('57', str(self.radial))\
                        .replace('hex', self.shape)\
                        .replace('/', self.slash)
        out_file.write(out_file_text)
        out_file.close()
        return out_file_text


    def do_spatialite(self, sql_file, db_file):
        """
        Shell access to spatialite command to process spatialite commands

        sql_file:
        db_file:
        """
        db_text = '{}{}{}.sqlite'.format(self.spatialite_path, self.slash, db_file)
        sql_text = '{}{}{}'.format(self.spatialite_path, self.slash, sql_file)
        process_1 = subprocess.Popen(["cat", sql_text], stdout=subprocess.PIPE)
        try:
            process_2 = subprocess.Popen([self.spatialite, db_text], \
                                          stdin=process_1.stdout)
            process_2.communicate()
        except FileNotFoundError:
            print('spatialite executable no found')

    def geojson_to_shp(self, geojson_file, shape_file, srid):
        """
        Reproject geojson file to shape file using the GDAL ogr2ogr shell command

        ogr2ogr -f 'ESRI Shapefile' out.shp file.vrt -dialect sqlite -sql sql file

        geojson_file: geojson file at old projection
        shape_file: shape file at new projection
        srid: EPSG value for reprojection
        """
        shape_files_text = '{}{}{}.shp'.format(self.shape_files_path, 
                            self.slash, shape_file)
        geojson_text = '{}{}{}.json'.format(self.geojson_path, self.slash, 
                        geojson_file)
        epsg_text = 'EPSG:{}'.format(srid)
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
        shape_in_text = '{}{}{}.shp'.format(self.shape_files_path, self.slash, \
                         shape_in)
        shape_out_text = '{}{}{}.shp'.format(self.shape_files_path, self.slash, \
                         shape_out)

        epsg_text = 'EPSG:{}'.format(srid)
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

        shapefiles_text ='{}{}{}.shp'.format(self.shape_files_path, self.slash, \
                         shape_file)
        vrt_text = '{}{}{}.vrt'.format(self.vrt_files_path, self.slash, vrt_file)
        sql_text = '@{}{}{}.sql'.format(self.sql_files_path, self.slash, sql_file)

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
        file = open("{}{}{}.txt".format(self.spatialite_path, self.slash,
                    sql_file), "r")
        sql_text = file.read()
        file.close()

        the_sql = str(sql_text)

        subprocess.check_output( \
                                ["sqlite3", \
                                 "{}{}{}.sqlite".\
                                 format(self.spatialite_path, self.slash, 
                                        db_name)], \
                                        input=bytes(the_sql.encode("utf-8")))


    def shp_to_db(self, file_name, db_name, tbl_name, srid):
        """

        db_name:
        tbl_name:
        srid:
        """
        with sqlite3.connect("{}{}{}.sqlite".\
                             format(self.spatialite_path, self.slash, db_name)\
                             ) as conn:
            conn.enable_load_extension(True)
            sql_con = conn.cursor()
            sql_con.execute(self.extn)
            #c.execute("SELECT InitSpatialMetaData(1)")
            sql_statement = """DROP TABLE IF EXISTS "{}";""".format(tbl_name)
            sql_con.execute(sql_statement)
            ## LOADING SHAPEFILE
            sql_statement = "SELECT ImportSHP('{}{}{}', '{}', '{}', {});". \
            format(self.shape_files_path, self.slash, file_name, tbl_name,
                   self.charset,srid)

            sql_con.execute(sql_statement)
            conn.commit()


    def csv_to_db(self, file_name, db_name, tbl_name):
        """

        db_name:
        tbl_name:
        """
        cnx = sqlite3.connect('{}{}{}.sqlite'.\
                              format(self.spatialite_path, self.slash, db_name))
        with sqlite3.connect('{}{}{}.sqlite'.\
                              format(self.spatialite_path, self.slash, 
                                     db_name)) as conn:
            sql_con = conn.cursor()
            sql_statement = 'DROP TABLE IF EXISTS "{}";'.format(tbl_name)
            sql_con.execute(sql_statement)
            csv_df = pd.read_csv('{}{}{}.csv'.format(self.csv_files_path, 
                                 self.slash, file_name))
            csv_df.to_sql(tbl_name, cnx)


    def cmds_to_db(self, cmd_file, db_name):
        """

        cmd_file:
        db_name:
        """
        db_text = '{}{}{}.sqlite'.format(self.spatialite_path, self.slash, 
                   db_name)

        cmd_text = '{}{}{}.vrt'.format(self.vrt_files_path, self.slash, 
                    cmd_file)
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
        shape_files_text = '{}{}{}.shp'.format(self.shape_files_path, 
                            self.slash, shape_file)
        geojson_text = '{}{}{}.json'.format(self.geojson_path, self.slash, 
                        geojson_file)
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
        shape_files_text = '{}{}{}.shp'.format(self.shape_files_path, 
                            self.slash, shape_file)
        kml_text = '{}{}{}.kml'.format(self.kml_files_path, self.slash, 
                    kml_file)
        #epsg_text = 'EPSG:{srid}'.format(srid=srid)
        shp_options = [self.ogr2ogr, '-f', 'KML', kml_text, shape_files_text]
        try:
            # record the output!
            subprocess.check_output(shp_options)
            print('\nKML file processed')
        except FileNotFoundError:
            print('No files processed')

import sys
import os
import pandas
import sqlite3
import subprocess

def sql_to_ogr (sqlfile,vrtfile,shapefile):
    print(options_text)
    shapefiles_text = '../shapefiles/{shapefile}.shp'.format(shapefile=shapefile)
    vrt_text = '../vrt/{vrtfile}.vrt'.format(vrtfile=vrtfile)
    sql_text = '@../sql/{sqlfile}.sql'.format(sqlfile=sqlfile)
    shp_options = ['/usr/bin/ogr2ogr','-f', 'ESRI Shapefile', shapefiles_text , vrt_text , '-dialect', 'sqlite','-sql', sql_text ]
    #shp_options = [options_text]
    try:
        # record the output!        
        subprocess.check_output(shp_options)
        print('\nquery successful')
    except FileNotFoundError:
        print('No files processed')

def sql_to_db (sqlfile,db):
    file  = open("../spatialite_db/{file}.txt".format(file=sqlfile), "r")
    sqltext = file.read()
    file.close()
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        c.execute(sqltext)
        conn.commit()

def shp_to_db (filename,db,tblname,srid):
    os.environ['SPATIALITE_SECURITY']='relaxed'
    charset = 'CP1252'
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        ## LOADING SHAPEFILE
        sql_statement="""SELECT ImportSHP('../shapefiles/{filename}', '{table}', '{charset}', {srid});""".format(filename=filename, table=tblname, charset=charset, srid=srid)
        c.execute(sql_statement)
        conn.commit()

def csv_to_db (filename, db, tblname):
    cnx = sqlite3.connect('../spatialite_db/{db}.sqlite'.format(db='db'))
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        c = conn.cursor()
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        df = pandas.read_csv('../csv/{filename}.csv'.format(filename=filename))
        df.to_sql(tblname , cnx)
import sys
import os
import pandas
import sqlite3
import subprocess

def sql_to_ogr (sqlfile,vrtfile,shapefile):
    options_text = "/usr/bin/ogr2ogr -f 'ESRI Shapefile' ../shapefiles/{shapefile}.shp '../vrt/{vrtfile}.vrt' -dialect sqlite -sql @../sql/{sqlfile}.sql".format(sqlfile=sqlfile,vrtfile=vrtfile,shapefile=shapefile)
    print(options_text)
    shapefiles_text = '../shapefiles/{shapefile}.shp'.format(shapefile=shapefile)
    vrt_text = '../vrt/{vrtfile}.vrt'.format(vrtfile=vrtfile)
    sql_text = '@../sql/{sqlfile}.sql'.format(sqlfile=sqlfile)
    shp_options = ['/usr/bin/ogr2ogr','-f', 'ESRI Shapefile', shapefiles_text , vrt_text , '-dialect', 'sqlite','-sql', sql_text ]
    #shp_options = [options_text]
    try:
        # record the output!
        
        subprocess.check_output(shp_options)
        print('\nquery successful')
    except FileNotFoundError:
        print('No files processed')
    
def sql_to_db (sqlfile,db):
    file  = open("../spatialite_db/{file}.txt".format(file=sqlfile), "r")
    sqltext = file.read()
    file.close()
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        c.execute(sqltext)
        conn.commit()

def shp_to_db (filename,db,tblname,srid):
    os.environ['SPATIALITE_SECURITY']='relaxed'
    charset = 'CP1252'
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        ## LOADING SHAPEFILE
        sql_statement="""SELECT ImportSHP('../shapefiles/{filename}', '{table}', '{charset}', {srid});""".format(filename=filename, table=tblname, charset=charset, srid=srid)
        c.execute(sql_statement)
        conn.commit()

def csv_to_db (filename, db, tblname):
    cnx = sqlite3.connect('../spatialite_db/{db}.sqlite'.format(db='db'))
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        c = conn.cursor()
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        df = pandas.read_csv('../csv/{filename}.csv'.format(filename=filename))
        df.to_sql(tblname , cnx)

#ogr2ogr ../shapefiles/aust_hex_shape_57km.shp '../vrt/aust_shape.vrt' -dialect sqlite -sql @../sql/aust_shape.sql
sql_to_ogr('aust_shape','aust_shape','aust_hex_shape_57km')
shp_to_db('aust_hex_shape_57km','db')

sql_to_ogr('feat_aust_11','feat_aust_11','feat_aust_57km_sa1_11')
shp_to_db('feat_aust_57km_sa1_11','db')

sql_to_ogr('feat_aust_16','feat_aust_16','feat_aust_57km_sa1_16')
shp_to_db('feat_aust_57km_sa1_16','db')


#sql_to_ogr('feat_aust_11','feat_aust_11','feat_aust_57km_sa1_11')
#shp_to_db('feat_aust_57km_sa1_11','db')
#
#sql_to_ogr('feat_aust_16','feat_aust_16','feat_aust_57km_sa1_16')
#shp_to_db('feat_aust_57km_sa1_16','db')
#
#csv_to_db('2011Census_B18_AUST_SA1_long','db','2011Census_B18_AUST_SA1_long')
#csv_to_db('2011Census_B21_AUST_SA1_long','db','2011Census_B21_AUST_SA1_long')
#csv_to_db('2011Census_B22_AUST_SA1_long','db','2011Census_B22_AUST_SA1_long')
#sql_to_db('donor_feat_11_B18_B21_B22','db')
#
#csv_to_db('2011Census_G18_AUST_SA1','db','2011Census_G18_AUST_SA1')
#csv_to_db('2011Census_G21_AUST_SA1','db','2011Census_G21_AUST_SA1')
#csv_to_db('2011Census_G22_AUST_SA1','db','2011Census_G22_AUST_SA1')
#sql_to_db('donor_feat_16_G18_G21_G22','db')
#
#sql_to_ogr('shape_donor_feat_57km_agil_count','shape_agil','shape_agil_count')
#sql_to_ogr('shape_donor_feat_57km_mbsp_count','shape_mbsp','shape_mbsp_count')
#sql_to_ogr('shape_donor_feat_57km_place_count','shape_place','shape_place_count')
#sql_to_ogr('shape_donor_feat_57km_agil_count','shape_agil','shape_agil_count')
#sql_to_ogr('shape_donor_feat_57km_road_count','shape_road','shape_road_count')
#sql_to_ogr('shape_donor_feat_57km_bstation_count','shape_pois','shape_bstation_count')
#sql_to_ogr('shape_donor_feat_57km_service_count','shape_pois','shape_services_count')
#sql_to_ogr('shape_57km_area_11_16','shape_11_16','shape_11_16_area')
#sql_to_ogr('shape_57km_place_11_16','shape_11_16','place_11_16_place')

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (fytpe,filename, db, tblname,srid) = ['csv','test', 'db', 'test',-1,]
    #csv_to_db(fytpe,filename, db, tblname)
    #(fytpe,filename, db, tblname,srid,sqltext) = ['shp','hex_57km_layer', 'db', 'hex_57km_layer',4283]
    #shp_to_db(filename, db, tblname,srid)
    (fytpe,filename, db, tblname,srid) = ['sql','test', 'db', 'test',-1]
    sql_to_db(filename, db)
else:
    if (len(sys.argv) <7 ):
        sys.exit("arguments are \nftype \n filename\n db \n tblname \n srid ")
    else:
        (blah,filename, db, tblname,srid,sqlfile) = sys.argv
        if ftype == "csv":
            csv_to_db(filename, db, tblname)
        else:
            if ftype == "shp":
                shp_to_db(filename, db, tblname,srid)
            else:
                if ftype == "sql":
                    sql_to_db(filename, db)
                else:
                    print('ftype is csv ,shp or sql')

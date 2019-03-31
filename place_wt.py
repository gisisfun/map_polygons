import sys
import os
import pandas
import sqlite3
import subprocess

def shape_and_size (dir,file,shape,size,newfile):
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    infile  =  open("{dir}{slash}{file}".format(dir=dir,file=file,slash=slash), "r")
    infiletext = infile.read()
    infile.close()
    
    outfile = open("{dir}{slash}{file}".format(dir=dir,file=newfile,slash=slash),"w")
    outfiletext = infiletext.replace('57',size).replace('hex',shape).replace('/',slash)
    outfile.write(outfiletext)
    outfile.close() 
    return outfiletext

def do_spatialite (sqlfile,dbfile):
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
        
    sql_text = "spatialite_db{slash}{sqlfile}.txt".format(sqlfile=sqlfile,slash=slash)
    p1 = subprocess.Popen(["cat", sql_text], stdout=subprocess.PIPE)
    db_text = 'spatialite_db{slash}{dbfile}.sqlite'.format(dbfile=dbfile,slash=slash)
    p2 = subprocess.Popen(["spatialite", db_text], stdin=p1.stdout)
    p2.communicate()
      
def geojson_to_shp (geojsonfile,shapefile,srid):
    #print(options_text)
    if (os.name is 'posix'):
        cmd_text='/usr/bin/ogr2ogr'
        slash='/'
    else:
        cmd_text='ogr2ogr.exe'
        slash='\/'
    
    shapefiles_text = 'shapefiles{slash}{shapefile}.shp'.format(shapefile=shapefile,slash=slash)
    geojson_text = 'geojson{slash}{geojsonfile}.json'.format(geojsonfile=geojsonfile,slash=slash)
    epsg_text = 'EPSG:{srid}'.format(srid=srid)  
    shp_options = [cmd_text,'-f', 'ESRI Shapefile',shapefiles_text, '-t_srs', epsg_text, geojson_text]
    try:
        # record the output!        
        subprocess.check_output(shp_options)
        print('\nquery successful')
    except FileNotFoundError:
        print('No files processed')

def sql_to_ogr (sqlfile,vrtfile,shapefile):
    print('sqlfile: {0} vrt: {1} shapefile: {2}'.format(sqlfile,vrtfile,shapefile))
    if (os.name is 'posix'):
        cmd_text='/usr/bin/ogr2ogr'
        slash='/'
    else:
        cmd_text='ogr2ogr.exe'
        slash='\/'
    shapefiles_text = 'shapefiles{slash}{shapefile}.shp'.format(shapefile=shapefile,slash=slash)
    vrt_text = 'vrt{slash}{vrtfile}.vrt'.format(vrtfile=vrtfile,slash=slash)
    sql_text = '@sql{slash}{sqlfile}.sql'.format(sqlfile=sqlfile,slash=slash)

    shp_options = [cmd_text,'-f', 'ESRI Shapefile', shapefiles_text , vrt_text , '-dialect', 'sqlite','-sql', sql_text ]
    #shp_options = [options_text]
    try:
        # record the output!        
        subprocess.check_output(shp_options)
        print('\nquery successful')
    except FileNotFoundError:
        print('No files processed')

def sql_to_db (sqlfile,db):
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    file  = open("spatialite_db{slash}{file}.txt".format(file=sqlfile,slash=slash), "r")
    sqltext = file.read()
    file.close()
    with sqlite3.connect("spatialite_db{slash}{db}.sqlite".format(db=db,slash=slash)) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        c.execute(sqltext)
        conn.commit()

def shp_to_db (filename,db,tblname,srid):
    os.environ['SPATIALITE_SECURITY']='relaxed'
    charset = 'CP1252'
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    with sqlite3.connect("spatialite_db{slash}{db}.sqlite".format(db=db,slash=slash)) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        ## LOADING SHAPEFILE
        sql_statement="""SELECT ImportSHP('shapefiles{slash}{filename}', '{table}', '{charset}', {srid});""".format(filename=filename, table=tblname, charset=charset, srid=srid, slash=slash)
        c.execute(sql_statement)
        conn.commit()

def csv_to_db (filename, db, tblname):
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    cnx = sqlite3.connect('spatialite_db{slash}{db}.sqlite'.format(db=db,slash=slash))
    with sqlite3.connect("spatialite_db{slash}{db}.sqlite".format(db=db,slash=slash)) as conn:
        c = conn.cursor()
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
        c.execute(sql_statement)
        df = pandas.read_csv('csv{slash}{filename}.csv'.format(filename=filename,slash=slash))
        df.to_sql(tblname , cnx)

def cmds_to_db (cmdfile,db):
    #print(options_text)
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    db_text = 'db{slash}{db}.sqlite'.format(db=db,slash=slash)
    cmd_text = 'vrt{slash}{cmdfile}.vrt'.format(cmdfile=cmdfile,slash=slash)
    if os.name is 'posix':
        cmd_text='spatialite'
    else:
        cmd_text='spatialite.exe'
    options = [cmd_text,  db_text ,'<', cmd_text]
    #shp_options = [options_text]
    try:
        # record the output!        
        subprocess.check_output(options)
        print('\ncommands successful')
    except FileNotFoundError:
        print('No commands processed')
    
def sql_to_db (sqlfile,db):
    if (os.name is 'posix'):
        slash='/'
    else:
        slash='\/'
    file  = open("spatialite_db{slash}{sqlfile}.txt".format(sqlfile=sqlfile,slash=slash), "r")
    sqltext = file.read()
    file.close()
    with sqlite3.connect("spatialite_db{slash}{db}.sqlite".format(db=db,slash=slash)) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        c.execute(sqltext)
        conn.commit()

def process_sql(shape,size,db):
#    size='57'
#    shape='hex'
    shape_and_size ('vrt','template.vrt',shape,size,'all.vrt')
    print('aust_shape')
    fname='aust_{shape}_shape_{size}km'.format(shape=shape,size=size)
    sql_to_ogr('aust_shape','all',fname)
    shp_to_db(fname,'db',fname,4823)
    
    print('feat_aust_11_area')
    fname='feat_aust_{size}km_sa1_11'.format(shape=shape,size=size)
    sql_to_ogr('feat_aust_11','all',fname)
    shp_to_db(fname,'db',fname,4823)
    
    print('feat_aust_16_area')
    fname='feat_aust_{size}km_sa1_16'.format(shape=shape,size=size)
    sql_to_ogr('feat_aust_16','all',fname)
    shp_to_db(fname,'db',fname,4823)
    
    print('tabular_place_wt')   
    csv_to_db('2011Census_B18_AUST_SA1_long','db','2011Census_B18_AUST_SA1_long')
    csv_to_db('2011Census_B21_AUST_SA1_long','db','2011Census_B21_AUST_SA1_long')
    csv_to_db('2011Census_B22B_AUST_SA1_long','db','2011Census_B22B_AUST_SA1_long')
    csv_to_db('2016Census_G18_AUS_SA1','db','2016Census_G18_AUS_SA1')
    csv_to_db('2016Census_G21_AUS_SA1','db','2016Census_G21_AUS_SA1')
    csv_to_db('2016Census_G22B_AUS_SA1','db','2016Census_G22B_AUS_SA1')
    fname='aust_{shape}_shape_{size}km'.format(shape=shape,size=size)
    shp_to_db(fname,'db',fname,4823)
    fname='feat_aust_{size}km_sa1_11'.format(shape=shape,size=size)
    shp_to_db(fname,'db',fname,4823)
    fname='feat_aust_{size}km_sa1_16'.format(shape=shape,size=size)
    shp_to_db(fname,'db',fname,4823)
    shp_to_db('gis_osm_places_free_1','db','gis_osm_places_free_1',4823)
    shp_to_db('gis_osm_roads_free_1','db','gis_osm_roads_free_1',4823)
    sql_to_ogr('shape_pois_shp','all','POI')
    shp_to_db('POI','db','POI',4823)
    geojson_to_shp ('AGIL','agil',4823)
    shp_to_db('agil','db','agil',4823)
    sql_to_ogr('shape_mbsp_shp','all','mbsp')
    shp_to_db('mbsp','db','mbsp',4823)

    sqlname='tabular_place_wt.txt'
    shape_and_size ('spatialite_db','tabular_place_wt.txt',shape,size,sqlname)
    do_spatialite(sqlname,'db')
    
    # spatialite ../spatialite_db/db.sqlite "vacuum;"
    
    
    #print('shape_11_16_area')
    #fname='shape_{size}km_area_11_16'.format(shape=shape,size=size)
    #sql_to_ogr('shape_11_16_area','all',fname)

    #print('shape_11_16_place')
    #fname='shape_{size}km_place_11_16'.format(shape=shape,size=size)
    #sql_to_ogr('shape_11_16_place','all',fname)

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (shape,size,db) = ['hex','57','db']
    process_sql(shape,size,db)
else:
    if (len(sys.argv) <4 ):
        sys.exit("arguments are \nshape \n size (km)\n db \ndatabase \n srid ")
    else:
        (blah,shape,size,db) = sys.argv
        process_sql(shape,size,db)

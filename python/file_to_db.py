import sys
import os
import pandas
import sqlite3

def sql_to_db (sqlfile,db):
    file  = open("../spatialite_db/test.txt", "r")
    sqltext = file.read()
    file.close()
    with sqlite3.connect("../spatialite_db/{db}.sqlite".format(db='db')) as conn:
        conn.enable_load_extension(True)
        c = conn.cursor()
        c.execute("SELECT load_extension('mod_spatialite')")
        #c.execute("SELECT InitSpatialMetaData(1)")
        sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=tblname)
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

print('Number of arguments: {0} arguments.'.format(len(sys.argv)))
print('Argument List: {0}'.format(str(sys.argv)))
if len(sys.argv) is 1:
    (fytpe,filename, db, tblname,srid,sqltext) = ['shp','hex_57km_layer', 'db', 'hex_57km_layer',4283,'']
    #csv_to_db(fytpe,filename, db, tblname)
    shp_to_db(filename, db, tblname,srid)
    
else:
    if (len(sys.argv) <7 ):
        sys.exit("arguments are \nftype \n filename\n db \n tblname \n srid \n sqlfile \n")
    else:
        (blah,filename, db, tblname,srid,sqlfile) = sys.argv
        if ftype == "csv":
            csv_to_db(filename, db, tblname)
        else:
            if shape == "shp":
                shp_to_db(filename, db, tblname,srid)
            else:
                if shape == "sql":
                sql_to_db(sqlfile, db)
                    else:
                        print('ftype is csv ,shp or sql')


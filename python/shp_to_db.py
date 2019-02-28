import os
import sqlite3
## LOADING EXTENSION SPATIALITE
os.environ['SPATIALITE_SECURITY']='relaxed'

filename = r'../shapefiles/hex_57km_layer'
table = 'hex_57km_layer'
charset = 'CP1252'
srid = 4283

with sqlite3.connect("../spatialite_db/db.sqlite") as conn:
    conn.enable_load_extension(True)
    c = conn.cursor()
    c.execute("SELECT load_extension('mod_spatialite')")
    c.execute("SELECT InitSpatialMetaData(1)")
    sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=table)
    c.execute(sql_statement)

## LOADING SHAPEFILE
    
    sql_statement="""SELECT ImportSHP('{filename}', '{table}', '{charset}', {srid});""".format(filename=filename, table=table, charset=charset, srid=srid)
    c.execute(sql_statement)
    conn.commit()
    
    
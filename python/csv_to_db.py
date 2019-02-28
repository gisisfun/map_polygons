import pandas
import sqlite3
table='test'
cnx = sqlite3.connect('../spatialite_db/db.sqlite')
with sqlite3.connect("../spatialite_db/db.sqlite") as conn:
    c = conn.cursor()
    sql_statement="""DROP TABLE IF EXISTS "{table}";""".format(table=table)
    c.execute(sql_statement)
df = pandas.read_csv('../csv/test.csv')
df.to_sql('test' , cnx)
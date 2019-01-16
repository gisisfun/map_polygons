import pandas
import sqlite3
cnx = sqlite3.connect('db.sqlite')
df = pandas.read_csv('feat_aust_57km_sa1_16.csv')
df.to_sql('feat_aust_57km_sa1_16' , cnx)
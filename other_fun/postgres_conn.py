#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 07:50:30 2021

@author: me
"""
#https://stackoverflow.com/questions/18708050/bulk-insert-list-values-with-sqlalchemy-core
#https://stackoverflow.com/questions/3659142/bulk-insert-with-sqlalchemy-orm
#https://docs.sqlalchemy.org/en/14/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow
#https://github.com/qapn/gnaf-importer/blob/master/import_gnaf.py

import psycopg2
def query(conn,sql_st):
    cur = conn.cursor()
    cur.execute(sql_st)
    conn.commit()
    one = cur.fetchone()
    all = cur.fetchall()
    print(all,one)
    #close resources
    cur.close()
    conn.close()
    
    

    
conn = psycopg2.connect("host=localhost dbname=testdb user=postgres password=")    

query(conn, "DROP TABLE IF EXISTS users CASCADE")

sql_st = """CREATE TABLE users(
    id integer PRIMARY KEY,
    email text,
    name text,
    address text
)"""    
query(conn,sql_st)


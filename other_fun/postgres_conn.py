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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 07:50:30 2021

@author: me
"""
import psycopg2


connection = psycopg2.connect("host=localhost dbname=testdb user=postgres password=database")


def query(conn,sql_st):
    cur = conn.cursor()
    cur.execute(sql_st)
    conn.commit()
    #one = cur.fetchone()
    #all = cur.fetchall()
    #print(all,one)
    #close resources
    cur.close()
    

query(connection, "DROP TABLE IF EXISTS ADDRESS_DETAIL CASCADE")

sql_st = """CREATE TABLE ADDRESS_DETAIL (
 address_detail_pid varchar(15) NOT NULL,
 date_created date NOT NULL,
 date_last_modified date,
 date_retired date,
 building_name varchar(200),
 lot_number_prefix varchar(2),
 lot_number varchar(5),
 lot_number_suffix varchar(2),
 flat_type_code varchar(7),
 flat_number_prefix varchar(2),
 flat_number numeric(5),
 flat_number_suffix varchar(2),
 level_type_code varchar(4),
 level_number_prefix varchar(2),
 level_number numeric(3),
 level_number_suffix varchar(2),
 number_first_prefix varchar(3),
 number_first numeric(6),
 number_first_suffix varchar(2),
 number_last_prefix varchar(3),
 number_last numeric(6),
 number_last_suffix varchar(2),
 street_locality_pid varchar(15),
 location_description varchar(45),
 locality_pid varchar(15) NOT NULL,
 alias_principal char(1),
 postcode varchar(4),
 private_street varchar(75),
 legal_parcel_id varchar(20),
 confidence numeric(1),
 address_site_pid varchar(15) NOT NULL,
 level_geocoded_code numeric(2) NOT NULL,
 property_pid varchar(15),
 gnaf_property_pid varchar(15),
 primary_secondary varchar(1))"""    
query(connection,sql_st)




SQL_STATEMENT = """
    COPY %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS '|'
    """
    


def process_file(conn, table_name, file_object):
    cursor = conn.cursor()
    cursor.copy_expert(sql=SQL_STATEMENT % table_name, file=file_object)
    conn.commit()
    cursor.close()
    
my_file = open("ACT_ADDRESS_DETAIL_psv.psv")   
process_file(connection, 'ADDRESS_DETAIL', my_file)

my_file = open("NSW_ADDRESS_DETAIL_psv.psv")   
process_file(connection, 'ADDRESS_DETAIL', my_file)


connection.close()

#ogr2ogr -f PostgreSQL PG:"host=localhost user=postgres dbname=postgres password=password"  docs.csv -oo AUTODETECT_TYPE=YES

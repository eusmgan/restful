#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import psycopg2
import sys
 
 
con = None
 
try:
    con = psycopg2.connect("host='localhost' dbname='parcelflow' user='postgres' password='postgres'")   
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL, username text, password text)")
    cur.execute("CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)")
    con.commit()
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
 
    print 'Error %s' % e    
    sys.exit(1)
 
finally:   
    if con:
        con.close()

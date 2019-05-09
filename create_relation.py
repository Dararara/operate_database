import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
user = input('tell me the user name')
dbname = input('tell me the database name')
password = input('tell me the password of database')
host = input('tell me the host')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host = host)
cur = conn.cursor()

path = input('tell me the path of csv')
csvfile = open(path)
reader = csv.DictReader(csvfile)
for row in reader:
    try:
        id1 = find_id(cur, row['table1_id'], row['table1'], row['table1_match_term'], row['table1_value'])
        id2 = find_id(cur, row['table2_id'], row['table2'], row['table2_match_term'], row['table2_value'])
        insert_double_value(cur, row['relation_table'], row['table1_id'], id1, row['table2_id'], id2)
    except Exception as e:
        print(e)
    conn.commit()
cur.close()
conn.close()

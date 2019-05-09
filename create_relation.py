import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
conn = login()
cur = conn.cursor()

path = input('tell me the path of csv: ')
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

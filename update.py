import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
conn = login()
cur = conn.cursor()

path = input('please input path of update csv: ')
csvfile = open(path)
reader = csv.DictReader(csvfile)
for row in reader:
    string = 'update {} set {} = %s where {} = %s'
    cur.execute(sql.SQL(string).format(sql.Identifier(row['table_name']), sql.Identifier(row['term_name']), sql.Identifier(row['condition_name'])), [row['update_value'], row['update_condition']])

conn.commit()
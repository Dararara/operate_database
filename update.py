import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
user = input('tell me the user name')
dbname = input('tell me the database name')
password = input('tell me the password of database')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host = "122.152.251.171")
cur = conn.cursor()

path = input('please input path of update csv')
csvfile = open(path)
reader = csv.DictReader(csvfile)
for row in reader:
    string = 'update {} set {} = %s where {} = %s'
    cur.execute(sql.SQL(string).format(sql.Identifier(row['table_name']), sql.Identifier(row['term_name']), sql.Identifier(row['condition_name'])), [row['update_value'], row['update_condition']])

conn.commit()
import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
user = input('tell me the user name')
dbname = input('tell me the database name')
password = input('tell me the password of database')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host = "122.152.251.171")
cur = conn.cursor()

i = 0
servent_id = ''
while i < 3:
    temp = input('tell me which servent you want to delete from database')
    if temp == 'q':
        exit(1)
    elif temp == servent_id:
        i += 1
    else:
        servent_id = temp
        i = 0
try:
    delete_servent(cur, 'servent_and_class', 'servent_id', servent_id)
    delete_servent(cur, 'servent_and_alignment', 'servent_id', servent_id)
    delete_servent(cur, 'servent_and_illustrator', 'servent_id', servent_id)
    delete_servent(cur, 'servent_and_prototype', 'servent_id', servent_id)
    delete_servent(cur, 'servent_and_voice_actor', 'servent_id', servent_id)
    delete_servent(cur, 'servent_bond', 'servent_id', servent_id)
    delete_servent(cur, 'servent_full_pic', 'servent_id', servent_id)
    delete_servent(cur, 'servent_profile_pic', 'servent_id', servent_id)
    delete_servent(cur, 'servent', 'servent_id', servent_id)
except Exception as e:
    print(e)
conn.commit()
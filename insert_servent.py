import csv
import psycopg2
from psycopg2 import sql
from check_insert import *

conn = login()
cur = conn.cursor()
path = input('tell me the path of csv: ')
csvfile = open(path)
reader = csv.DictReader(csvfile)

def insert_servent(row):
    string = 'insert into servent (servent_id, servent_name, servent_name_japanese, servent_name_english, height, weight,gender, strength,endurance, agility, mana, luck, noble_phantasm, craft_name, craft_description, craft_src) values (%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );'
    data = ('servent', 'servent_id', 'servent_name', 'servent_name_japanese', 'servent_name_english', 'height', 'weight','gender', 'strength',
            'endurance', 'agility', 'mana', 'luck', 'noble_phantasm', 'craft_name', 'craft_description', 'craft_src')
    k = [row['no'], row['servent_name'], row['servent_name_jap'], row['servent_name_eng'], int(row['height']), int(row['weight']), row['gender'], row['strength'],
            row['endurance'], row['agility'], row['mana'], row['luck'], row['noble_phantasm'], row['craft_name'], row['craft_description'], row['craft_src']]
    cur.execute(string, k)

def insert_bond(servent_id, bond):
    try:
        cur.execute('select max(bond_id) from servent_bond where servent_id = %s;', [servent_id])
        bond_id = cur.fetchone()[0]
        print(bond_id)
        if(bond_id == None):
            print(bond_id)
            bond_id = 1
        else:
            bond_id+=1
        string = 'insert into servent_bond (servent_id, bond_id, bond_text) values(%s,%s, %s);'
        cur.execute(string,[servent_id, bond_id, bond] )
    except Exception as e:
        print(e)
def insert_profile_pic(servent_id, profile_pic, full_pic):
    try:
        string = 'insert into servent_profile_pic (servent_id, profile_pic_id, profile_pic) values (%s, %s, %s);'
        cur.execute(string, [servent_id, 1, profile_pic])
        string = 'insert into servent_full_pic(servent_id, full_pic_id, servent_picture) values (%s, %s, %s);'
        cur.execute(string, [servent_id, 1, full_pic])
    except Exception as e:
        print(e)


def create_relation(row):
    try:
        class_id = find_id(cur, 'class_id', 'class', 'class_name', row['servent_class'])
        print(class_id)

        alignment_id = find_id(cur, 'alignment_id', 'alignment', 'alignment_name', row['alignment'])
        print(alignment_id)

        origin_id = find_id(cur, 'origin_id', 'origin', 'origin_name', row['origin'])
        print(origin_id)

        region_id = find_id(cur, 'region_id', 'region', 'region_name', row['region'])
        print(region_id)

        voice_actor_id = find_id(cur, 'voice_actor', 'voice_actor', 'voice_actor', row['voice_actor'])
        print(voice_actor_id)

        illustrator_id = find_id(cur, 'illustrator_id', 'illustrator', 'illustrator_name', row['illustrator'])
        print(illustrator_id)

        prototype_id = find_id(cur, 'prototype_id', 'prototype', 'prototype_name', row['prototype'])
        print(prototype_id)

        servent_id = row['no']
        print(servent_id)
        insert_double_value(cur, 'prototype_and_origin', 'prototype_id', prototype_id, 'origin_id', origin_id)
        insert_double_value(cur, 'prototype_and_region', 'prototype_id', prototype_id, 'region_id', region_id)
        insert_double_value(cur, 'servent_and_alignment', 'servent_id', servent_id, 'alignment_id', alignment_id)
        insert_double_value(cur, 'servent_and_class', 'servent_id', servent_id, 'class_id', class_id)
        insert_double_value(cur, 'servent_and_illustrator', 'servent_id', servent_id, 'illustrator_id', illustrator_id)
        insert_double_value(cur, 'servent_and_prototype', 'servent_id', servent_id, 'prototype_id', prototype_id)
        insert_double_value(cur, 'servent_and_voice_actor', 'servent_id', servent_id, 'voice_actor_id', voice_actor_id)
        print('hello')


    except Exception as e:
        print(e)

def insert(row):
    ans = check_single_exist(cur, 'servent', 'servent_name', row['servent_name'])
    print(row['servent_name'] + '' + str(ans))
    if ans:
        return
    if not ans:
        insert_servent(row)
        insert_profile_pic(row['no'], row['profile_src'], row['full_pic_src'])
        for i in range(1, 8):
            t = 'bond' + str(i)
            insert_bond(row['no'], row[t])
    insert_single_value(cur, 'region', 'region_name', row['region'])
    insert_single_value(cur, 'origin', 'origin_name', row['origin'])
    insert_single_value(cur, 'prototype', 'prototype_name', row['prototype'])
    insert_single_value(cur, 'illustrator', 'illustrator_name', row['illustrator'])
    insert_single_value(cur, 'voice_actor', 'voice_actor_name', row['voice_actor'])
    insert_single_value(cur, 'alignment', 'alignment_name', row['alignment'])
    create_relation(row)


for row in reader:
    insert(row)

conn.commit()
csvfile.close()
conn.close()
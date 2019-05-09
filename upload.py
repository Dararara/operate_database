import csv
import psycopg2
from psycopg2 import sql
from check_insert import *
user = input('tell me the user name')
dbname = input('tell me the database name')
password = input('tell me the password of database')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host = "122.152.251.171")
cur = conn.cursor()


type = input("tell me which you want to upload(book/article)")
if type == 'book' or type == 'article':
    path = input('tell me the path of csv file')
    try:
        csvfile = open(path)
        reader = csv.DictReader(csvfile)
        for row in reader:
            if type == 'book':
                insert_double_value(cur, 'book', 'book_name', row['book_name'], 'isbn', row['isbn'])
                insert_single_value(cur, 'writer', 'writer_name', row['writer_name'])
                writer_id = find_id(cur, 'writer_id','writer','writer_name',row['writer_name'])
                book_id = find_id(cur, 'book_id', 'book', 'book_name', row['book_name'])
                insert_double_value(cur, 'book_and_writer', 'book_id', book_id, 'writer_id', writer_id)


            elif type == 'article':
                string = 'insert into article(article_title, article_content) values (%s, %s);'
                cur.execute(string, [row['article_title'], row['article_content']])
                string = 'select  exists(select * from author where author_name = %s);'
                cur.execute(string, [row['author_name']])

                if (not cur.fetchone()[0]):
                    string = 'insert into writer(author_name) values (%s);'
                    cur.execute(string, [row['author_name']])


                author_id = find_id(cur, 'author_id', 'author', 'author_name', row['author_name'])

                string = 'select article_id from article where article_title = %s;'
                cur.execute(string, [row['article_title']])
                article_id = cur.fetchone()[0]
                insert_double_value(cur, 'author_and_article', 'author_id', author_id, 'article_id', article_id)

        conn.commit()







    except Exception as e:
        print(e)



else:
    print('input false')
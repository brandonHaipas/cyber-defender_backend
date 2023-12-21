import os
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
        host="localhost",
        database="cyberdefender",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute("SELECT COUNT(table_name) FROM information_schema.tables WHERE table_name = 'grupos_telegram';")

if cur.fetchone()[0] == 0:
    cur.execute('CREATE TABLE grupos_telegram (id_grupo serial PRIMARY KEY, '
                                 'nombre varchar (150) NOT NULL, '
                                 'tags_responsables varchar[]);'
                                 )

conn.commit()

cur.close()
conn.close()
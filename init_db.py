import sqlite3

conn = sqlite3.connect('repertoire.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS "CONTACT"("id" INT, "first_name" TEXT, "last_name" TEXT, "tel" TEXT, PRIMARY KEY("id"))')

conn.commit()

cur.close()
conn.close()

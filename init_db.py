import sqlite3

conn = sqlite3.connect('repertoire.db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS "CONTACT"("id" INTEGER PRIMARY KEY AUTOINCREMENT, "first_name" TEXT, "last_name" TEXT, "tel" TEXT)')

conn.commit()

cur.close()
conn.close()

import sqlite3

conn = sqlite3.connect('repertoire.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS CONTACT(id INT, name TEXT, tel TXT)")

conn.commit()

cur.close()
conn.close()

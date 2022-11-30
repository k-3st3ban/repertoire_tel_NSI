import sqlite3

# ouverture des connexions
conn = sqlite3.connect('repertoire.db')
cur = conn.cursor()

# ajouter: tel secondaire, mail, entreprise, adresse, naissance, note
cur.execute('CREATE TABLE IF NOT EXISTS "CONTACT"("id" INTEGER PRIMARY KEY AUTOINCREMENT, "first_name" TEXT, "last_name" TEXT, "tel" TEXT, "picture" TEXT)')
conn.commit()

# fermeture des connexions
cur.close()
conn.close()

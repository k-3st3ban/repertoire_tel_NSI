# Projet Répertoire Téléphonique NSI Terminale

### Auteurs
Esteban PATTIN--BAS et Kirill BIRYUKOV

Projet disponible sur https://github.com/k-3st3ban/repertoire_tel_NSI

### Principe de fonctionnement
Ce code permet de lancer un site local ayant le fonctionnement d'un annuaire de contacts.
Une base de données SQL est utilisée et manipulée avec la bibliotheque python `sqlite3`.
Le site internet est lancé avec la bibliotheque `Flask`.
Il contient plusieurs pages codées en HTML et Jinja, avec du CSS et JS, et des formulaires d'ajout et modifications de contacts avec la librairie `Flask-WTF` (`FlaskForm`).

### Notice d'utilisation
Les librairies suivantes sont nécéssaires pour l'exécution du programme: `sqlite3` (installée de base), `Flask`, `Flask-WTF`.
Ces librairies peuvent être installées automatiquement avec `pip install -r requirements.txt`.
Pour tester le programme, veuillez lancer le fichier `main.py`: `python main.py`

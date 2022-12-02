"""Fichier des fonctions relatives à la BD"""
import sqlite3

from config import app_config


def db_tuple_to_dict(cursor, row):
    """Renvoie un dictionnaire putôt qu'un tuple depuis la BD

    Args:
        cursor (sqlite3.Cursor): l'objet cursor actuel pour trouver les clés
        row (tuple): la requête sous forme de tuple

    Returns:
        dict: dictionnaire avec les valeurs de la requête
    """
    return dict((cursor.description[index][0], value)
                for index, value in enumerate(row))


def db_get():
    """Renvoie un objet db qui permet de faire des requêtes à la BD

    Returns:
        sqlite3.Connection: objet de connexion à la BD
    """
    db_obj = sqlite3.connect(app_config["DATABASE_NAME"])
    db_obj.row_factory = db_tuple_to_dict
    return db_obj


def db_query(query, args=(), first=False, commit=False, fetch=True):
    """Permet des requêtes à la BD

    Args:
        query (str): la requête à la BD
        args (tuple, optional): les arguments de la requête. Defaults to ().
        first (bool, optional): renvoie seulement le premier résultat de la requête (True)
                                ou tous les résultats (False). Defaults to False.
        commit (bool, optional): ajout d'une commande de commit
                                nécessaire pour les modifications. Defaults to False.
        fetch (bool, optional): renvoie les résultats de la requête (True)
                                ou ne renvoie rien (False). Defaults to True.

    Returns:
        - None: quand fetch = False
        - dict: quand fetch = True, dictionnaire qui contient les résultats de la requête
    """
    # ouverture des connexions
    conn = db_get()
    cur = conn.cursor()
    # exécution de la requête
    cur.execute(query, args)
    # résultats de la requête
    if fetch is True:
        results = cur.fetchall()
    # commit pour la requête
    if commit is True:
        conn.commit()
    # fermeture des connexions
    cur.close()
    conn.close()
    # renvoi des valeurs
    if fetch is True:
        return (results[0] if results else None) if first else results


def db_init():
    """Initialisation de la BD"""
    db_query('CREATE TABLE IF NOT EXISTS "CONTACT"("id" INTEGER PRIMARY KEY AUTOINCREMENT, \
        "first_name" TEXT, "last_name" TEXT, "tel" TEXT, "tel_sec" TEXT, "email" TEXT, "entreprise" TEXT,\
            "adresse" TEXT, "naissance" TEXT, "picture" TEXT)', commit=True, fetch=False)

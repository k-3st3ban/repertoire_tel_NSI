from flask import Flask, render_template, redirect, url_for, abort, flash, request
import sqlite3
import os
import uuid

from config import app_config
from forms import ContactForm

import init_db


# configuration de Flask
app = Flask(__name__)
app.config.update(app_config)


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
    db_obj = sqlite3.connect(app.config["DATABASE_NAME"])
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


def contact_delete_picture(contact):
    """Suppression de la photo de profil d'un contact si elle existe

    Args:
        contact (dict): contact pour lequel il faut supprimer la photo
    """
    if contact and contact.get("picture"):
        os.remove(f"static/pictures/{contact.get('picture')}")


def contact_get(contact_id):
    """Retourne un contact en dictionnaire

    Args:
        contact_id (int): primary key du contact demandé

    Returns:
        dict: dictionnaire du contact
    """
    # requête du contact à la BD
    contact = db_query(
        f"SELECT * FROM CONTACT WHERE id={contact_id}", first=True)
    # renvoie une page 404 si le contact n'existe pas
    if not contact:
        return abort(404)
    return contact


def contact_infos_from_form(form, contact=None):
    """Sauvegarde la photo du contact puis renvoie ses informations

    Args:
        form (forms.ContactForm): formulaire de la page avec les nouvelles données
        contact (dict, optional): dictionnaire des données du contact actuel. Defaults to None.

    Returns:
        tuple: tuple d'informations du contact pour les arguments d'une requête à la BD
    """
    # upload d'une photo de profil
    filename = ""
    if form.picture.data:
        # sauvegarde de l'image pour accèder à son chemin d'accès
        filename = str(uuid.uuid4())
        form.picture.data.save(f"static/pictures/{filename}")
        # supprimer l'ancienne image
        contact_delete_picture(contact)
    if contact and contact.get("picture") and not form.picture.data:
        filename = contact.get("picture")
    # retourner les données
    return (form.first_name.data, form.last_name.data, form.tel.data, form.tel_sec.data, filename)


@app.template_filter("contact_label")
def contact_label(contact):
    """Renvoie le label d'un contact (prénom et nom, sinon: téléphone), à utiliser dans les templates

    Args:
        contact (dict): dictionnaire des données du contact

    Returns:
        str: label du contact
    """
    label = []
    if not contact.get("first_name") and not contact.get("last_name"):
        label.append(contact.get("tel"))
    if contact.get("first_name"):
        label.append(contact.get("first_name"))
    if contact.get("last_name"):
        label.append(contact.get("last_name"))
    return " ".join(label)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404"), 404


@app.get("/")
def index():
    if request.args.get("rech"):
        recherche = request.args.get("rech")
        contacts = db_query(f"""
            SELECT * FROM CONTACT WHERE
            first_name LIKE \"%{recherche}%\" 
            or last_name LIKE \"%{recherche}%\" 
            or tel LIKE \"%{recherche}%\"
                ORDER BY first_name""")
        if not contacts:
            flash("Aucun contact trouvé", "red")
            return redirect(url_for("index"))
    else:
        contacts = db_query("SELECT * FROM CONTACT ORDER BY first_name")
    return render_template("index.html", contacts=contacts)


@app.get("/contact/add")
def contact_add_page():
    form = ContactForm()
    return render_template("add.html", form=form)


@app.post("/contact/add")
def contact_add_post():
    form = ContactForm()
    if form.validate_on_submit():
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        else:
            db_query(
                f"INSERT INTO CONTACT({app.config['DATABASE_KEYS']}) VALUES({app.config['DATABASE_ARGS']})", args=contact_infos_from_form(form), commit=True, fetch=False)
            flash("Le contact a été ajouté", "green")
            return redirect(url_for("contact_add_page"))
    return render_template("add.html", form=form)


@app.get("/contact/<int:contact_id>")
def contact_infos(contact_id):
    # accéder au contact
    contact = contact_get(contact_id)
    return render_template("infos.html", contact=contact)


@app.get("/contact/<int:contact_id>/edit")
def contact_edit_page(contact_id):
    contact = contact_get(contact_id)
    form = ContactForm(data=contact)
    return render_template("edit.html", contact=contact, form=form)


@app.post("/contact/<int:contact_id>/edit")
def contact_edit_post(contact_id):
    contact = contact_get(contact_id)
    form = ContactForm(data=contact)
    if form.validate_on_submit():
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        else:
            db_query(f"UPDATE CONTACT SET ({app.config['DATABASE_KEYS']}) = ({app.config['DATABASE_ARGS']}) WHERE id={contact_id}",
                     args=contact_infos_from_form(form, contact), commit=True, fetch=False)
            flash("Le contact a été modifié", "green")
            return redirect(url_for("contact_infos", contact_id=contact_id))
    return render_template("edit.html", contact=contact, form=form)


@app.get("/contact/<int:contact_id>/delete")
def contact_delete(contact_id):
    # accéder au contact
    contact = contact_get(contact_id)
    # supprimer la photo de profil du contact
    contact_delete_picture(contact)
    # supprimer le contact de la DB
    db_query(
        f"DELETE FROM CONTACT WHERE id={contact_id}", commit=True, fetch=False)
    flash("Le contact a été supprimé", "red")
    return redirect(url_for("index"))


app.run(debug=True)

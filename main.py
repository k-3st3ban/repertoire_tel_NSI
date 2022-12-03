"""Fichier principal de l'application"""
import os
import uuid
from flask import Flask, render_template, redirect, url_for, abort, flash, request

from config import app_config
from forms import ContactForm
from db import db_query, db_init


# initialisation de la BD
db_init()


# configuration de Flask
app = Flask(__name__)
app.config.update(app_config)


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
    return (form.first_name.data, form.last_name.data, form.entreprise.data, form.tel.data,
            form.tel_sec.data, form.email.data, form.adresse.data, form.naissance.data, filename)


@app.template_filter("contact_label")
def contact_label(contact):
    """Renvoie le label d'un contact (prénom et nom, sinon téléphone), à utiliser dans les templates

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


@app.template_filter("database_key_to_txt")
def database_key_to_txt(key):
    """Renvoie une clé plus compréhensible depuis une clé de la BD, à utiliser dans les templates

    Args:
        key (str): la clé de dictionnaire à convertir

    Returns:
        str: la clé sous format plus compréhensible (ex: "first_name" -> "Prénom")
    """
    return app.config["DATABASE_KEYS_TO_TXT"][key]


@app.errorhandler(404)
def page_not_found(error):
    """Mise en place d'une page 404 personnalisée"""
    return render_template("404.html", title="404"), 404


@app.get("/")
def index():
    """Page d'accueil: liste et recherche de contacts"""
    # requête personnalisée quand le paramètre "recherche" est dans l'URL
    if request.args.get("recherche"):
        recherche = request.args.get("recherche")
        prenom_suppose = "" 
        nom_suppose = ""
        separations = 0 #Séparation du nom et prénom du aux limitations SQL si il y a recherche par les 2
        for lettre in recherche: 
            if lettre == " ":
                if separations > 0: #Dans le cas d'un nom séparé, ajout d'un espace
                    nom_suppose += " "
                separations += 1
            elif separations == 0:
                prenom_suppose += lettre
            else:
                nom_suppose += lettre
        contacts = db_query(f"""
            SELECT * FROM CONTACT WHERE
            first_name LIKE \"%{recherche}%\" 
            or last_name LIKE \"%{recherche}%\" 
            or tel LIKE \"%{recherche}%\"
            or first_name LIKE \"%{prenom_suppose}%\" and last_name LIKE \"%{nom_suppose}%\"
            or first_name LIKE \"%{nom_suppose}%\" and last_name LIKE \"%{prenom_suppose}%\"
                ORDER BY first_name""")
        if not contacts:
            flash("Aucun contact trouvé", "red")
            return redirect(url_for("index"))
    # requête normale (tous les contacts)
    else:
        contacts = db_query("SELECT * FROM CONTACT ORDER BY first_name")
    return render_template("index.html", contacts=contacts)


@app.get("/contact/add")
def contact_add_page():
    """Page GET d'ajout de contacts: renvoie du formulaire d'ajout"""
    form = ContactForm()
    return render_template("add.html", form=form)


@app.post("/contact/add")
def contact_add_post():
    """Page POST d'ajout de contacts: validations et ajout des données du contact"""
    form = ContactForm()
    if form.validate_on_submit():
        # vérification téléphone
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        # ajout dans la BD
        else:
            db_query(f"INSERT INTO CONTACT({app.config['DATABASE_KEYS']})\
                    VALUES({app.config['DATABASE_ARGS']})",
                     args=contact_infos_from_form(form), commit=True, fetch=False)
            flash("Le contact a été ajouté", "green")
            return redirect(url_for("contact_add_page"))
    return render_template("add.html", form=form)


@app.get("/contact/<int:contact_id>")
def contact_infos(contact_id):
    """Page d'infos d'un contact spécifique"""
    contact = contact_get(contact_id)
    return render_template("infos.html", contact=contact)


@app.get("/contact/<int:contact_id>/edit")
def contact_edit_page(contact_id):
    """Page GET de modifications de contact: renvoie du formulaire de modifications"""
    contact = contact_get(contact_id)
    form = ContactForm(data=contact)
    return render_template("edit.html", contact=contact, form=form)


@app.post("/contact/<int:contact_id>/edit")
def contact_edit_post(contact_id):
    """Page POST de modifications de contact: validations et modifications des données du contact"""
    contact = contact_get(contact_id)
    form = ContactForm(data=contact)
    if form.validate_on_submit():
        # vérification du téléphone
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        # modifications dans la BD
        else:
            db_query(f"UPDATE CONTACT SET\
                ({app.config['DATABASE_KEYS']}) = ({app.config['DATABASE_ARGS']})\
                WHERE id={contact_id}",
                     args=contact_infos_from_form(form, contact), commit=True, fetch=False)
            flash("Le contact a été modifié", "green")
            return redirect(url_for("contact_infos", contact_id=contact_id))
    return render_template("edit.html", contact=contact, form=form)


@app.get("/contact/<int:contact_id>/delete")
def contact_delete(contact_id):
    """Page de suppression d'un contact"""
    contact = contact_get(contact_id)
    # supprimer la photo de profil du contact
    contact_delete_picture(contact)
    # supprimer le contact de la BD
    db_query(
        f"DELETE FROM CONTACT WHERE id={contact_id}", commit=True, fetch=False)
    flash("Le contact a été supprimé", "red")
    return redirect(url_for("index"))


# app.run(debug=True) # pour le développement
app.run()

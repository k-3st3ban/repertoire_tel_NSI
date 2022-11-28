from flask import Flask, render_template, redirect, url_for, abort, flash, request, g
import sqlite3
import os
import uuid
from forms import ContactForm


app = Flask(__name__)
app.secret_key = "53f97a75fdd53a6404524a38"
DATABASE_NAME = "repertoire.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_NAME)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
    db.row_factory = make_dicts

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def db_query(query, args=(), first=False, commit=False, fetch=True):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    if fetch == True:
        results = cur.fetchall()
    if commit == True:
        conn.commit()
    cur.close()
    if fetch:
        return (results[0] if results else None) if first else results


def contact_infos_from_form(form, contact=None):
    filename = ""
    # upload d'une photo de profil
    if form.picture.data:
        # sauvegarde de l'image pour accèder à son chemin d'accès
        filename = str(uuid.uuid4())
        form.picture.data.save(f"static/pictures/{filename}")
        # supprimer l'ancienne image
        if contact and contact.get("picture"):
            os.remove(f"static/pictures/{contact.get('picture')}")
    if contact and contact.get("picture") and not form.picture.data:
        filename = contact.get("picture")
    # retourner les données
    return (form.first_name.data, form.last_name.data, form.tel.data, filename)


@app.template_filter("contact_label")
def contact_label(contact):
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
        contacts = db_query(
            f"SELECT * FROM CONTACT WHERE first_name LIKE \"%{recherche}%\" or last_name LIKE \"%{recherche}%\" or tel LIKE \"%{recherche}%\" ORDER BY first_name")
        if not contacts:
            flash("Aucun contact trouvé", "red")
            return redirect(url_for("index"))
    else:
        contacts = db_query("SELECT * FROM CONTACT ORDER BY first_name")
    return render_template("index.html", contacts=contacts)


@app.get("/contact/add")
def contact_add_page():
    form = ContactForm()
    return render_template("add.html", form=ContactForm())


@app.post("/contact/add")
def contact_add_post():
    form = ContactForm()
    if form.validate_on_submit():
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        else:
            db_query(
                "INSERT INTO CONTACT(first_name, last_name, tel, picture) VALUES(?, ?, ?, ?)", args=contact_infos_from_form(form), commit=True, fetch=False)
            flash("Le contact a été ajouté", "green")
            return redirect(url_for("contact_add_page"))
    return render_template("add.html", form=ContactForm())


@app.get("/contact/<int:contact_id>")
def contact_infos(contact_id):
    contact = db_query(
        f"SELECT * FROM CONTACT WHERE id={contact_id}", first=True)
    if not contact:
        return abort(404)
    return render_template("infos.html", contact=contact)


@app.get("/contact/<int:contact_id>/edit")
def contact_edit_page(contact_id):
    contact = db_query(
        f"SELECT * FROM CONTACT WHERE id={contact_id}", first=True)
    if not contact:
        return abort(404)
    form = ContactForm(data=contact)
    return render_template("edit.html", contact=contact, form=form)


@app.post("/contact/<int:contact_id>/edit")
def contact_edit_post(contact_id):
    contact = db_query(
        f"SELECT * FROM CONTACT WHERE id={contact_id}", first=True)
    if not contact:
        return abort(404)
    form = ContactForm(data=contact)
    if form.validate_on_submit():
        if not form.tel.data:
            flash("Un numéro de téléphone est nécessaire", "yellow")
        else:
            db_query(f"UPDATE CONTACT SET (first_name, last_name, tel, picture) = (?, ?, ?, ?) WHERE id={contact_id}",
                     args=contact_infos_from_form(form, contact), commit=True, fetch=False)
            flash("Le contact a été modifié", "green")
            return redirect(url_for("contact_infos", contact_id=contact_id))
    return render_template("edit.html", contact=contact, form=form)


@app.get("/contact/<int:contact_id>/delete")
def contact_delete(contact_id):
    db_query(
        f"DELETE FROM CONTACT WHERE id={contact_id}", commit=True, fetch=False)
    flash("Le contact a été supprimé", "red")
    return redirect(url_for("index"))


app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, abort, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "53f97a75fdd53a6404524a38"
DATABASE_NAME = "repertoire.db"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="404"), 404


@app.get("/")
def index():
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONTACT")
    conn.commit()
    contacts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", contacts=contacts)


@app.get("/contact/add")
def contact_add_page():
    return render_template("add.html")


@app.post("/contact/add")
def contact_add_post():
    # flash success message
    return redirect(url_for("index"))


@app.get("/contact/<int:contact_id>")
def contact_infos(contact_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    # handle errors (ex: contact not exists)
    cur.execute(f"SELECT * FROM CONTACT WHERE id={contact_id}")
    conn.commit()
    try:
        contact = cur.fetchall()[0]
    except IndexError:
        return abort(404)
    cur.close()
    conn.close()
    return render_template("infos.html", contact=contact)


@app.get("/contact/<int:contact_id>/delete")
def contact_delete(contact_id):
    # delete contact here + flash message
    flash("Le contact a été supprimé", "red")
    return redirect(url_for("index"))


app.run(debug=True)

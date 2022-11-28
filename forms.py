from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from flask import redirect, url_for, flash


class ContactForm(FlaskForm):
    picture = FileField("Photo de profil")
    first_name = StringField("Prénom", render_kw={"placeholder": "Prénom"})
    last_name = StringField("Nom", render_kw={"placeholder": "Nom"})
    tel = StringField("Téléphone", render_kw={
                      "placeholder": "Téléphone"})
    submit = SubmitField("Envoyer")

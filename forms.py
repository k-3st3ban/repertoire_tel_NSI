"""Fichier des formulaires de l'application"""
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TelField, EmailField


class ContactForm(FlaskForm):
    """Formulaire de création/modification d'un contact"""
    picture = FileField("Photo de profil")
    first_name = StringField("Prénom", render_kw={"placeholder": "Prénom"})
    last_name = StringField("Nom", render_kw={"placeholder": "Nom"})
    entreprise = StringField("Entreprise", render_kw={
                             "placeholder": "Entreprise"})
    tel = TelField("Téléphone", render_kw={
        "placeholder": "Téléphone"})
    tel_sec = TelField("Téléphone Secondaire", render_kw={
        "placeholder": "Téléphone Secondaire"})
    email = EmailField("Adresse Email", render_kw={
                       "placeholder": "Adresse Email"})
    adresse = StringField("Adresse", render_kw={
        "placeholder": "Adresse"})
    naissance = StringField("Naissance", render_kw={
        "placeholder": "Naissance"})

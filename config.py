"""Fichier de configuration de l'application"""
app_config = {
    "SECRET_KEY": "53f97a75fdd53a6404524a38",
    "DATABASE_NAME": "repertoire.db",
    "DATABASE_KEYS": "first_name, last_name, entreprise, tel, tel_sec, email, adresse, naissance, picture",
    "DATABASE_ARGS": "?, ?, ?, ?, ?, ?, ?, ?, ?",
    "DATABASE_KEYS_TO_TXT": {
        "first_name": "Prénom",
        "last_name": "Nom",
        "entreprise": "Entreprise",
        "tel": "Téléphone",
        "tel_sec": "Téléphone Secondaire",
        "email": "Adresse Email",
        "adresse": "Adresse",
        "naissance": "Naissance"
    }
}

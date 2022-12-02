function deleteContact(e) {
    if (!confirm("Êtes-vous sûr de supprimer ce contact?")) {
        e.preventDefault();
    }
}
def repertoire_telephonique():
    while(True):
        choix_de_l_utilisateur=menu()
        if (choix_de_l_utilisateur!=0):
            if(choix_de_l_utilisateur==1):
                print("Vous avez choisi d'écrire dans le répertoire téléphonique ...")
                ecriture()
            if(choix_de_l_utilisateur==2):
                lecture()
        else:
            print("Le programme est terminé.")
            return

def menu():
    print("0-quitter")
    print("1-écrire dans le répertoire")
    print("2-rechercher dans le répertoire")
    choix=input("Votre choix ? ")
    return(int(choix))

def ecriture():
    nom_a_entrer=input("Nom (0 pour terminer) : ")
    while (nom_a_entrer!="0"):
        with open('rep_tel.txt','a') as f :
            f.write(nom_a_entrer)
            f.write('\n')
            tel_a_entrer=input("Téléphone : ")
            f.write(tel_a_entrer)
            f.write('\n')
        nom_a_entrer=input("Nom (0 pour terminer) : ")
    return

def lecture():
    noms=[]
    with open('rep_tel.txt','r') as f :
        for ligne in f:
            ligne=ligne.replace("\n","")
            noms.append(ligne)
    #ligne suivante à décommenter pour avoir le répertoire en entier
    #print(noms)
    nom_a_chercher=input("Entrer un nom : ")
    compteur_nom=0
    indice=0
    for element in noms:
        indice=indice+1
        if(element==nom_a_chercher):
            print("Le numéro recherché est : ", noms[indice])
            compteur_nom=compteur_nom+1
    if(compteur_nom==0):
        print("Inconnu.")

repertoire_telephonique()
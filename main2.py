import data

# Fonction pour tester la connexion Internet
def test_internet_connection():
    url = data.url_for_test
    timeout = data.timeout

    try:
        response = data.requests.get(url=url, timeout=timeout)
        if response.status_code == 200:
            return True
    except data.requests.RequestException:
        pass
    return False

# Fonction pour mettre à jour le chemin en remplaçant les backslashes par des slashes
def updatePath(chaine):
    nouvelle_chaine = ""
    for caractere in chaine:
        if caractere == "\\":
            nouvelle_chaine += "/"
        else:
            nouvelle_chaine += caractere
    return nouvelle_chaine

# Fonction pour enregistrer les fichiers envoyés avec succès
def send(fichier):
    with open('elements_envoyes.txt', 'a') as f:
        f.write(fichier + '\n')

# Fonction pour enregistrer les fichiers qui n'ont pas pu être envoyés et copier les fichiers dans le répertoire des erreurs
def error(fichier, chemin_complet):
    with open('elements_non_envoyes.txt', 'a') as f:
        f.write(fichier + '\n')
    data.shutil.copy(chemin_complet, data.os.path.join(data.repertoire_erreurs, fichier))

# Fonction pour envoyer un fichier à l'API
def envoyer_fichier(chemin_complet, fichier):
    with open(chemin_complet, 'rb') as file:
        created_file = {'image': file}
        
        # Vérifier la connexion Internet avant d'envoyer le fichier
        if test_internet_connection():
            try:
                response = data.requests.post(data.endpoint, files=created_file, data={'slug': data.idClient})
                if response.status_code == 200:
                    print("Le fichier a été envoyé avec succès.")
                    send(fichier)  # Enregistrer le fichier envoyé
                else:
                    print("Le code de retour n'est pas 200")
                    error(fichier, chemin_complet)  # Enregistrer et copier le fichier en cas d'erreur
            except:
                print("L'envoie n'a pas été effectué")
                error(fichier, chemin_complet)  # Enregistrer et copier le fichier en cas d'exception
        else:
            print("Le PC n'est pas connecté à Internet.")
            error(fichier, chemin_complet)  # Enregistrer et copier le fichier en cas de problème de connexion

# Fonction principale pour surveiller le répertoire et envoyer les fichiers
def main():
    # Mettre à jour le chemin du répertoire à surveiller
    repertoire_a_surveiller = updatePath(data.repertoire)
    
    # Lister tous les fichiers actuels dans le répertoire
    fichiers_actuels = data.os.listdir(repertoire_a_surveiller)

    while True:
        
        # Si la liste des fichiers est vide, arrêter la boucle
        if not fichiers_actuels:
            print("Tous les fichiers ont été traités.")
            break

        # Parcourir tous les fichiers et les envoyer
        for fichier in fichiers_actuels:
            chemin_complet = data.os.path.join(repertoire_a_surveiller, fichier)
            envoyer_fichier(chemin_complet, fichier)  # Envoyer le fichier
            fichiers_actuels.remove(fichier)  # Retirer le fichier de la liste

        # Attendre un certain intervalle avant de vérifier à nouveau
        data.time.sleep(data.intervalle_de_verification)

# Exécuter le programme principal
main()
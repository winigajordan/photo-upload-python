import data


def test_internet_connection():

    url = data.url_for_test
    timeout = data.timeout

    try:
        response = data.requests.get(url=url,timeout=timeout)
        if response.status_code == 200:
            return True
    except data.requests.RequestException:
        pass
    return False

def updatePath(chaine):
    nouvelle_chaine = ""
    for caractere in chaine:
        if caractere == "\\":
            nouvelle_chaine += "/"
        else:
            nouvelle_chaine += caractere
    return nouvelle_chaine

"""
def get_path_from_directory(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()
            if lignes:
                derniere_ligne = lignes[-1].strip()  # Strip pour supprimer les caractères de nouvelle ligne
                return derniere_ligne
            else:
                return None  # Si le fichier est vide
    except FileNotFoundError:
        print("Le fichier spécifié n'existe pas.")
        return None  # Si le fichier n'existe pas
    except Exception as e:
        print("Une erreur s'est produite lors de la lecture du fichier:", e)
        return None

"""



def main():


    repertoire_a_surveiller = updatePath(data.repertoire)

    # Liste des fichiers actuels dans le répertoire
    fichiers_existant = set(data.os.listdir(repertoire_a_surveiller))

    # Liste pour stocker les nouveaux fichiers
    nouveaux_fichiers = []

   

    while True:
        # Liste des fichiers actuels dans le répertoire
        fichiers_actuels = set(data.os.listdir(repertoire_a_surveiller))
        
        # Recherche de nouveaux fichiers
        nouveaux_fichiers_temp = fichiers_actuels - fichiers_existant
        
        # Ajouter les nouveaux fichiers à la liste
        nouveaux_fichiers.extend(nouveaux_fichiers_temp)
        
        # Mettre à jour la liste des fichiers existants
        fichiers_existant = fichiers_actuels
        
        # Si des nouveaux fichiers sont trouvés, les imprimer et envoyer vers l'API
        if nouveaux_fichiers != []:
            #print(nouveaux_fichiers)
            # requests.post('https://eoljah6zhpt6t2h.m.pipedream.net', json=nouveaux_fichiers)
            print(nouveaux_fichiers)
            # Si des nouveaux fichiers sont trouvés
            if test_internet_connection():
                print("Le PC est connecté à Internet.")
                for fichier in nouveaux_fichiers:
                    print("Nouveau fichier créé:", fichier)

                    # Construire le chemin complet du fichier
                    chemin_complet = data.os.path.join(repertoire_a_surveiller, fichier)
        
                    
                    with open(chemin_complet, 'rb') as file:
                        created_file = {'image': file}
                    # Envoi du fichier a l'API
                        
                        try: 

                            #response = data.requests.post(data.endpoint, data={'file': fichier})
                            response = data.requests.post(data.endpoint, files=created_file)

                            # Si la réponse est 200 OK
                            if response.status_code == 200:
                                # Écrire l'élément envoyé dans un fichier texte
                                with open('elements_envoyes.txt', 'a') as f:
                                    f.write(fichier + '\n')
                            else:
                                # Écrire l'élément non envoyé dans un autre fichier texte
                                with open('elements_non_envoyes.txt', 'a') as f:
                                    f.write(fichier + '\n')
                                
                        except:
                                with open('elements_non_envoyes.txt', 'a') as f:
                                    f.write(fichier + '\n')


                        # Retirer le fichier de la liste des nouveaux fichiers
                        nouveaux_fichiers.remove(fichier)
            else :
                print("Le PC n'est pas connecté à Internet.")



        # Attendre avant de vérifier à nouveau
        data.time.sleep(data.intervalle_de_verification)



# Exécuter le programme principal
main()
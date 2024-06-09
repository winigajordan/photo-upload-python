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


def send(fichier):
    with open('elements_envoyes.txt', 'a') as f:
                                    f.write(fichier + '\n')


def error(fichier, chemin_complet):
    with open('elements_non_envoyes.txt', 'a') as f:
        f.write(fichier + '\n')
    data.shutil.copy(chemin_complet, data.os.path.join(data.repertoire_erreurs, fichier))
    


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

        #Repertorie des erreurs
        #repertoire_erreurs = updatePath(data.repertoire_erreurs)
        
        # Si des nouveaux fichiers sont trouvés, les imprimer et envoyer vers l'API
        if nouveaux_fichiers != []:
            #print(nouveaux_fichiers)
            # requests.post('https://eoljah6zhpt6t2h.m.pipedream.net', json=nouveaux_fichiers)
            print(nouveaux_fichiers)
            
            
            for fichier in nouveaux_fichiers:
                print("Nouveau fichier créé:", fichier)
                nouveaux_fichiers.remove(fichier)
                data.os.chmod(fichier, 0o777)
                # Construire le chemin complet du fichier
                chemin_complet = data.os.path.join(repertoire_a_surveiller, fichier)
                with open(chemin_complet, 'rb') as file:
                    created_file = {'image': file}


                    #Test de connexion internet                    
                    if test_internet_connection():

                        # Envoi du fichier a l'API
                        try: 
                            #response = data.requests.post(data.endpoint, data={'file': fichier})
                            response = data.requests.post(data.endpoint, files=created_file, data={'slug':data.idClient})
                            #print(response)
                            # Si la réponse est 200 OK
                            if response.status_code == 200:
                                # Écrire l'élément envoyé dans un fichier texte
                                send(fichier)
                            else:
                                # Écrire l'élément non envoyé dans un autre fichier texte
                                error(fichier)
                                break
                                
                        except:
                            error(fichier, chemin_complet)
                            break

                    else:
                        print("Le PC n'est pas connecté à Internet.")   
                        error(fichier, chemin_complet)
                        break

            # Retirer le fichier de la liste des nouveaux fichiers
           
           
           
            
            



        # Attendre avant de vérifier à nouveau
        data.time.sleep(data.intervalle_de_verification)



# Exécuter le programme principal
main()
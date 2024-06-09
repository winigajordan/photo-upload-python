# Description: Configuration des paramètres de l'application


# Importation des modules nécessaires
import os
import time
import requests
import shutil

# URL pour tester la connexion Internet
url_for_test = "http://127.0.0.1:8000"

#client ID
# Endpoint de l'API

idClient = "6665dbb918763"  

# Endpoint de l'API
endpoint = url_for_test+"/demande/"+idClient+"/image" 


# Temps d'attente pour la réponse pour le test de connexion Internet (en secondes)
timeout = 5


# Répertoire à surveiller pour les fichiers à traiter
#repertoire_a_surveiller = "C:\\Users\ziadh\\Desktop\\test\\hello"
#repertoire = r"C:\Users\winig\OneDrive\Desktop\JORD\STRADMOB\Photo-Upload-V1" 
repertoire = r"C:\Users\winig\OneDrive\Desktop\JORD\STRADMOB\Photo-Upload-V1\dossier test"

# Répertoire pour stocker les fichiers en erreur
repertoire_erreurs = r"C:\Users\winig\OneDrive\Desktop\JORD\STRADMOB\Photo-Upload-V1\erreurs"


# Intervalle de vérification avant de vérifier les nouveaux fichiers (en secondes)
intervalle_de_verification = 5



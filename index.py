import os
import json
import requests
from datetime import datetime, timedelta

CACHE_FOLDER = "cache"  # Dossier où les fichiers de cache seront stockés
CACHE_EXPIRATION = timedelta(minutes=1)  # Durée d'expiration du cache (1 heure dans cet exemple)
CACHE_FILE = "cache_file.json"  # Nom du fichier de cache

def charger_donnees_json_de_url(url):
    # Générer le chemin complet du fichier de cache
    cacheFichier = os.path.join(CACHE_FOLDER, CACHE_FILE)

    # Vérifier si le fichier de cache existe et s'il n'a pas expiré
    if os.path.exists(cacheFichier):
        timestamp_expiration = os.path.getmtime(cacheFichier) + CACHE_EXPIRATION.total_seconds()
        current_timestamp = datetime.now().timestamp()

        print(f"Timestamp d'expiration : {timestamp_expiration}")
        print(f"Heure actuelle : {current_timestamp}")

        if current_timestamp < timestamp_expiration:
            with open(cacheFichier, 'r', encoding='utf-8') as fichier:
                donnees_json = json.load(fichier)
                print(f"Données chargées depuis le cache {cacheFichier}, {len(donnees_json)} éléments")
                return donnees_json
        else:
            print("Le cache a expiré.")
    else:
        print(f"Le fichier de cache {cacheFichier} n'existe pas.")

    # Si le fichier de cache n'existe pas ou a expiré, faire la requête HTTP
    reponse = requests.get(url)

    if reponse.status_code == 200:
        donnees_json = reponse.json()
        print(f"Données chargées depuis {url}, {len(donnees_json)} éléments")

        # Sauvegarder les données dans le cache
        os.makedirs(CACHE_FOLDER, exist_ok=True)
        with open(cacheFichier, 'w', encoding='utf-8') as fichier_cache:
            json.dump(donnees_json, fichier_cache, ensure_ascii=False)
            print(f"Données sauvegardées dans le cache {cacheFichier}, {len(donnees_json)} éléments")

        return donnees_json
    else:
        print(f"Échec du chargement des données depuis {url}. Code d'état : {reponse.status_code}")
        return None

def sauvegarder_donnees_json(nom_fichier, donnees_json):
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        json.dump(donnees_json, fichier, ensure_ascii=False)
        print(f"Données sauvegardées dans {nom_fichier}, {len(donnees_json)} éléments")

# Exemple d'utilisation
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json?lang=fr&timezone=Europe%2FParis"
donnees_json_de_url = charger_donnees_json_de_url(url)

if donnees_json_de_url:
    sauvegarder_donnees_json("sortie.json", donnees_json_de_url)

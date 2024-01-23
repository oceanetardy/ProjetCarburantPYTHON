import os
import json
import requests
from datetime import datetime, timedelta
import pytz

CACHE_FOLDER = "cache"  # Dossier où les fichiers de cache seront stockés
CACHE_EXPIRATION = timedelta(hours=1)  # Durée d'expiration du cache
CACHE_FILE = "cache_file.json"  # Nom du fichier de cache

def charger_donnees_json_de_url(url):
    # Générer le chemin complet du fichier de cache
    cacheFichier = os.path.join(CACHE_FOLDER, CACHE_FILE)

    # Vérifier si le fichier de cache existe et s'il n'a pas expiré
    if os.path.exists(cacheFichier):
        timestamp_expiration = os.path.getmtime(cacheFichier) + CACHE_EXPIRATION.total_seconds()
        current_timestamp = datetime.now().timestamp()

        expiration_date = datetime.fromtimestamp(timestamp_expiration, tz=pytz.timezone("Europe/Paris")).strftime(
            '%Y-%m-%d %H:%M:%S %Z')
        print(f"Date d'expiration : {expiration_date}")

        current_date = datetime.fromtimestamp(current_timestamp, tz=pytz.timezone("Europe/Paris")).strftime(
            '%Y-%m-%d %H:%M:%S %Z')
        print(f"Heure actuelle : {current_date}")

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

        # Vérifier si les données sont une liste
        if isinstance(donnees_json, list):
            # Pour chaque record dans les données JSON, ajouter le nom de la marque
            for record in donnees_json:
                station_id = record.get('id', None)
                if station_id:
                    brand_name = get_station_info_by_id(station_id)
                    record['brand_name'] = brand_name

            # Sauvegarder les données dans le cache
            os.makedirs(CACHE_FOLDER, exist_ok=True)
            with open(cacheFichier, 'w', encoding='utf-8') as fichier_cache:
                json.dump(donnees_json, fichier_cache, ensure_ascii=False)
                print(f"Données sauvegardées dans le cache {cacheFichier}, {len(donnees_json)} éléments")

            return donnees_json
        else:
            print("Les données ne sont pas sous la forme attendue.")
    else:
        print(f"Échec du chargement des données depuis {url}. Code d'état : {reponse.status_code}")
        return None

def sauvegarder_donnees_json(nom_fichier, donnees_json):
    with open(nom_fichier, 'w', encoding='utf-8') as fichier:
        json.dump(donnees_json, fichier, ensure_ascii=False)
        print(f"Données sauvegardées dans {nom_fichier}, {len(donnees_json)} éléments")

def get_station_info_by_id(station_id):
    url = f"https://api.prix-carburants.2aaz.fr/station/{station_id}"

    try:
        response = requests.get(url)
        data = response.json()

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Récupérer le nom de la marque associée
            brand_info = data.get('Brand', {})
            brand_name = brand_info.get('name', 'Nom de la marque non disponible')
            return brand_name
        else:
            print(f"Erreur lors de la requête : {response.status_code} ,Station id : {str(station_id)}")
    except Exception as e:
        print(f"Erreur lors de la requête : {str(e)}, Station id : {str(station_id)}")


# Charger les données JSON depuis l'URL
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json?lang=fr&timezone=Europe%2FParis"
donnees_json_de_url = charger_donnees_json_de_url(url)

# Sauvegarder les données mises à jour dans un nouveau fichier
if donnees_json_de_url:
    sauvegarder_donnees_json("sortie.json", donnees_json_de_url)

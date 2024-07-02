import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import subprocess

# Constants
CACHE_FOLDER = "cache/"
CACHE_EXPIRATION = timedelta(hours=1)
CACHE_FILE = "cache_file.json"
LIMIT = 100
BASE_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records"
STATIONS_WITH_NAME_FILE = "stations_with_name.csv"

def cache_name():
    return os.path.join(CACHE_FOLDER, CACHE_FILE)

def cache_hit(cacheFichier):
    if not os.path.exists(cacheFichier):
        print(f"Le fichier de cache {cacheFichier} n'existe pas.")
        return False
    if datetime.now().timestamp() >= os.path.getmtime(cacheFichier) + CACHE_EXPIRATION.total_seconds():
        print("Le cache a expiré.")
        return False
    return True

def get_total_count():
    url = f"{BASE_URL}?limit=1&offset=0"
    try:
        reponse = requests.get(url)
        if reponse.status_code != 200:
            raise RuntimeError(f"Échec de récupération du nombre total d'enregistrements. Code d'état : {reponse.status_code}")
        total_count = reponse.json().get('total_count', 0)
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la récupération du nombre total d'enregistrements : {e}")
    return total_count

def get_stations(url):
    try:
        reponse = requests.get(url)
        print(f"Requête HTTP vers {url}, code de réponse : {reponse.status_code}")
        if reponse.status_code != 200:
            raise RuntimeError(f"Échec du chargement des données depuis {url}. Code d'état : {reponse.status_code}")
        donnees_json = reponse.json().get('results', [])
        if not donnees_json:
            raise ValueError("No data")
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la requête HTTP : {e}")
    return donnees_json

def charger_noms_stations():
    df = pd.read_csv(STATIONS_WITH_NAME_FILE)
    id_info_dict = {str(row['ID']): {'marque': row['Marque'], 'nom': row['Nom']} for _, row in df.iterrows()}
    return id_info_dict

def write_cache(cacheFichier, all_data):
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    try:
        with open(cacheFichier, 'w', encoding='utf-8') as fichier_cache:
            json.dump(all_data, fichier_cache, ensure_ascii=False)
            print(f"Données sauvegardées dans le cache {cacheFichier}, {len(all_data)} éléments")
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la sauvegarde des données dans le cache : {e}")


def charger_donnees_json_de_url(base_url):
    cacheFichier = cache_name()
    print(f"Chemin du fichier de cache : {cacheFichier}")
    if cache_hit(cacheFichier):
        try:
            with open(cacheFichier, 'r', encoding='utf-8') as fichier:
                donnees_json = json.load(fichier)
                print(f"Données chargées depuis le cache {cacheFichier}, {len(donnees_json)} éléments")
                return donnees_json
        except Exception as e:
            print(f"Erreur lors du chargement des données depuis le cache : {e}")

    offset = 0
    all_data = []
    total_count = get_total_count()
    print(f"Nombre total d'enregistrements : {total_count}")

    while offset < total_count:
        limit = min(LIMIT, total_count - offset)

        # Vérifier si offset + limit dépasse la limite imposée par l'API (10000 dans votre cas)
        if offset + limit > 10000:
            limit = 10000 - offset  # Réduire limit pour respecter la limite de l'API

        url = f"{BASE_URL}?limit={limit}&offset={offset}"
        try:
            donnees_json = get_stations(url)
            all_data.extend(donnees_json)
            offset += len(donnees_json)
        except RuntimeError as e:
            print(f"Erreur lors de la récupération des données depuis {url}: {e}")
            break

    id_info_dict = charger_noms_stations()
    for item in all_data:
        item_id = str(item['id'])
        if item_id in id_info_dict:
            item.update(id_info_dict[item_id])

    print(f"Données chargées depuis {base_url}, {len(all_data)} éléments")
    write_cache(cacheFichier, all_data)
    return all_data


if __name__ == "__main__":
    donnees_json_de_url = charger_donnees_json_de_url(BASE_URL)
    subprocess.run(["python", "db/import_db.py"])

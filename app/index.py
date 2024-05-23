import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import subprocess

# Constants
CACHE_FOLDER = "app/cache/"  # Cache directory
CACHE_EXPIRATION = timedelta(hours=1)  # Cache expiration duration
CACHE_FILE = "cache_file.json"  # Cache file name
LIMIT = 100  # Number of results per request

def charger_donnees_json_de_url(base_url):
    # Construct full cache file path
    cacheFichier = os.path.join(CACHE_FOLDER, CACHE_FILE)
    print(f"Chemin du fichier de cache : {cacheFichier}")

    # Check if the cache file exists and is still valid
    if os.path.exists(cacheFichier):
        timestamp_expiration = os.path.getmtime(cacheFichier) + CACHE_EXPIRATION.total_seconds()
        current_timestamp = datetime.now().timestamp()

        expiration_date = datetime.fromtimestamp(timestamp_expiration, tz=pytz.timezone("Europe/Paris")).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"Date d'expiration : {expiration_date}")

        current_date = datetime.fromtimestamp(current_timestamp, tz=pytz.timezone("Europe/Paris")).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"Heure actuelle : {current_date}")

        if current_timestamp < timestamp_expiration:
            try:
                with open(cacheFichier, 'r', encoding='utf-8') as fichier:
                    donnees_json = json.load(fichier)
                    print(f"Données chargées depuis le cache {cacheFichier}, {len(donnees_json)} éléments")
                    return donnees_json
            except Exception as e:
                print(f"Erreur lors du chargement des données depuis le cache : {e}")
        else:
            print("Le cache a expiré.")
    else:
        print(f"Le fichier de cache {cacheFichier} n'existe pas.")

    # If the cache file does not exist or has expired, make the HTTP request
    offset = 0
    all_data = []

    def get_total_count():
        url = f"{base_url}?limit=1&offset=0"
        try:
            reponse = requests.get(url)
            if reponse.status_code == 200:
                total_count = reponse.json().get('total_count', 0)
                return total_count
            else:
                print(f"Échec de récupération du nombre total d'enregistrements. Code d'état : {reponse.status_code}")
                return 0
        except Exception as e:
            print(f"Erreur lors de la récupération du nombre total d'enregistrements : {e}")
            return 0

    total_count = get_total_count()
    if total_count == 0:
        print("Impossible de récupérer les données car le nombre total d'enregistrements est inconnu.")
    else:
        print(f"Nombre total d'enregistrements : {total_count}")

    while offset < total_count:
        limit = min(LIMIT, total_count - offset)
        url = f"{base_url}?limit={limit}&offset={offset}"
        try:
            reponse = requests.get(url)
            print(f"Requête HTTP vers {url}, code de réponse : {reponse.status_code}")

            if reponse.status_code == 200:
                donnees_json = reponse.json().get('results', [])
                if not donnees_json:
                    break  # Stop the loop if no data is returned
                all_data.extend(donnees_json)
                offset += len(donnees_json)
            else:
                print(f"Échec du chargement des données depuis {url}. Code d'état : {reponse.status_code}")
                break
        except Exception as e:
            print(f"Erreur lors de la requête HTTP : {e}")
            break
    # Load brand and name information from the CSV file
    stations_with_name_file = "app/stations_with_name.csv"
    df = pd.read_csv(stations_with_name_file)

    # Create a dictionary with brand and name information for each ID
    id_info_dict = {str(row['ID']): {'marque': row['Marque'], 'nom': row['Nom']} for _, row in df.iterrows()}

    # Iterate over the list of data
    for item in all_data:
        item_id = str(item['id'])
        if item_id in id_info_dict:
            item.update(id_info_dict[item_id])

    print(f"Données chargées depuis {base_url}, {len(all_data)} éléments")

    # Save the data to the cache
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    try:
        with open(cacheFichier, 'w', encoding='utf-8') as fichier_cache:
            json.dump(all_data, fichier_cache, ensure_ascii=False)
            print(f"Données sauvegardées dans le cache {cacheFichier}, {len(all_data)} éléments")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données dans le cache : {e}")

    return all_data

# Données json
base_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records"
donnees_json_de_url = charger_donnees_json_de_url(base_url)

# Call the script import_db.py with subprocess
subprocess.run(["python", "app/db/import_db.py"])

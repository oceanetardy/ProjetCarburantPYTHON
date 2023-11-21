import json
import requests

def charger_donnees_json_de_url(url):
    reponse = requests.get(url)
    
    if reponse.status_code == 200:
        donnees_json = reponse.json()
        print(f"Données chargées depuis {url}, {len(donnees_json)} éléments")
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

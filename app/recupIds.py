import json
import csv
# Chemin du cache
chemin_fichier = 'cache/cache_file.json'

with open(chemin_fichier, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# Vérifier si le fichier contient une liste d'éléments
if isinstance(data_list, list):
    # Stockage des ids
    ids_list = []

    # Boucler sur chaque élément
    for item in data_list:
        # Vérifier si une clé id
        if 'id' in item:
            # Ajouts des ids à la liste
            ids_list.append(item['id'])

    # Écrire la liste des IDs dans un nouveau fichier CSV
    with open('ids_stations_gouv.csv', 'w', newline='', encoding='utf-8') as nouveau_fichier:
        writer = csv.writer(nouveau_fichier)
        writer.writerow(['ID'])
        for id_value in ids_list:
            writer.writerow([id_value])

    print("Fichier 'ids_stations_gouv.csv' généré avec succès.")
else:
    print("Le fichier csv ne contient pas une liste d'éléments.")

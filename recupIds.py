import json
import csv
# Spécifier le chemin relatif ou absolu vers le fichier JSON
chemin_fichier = 'cache/cache_file.json'

# Charger le contenu du fichier JSON
with open(chemin_fichier, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

# Vérifier si le fichier contient une liste d'éléments
if isinstance(data_list, list):
    # Créer une liste pour stocker les IDs
    ids_list = []

    # Boucler à travers chaque élément
    for item in data_list:
        # Vérifier si l'élément contient la clé 'id'
        if 'id' in item:
            # Récupérer l'ID et l'ajouter à la liste
            ids_list.append(item['id'])

    # Écrire la liste des IDs dans un nouveau fichier CSV
    with open('ids_stations.csv', 'w', newline='', encoding='utf-8') as nouveau_fichier:
        # Utiliser le module csv pour écrire dans le fichier CSV
        writer = csv.writer(nouveau_fichier)
        # Écrire la première ligne avec le nom de la colonne
        writer.writerow(['ID'])
        # Écrire les IDs dans les lignes suivantes
        for id_value in ids_list:
            writer.writerow([id_value])

    print("Fichier 'ids_stations.csv' généré avec succès.")
else:
    print("Le fichier csv ne contient pas une liste d'éléments.")

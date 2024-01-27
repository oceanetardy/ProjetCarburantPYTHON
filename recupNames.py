import pandas as pd
import json

# Charger le fichier JSON
with open('stations_names.json', 'r', encoding='utf-8') as json_file:
    data_json = json.load(json_file)

# Charger le fichier CSV contenant les ids du site gouv
df = pd.read_csv('ids_stations.csv')

# Fonction pour récupérer la marque et le nom en fonction de l'ID
def get_info_from_json(row):
    id = str(row['ID'])
    if id in data_json:
        return pd.Series([data_json[id]['marque'], data_json[id]['nom']])
    else:
        return pd.Series(['', ''])

# Appliquer la fonction pour créer de nouvelles colonnes
df[['Marque', 'Nom']] = df.apply(get_info_from_json, axis=1)

# Sauvegarder le nouveau DataFrame avec les informations ajoutées dans un nouveau fichier CSV
df.to_csv('stations_with_name.csv', index=False)

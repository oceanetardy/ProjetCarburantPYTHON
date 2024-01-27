import pandas as pd
import requests

# Fonction pour récupérer le nom depuis l'API en utilisant l'ID
def get_name_from_api(row):
    station_id = row['ID']
    url = f"https://api.prix-carburants.2aaz.fr/station/{station_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        brand_name = data.get('Brand', {}).get('name', '')
        print(f"Row: {row.name}, ID: {station_id}, Brand Name: {brand_name}")
        return brand_name
    else:
        error_message = f"Row: {row.name}, Failed to retrieve data for ID: {station_id}, Error: {response.text}"
        print(error_message)
        return ''

# Charger le CSV
csv_path = 'ids_stations.csv'
df = pd.read_csv(csv_path)

# Créer une nouvelle colonne 'Brand_Name' et la remplir en utilisant l'API
df['Brand_Name'] = df.apply(get_name_from_api, axis=1)

# Enregistrez le DataFrame mis à jour dans le même fichier CSV
df.to_csv(csv_path, index=False)

print("Opération terminée.")

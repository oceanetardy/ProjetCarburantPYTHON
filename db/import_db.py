import sqlite3
import json

file_encoding = 'utf-8'


with open('cache/cache_file.json', 'r', encoding=file_encoding) as file:
    data_list = json.load(file)


# Établir une connexion à la base de données (crée le fichier si inexistant)
conn = sqlite3.connect('db/stations_data.db')

# Créer un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Créer la table pour stocker les données si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY,
        latitude TEXT,
        longitude REAL,
        cp TEXT,
        pop TEXT,
        adresse TEXT,
        ville TEXT,
        horaires TEXT,
        services TEXT,
        prix TEXT,
        geom TEXT,
        gazole_maj TEXT,
        gazole_prix TEXT,
        sp95_maj TEXT,
        sp95_prix TEXT,
        e85_maj TEXT,
        e85_prix TEXT,
        gplc_maj TEXT,
        gplc_prix TEXT,
        e10_maj TEXT,
        e10_prix TEXT,
        sp98_maj TEXT,
        sp98_prix TEXT,
        carburants_disponibles TEXT,
        carburants_indisponibles TEXT,
        horaires_automate_24_24 TEXT,
        services_service TEXT,
        departement TEXT,
        code_departement TEXT,
        region TEXT,
        code_region TEXT,
        marque TEXT,
        nom TEXT
    )
''')

# Insérer chaque enregistrement dans la table
for data in data_list:

    horaires_str = json.dumps(data['horaires'])
    print(f"{horaires_str}")

    services_str = json.dumps(data['services'])
    prix_str = json.dumps(data['prix'])
    geom_str = json.dumps(data['geom'])
    carburants_disponibles_str = json.dumps(data['carburants_disponibles'])
    carburants_indisponibles_str = json.dumps(data['carburants_indisponibles'])
    services_service_str = json.dumps(data['services_service'])

    cursor.execute('''
        INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['id'], data['latitude'], data['longitude'], data['cp'], data['pop'], data['adresse'], data['ville'],
          horaires_str, services_str, prix_str, geom_str, data['gazole_maj'], data['gazole_prix'], data['sp95_maj'],
          data['sp95_prix'], data['e85_maj'], data['e85_prix'], data['gplc_maj'], data['gplc_prix'], data['e10_maj'],
          data['e10_prix'], data['sp98_maj'], data['sp98_prix'], carburants_disponibles_str, carburants_indisponibles_str,
          data['horaires_automate_24_24'], services_service_str, data['departement'], data['code_departement'],
          data['region'], data['code_region'], data['marque'], data['nom']))

# Valider les modifications et fermer la connexion
conn.commit()
conn.close()

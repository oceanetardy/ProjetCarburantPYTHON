import sqlite3
import json

# Fonction pour créer la base de données et les tables
def create_tables():
    conn = sqlite3.connect('db/stations_data.db')
    cursor = conn.cursor()

    # Créer les tables nécessaires si elles n'existent pas déjà
    cursor.execute('''CREATE TABLE IF NOT EXISTS Station (
                        id INTEGER PRIMARY KEY,
                        nom TEXT,
                        adresse TEXT,
                        latitude REAL,
                        longitude REAL,
                        cp TEXT,
                        ville TEXT,
                        departement TEXT,
                        code_departement TEXT,
                        region TEXT,
                        code_region TEXT,
                        marque TEXT,
                        horaires_automate_24_24 TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Service (
                        id INTEGER PRIMARY KEY,
                        nom TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Station_Service (
                        station_id INTEGER,
                        service_id INTEGER,
                        PRIMARY KEY (station_id, service_id),
                        FOREIGN KEY (station_id) REFERENCES Station(id),
                        FOREIGN KEY (service_id) REFERENCES Service(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Carburant (
                        id INTEGER PRIMARY KEY,
                        nom TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Prix (
                        id INTEGER PRIMARY KEY,
                        station_id INTEGER,
                        carburant_id INTEGER,
                        prix REAL,
                        maj TEXT,
                        FOREIGN KEY (station_id) REFERENCES Station(id),
                        FOREIGN KEY (carburant_id) REFERENCES Carburant(id)
                    )''')

    conn.commit()
    conn.close()

# Fonction pour insérer les données JSON d'une station dans la base de données
# Fonction pour insérer les données JSON d'une station dans la base de données
def insert_data_from_json(station_data):
    conn = sqlite3.connect('db/stations_data.db')
    cursor = conn.cursor()

    try:
        # Insérer les données de la station
        station_values = (station_data['id'], station_data.get('nom', ''), station_data.get('adresse', ''),
                          station_data.get('latitude', 0), station_data.get('longitude', 0),
                          station_data.get('cp', ''), station_data.get('ville', ''),
                          station_data.get('departement', ''), station_data.get('code_departement', ''),
                          station_data.get('region', ''), station_data.get('code_region', ''),
                          station_data.get('marque', ''), station_data.get('horaires_automate_24_24', ''))
        cursor.execute('''INSERT OR IGNORE INTO Station (id, nom, adresse, latitude, longitude, cp, ville, 
                          departement, code_departement, region, code_region, marque, horaires_automate_24_24) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', station_values)

        # Insérer les services de la station
        for service in station_data.get('services', {}).get('service', []):
            cursor.execute('''INSERT OR IGNORE INTO Service (nom) VALUES (?)''', (service,))
            service_id = cursor.lastrowid
            cursor.execute('''INSERT OR IGNORE INTO Station_Service (station_id, service_id) VALUES (?, ?)''',
                           (station_data['id'], service_id))

        # Insérer les prix des carburants
        for prix in station_data.get('prix', []):
            cursor.execute('''INSERT OR IGNORE INTO Carburant (nom) VALUES (?)''', (prix['@nom'],))
            carburant_id = cursor.lastrowid
            prix_values = (station_data['id'], carburant_id, prix['@valeur'], prix['@maj'])
            cursor.execute('''INSERT OR IGNORE INTO Prix (station_id, carburant_id, prix, maj) VALUES (?, ?, ?, ?)''',
                           prix_values)

        conn.commit()
        print(f"Données pour la station avec l'ID {station_data['id']} insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données pour la station avec l'ID {station_data['id']}: {str(e)}")
    finally:
        conn.close()



# Charger les données JSON depuis un fichier
with open('cache/cache_file.json', 'r', encoding='utf-8') as file:
    json_data_list = json.load(file)

# Créer les tables dans la base de données
create_tables()

# Insérer les données JSON de chaque station dans la base de données
for station_data in json_data_list:
    insert_data_from_json(station_data)

print("Les données ont été insérées avec succès dans la base de données.")

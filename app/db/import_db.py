import sqlite3
import json
import os

# Obtenir le chemin absolu du répertoire courant
base_dir = os.path.abspath(os.path.dirname(__file__))

# Définir les chemins de la base de données et du fichier de cache
db_path = os.path.join(base_dir, '..', 'db', 'stations_data.db')
cache_file_path = os.path.join(base_dir, '..', 'cache', 'cache_file.json')

def create_tables():
    # Créer le répertoire de la base de données s'il n'existe pas
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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
                        horaires_automate_24_24 TEXT,
                        UNIQUE(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Service (
                        id INTEGER PRIMARY KEY,
                        nom TEXT UNIQUE
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
                        nom TEXT UNIQUE
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

def insert_data_from_json(station_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Validation des données d'entrée
        validate_station_data(station_data)

        # Début de la transaction explicite
        cursor.execute("BEGIN")

        # Insertion des données de la station
        insert_station_data(cursor, station_data)

        # Insertion des services de la station
        insert_station_services(cursor, station_data)

        # Insertion des prix des carburants
        insert_fuel_prices(cursor, station_data)

        # Validation de la transaction
        conn.commit()
        print(f"Données pour la station avec l'ID {station_data['id']} insérées avec succès depuis le cache.")
    except Exception as e:
        # Journalisation des erreurs
        log_error(f"Erreur lors de l'insertion des données pour la station avec l'ID {station_data['id']}: {str(e)}")
        # Annulation de la transaction en cas d'erreur
        conn.rollback()
    finally:
        conn.close()

def validate_station_data(station_data):
    # Ajoutez ici votre logique de validation des données d'entrée
    pass

def insert_station_data(cursor, station_data):
    # Insertion des données de la station
    station_values = (
        int(station_data['id']),
        station_data.get('nom', ''),
        station_data.get('adresse', ''),
        float(station_data.get('latitude', 0)),
        float(station_data.get('longitude', 0)),
        station_data.get('cp', ''),
        station_data.get('ville', ''),
        station_data.get('departement', ''),
        station_data.get('code_departement', ''),
        station_data.get('region', ''),
        station_data.get('code_region', ''),
        station_data.get('marque', ''),
        station_data.get('horaires_automate_24_24', '')
    )
    cursor.execute('''INSERT OR IGNORE INTO Station (id, nom, adresse, latitude, longitude, cp, ville, 
                      departement, code_departement, region, code_region, marque, horaires_automate_24_24) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', station_values)

def insert_station_services(cursor, station_data):
    # Insertion des services de la station
    services_json = station_data.get('services', '{}')
    if services_json:
        services = json.loads(services_json).get('service', [])
        for service in services:
            # Vérifier si le nom du service contient plus d'un caractère
            if len(service) > 1:
                # Vérifier si le service existe déjà
                cursor.execute('''SELECT id FROM Service WHERE nom = ?''', (service,))
                service_row = cursor.fetchone()

                if service_row:
                    service_id = service_row[0]
                else:
                    # Insérer le service s'il n'existe pas
                    cursor.execute('''INSERT INTO Service (nom) VALUES (?)''', (service,))
                    service_id = cursor.lastrowid

                # Insérer la liaison entre la station et le service
                cursor.execute('''INSERT OR IGNORE INTO Station_Service (station_id, service_id) VALUES (?, ?)''',
                               (int(station_data['id']), service_id))

def insert_fuel_prices(cursor, station_data):
    # Insertion des prix des carburants
    prix_json = station_data.get('prix', '[]')
    if prix_json:
        prix_list = json.loads(prix_json)
        for prix in prix_list:
            if isinstance(prix, dict):  # Vérification si l'élément est un dictionnaire
                carburant_nom = prix.get('@nom', '')
                carburant_valeur = float(prix.get('@valeur', 0))
                maj = prix.get('@maj', '')
                # Vérifier si le carburant existe déjà
                cursor.execute('''SELECT id FROM Carburant WHERE nom = ?''', (carburant_nom,))
                carburant_row = cursor.fetchone()
                if carburant_row:
                    carburant_id = carburant_row[0]
                else:
                    # Si le carburant n'existe pas, l'insérer
                    cursor.execute('''INSERT INTO Carburant (nom) VALUES (?)''', (carburant_nom,))
                    carburant_id = cursor.lastrowid
                # Insérer le prix avec l'ID correct du carburant
                prix_values = (int(station_data['id']), carburant_id, carburant_valeur, maj)
                cursor.execute('''INSERT OR IGNORE INTO Prix (station_id, carburant_id, prix, maj) VALUES (?, ?, ?, ?)''',
                               prix_values)

def log_error(message):
    print(message)

if os.path.exists(cache_file_path):
    with open(cache_file_path, 'r', encoding='utf-8') as file:
        json_data_list = json.load(file)

    create_tables()

    for station_data in json_data_list:
        insert_data_from_json(station_data)

    print("Les données ont été insérées avec succès dans la base de données depuis le cache.")
else:
    print(f"Le fichier de cache {cache_file_path} n'existe pas.")

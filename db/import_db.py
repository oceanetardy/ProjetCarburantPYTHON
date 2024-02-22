import sqlite3
import json

def create_tables():
    conn = sqlite3.connect('db/stations_data.db')
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
    conn = sqlite3.connect('db/stations_data.db')
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
        print(f"Données pour la station avec l'ID {station_data['id']} insérées avec succès.")
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
            cursor.execute('''INSERT OR IGNORE INTO Service (nom) VALUES (?)''', (service,))
            service_id = cursor.lastrowid
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

                # Vérifier si le carburant existe dans la table Carburant
                cursor.execute("SELECT id FROM Carburant WHERE nom=?", (carburant_nom,))
                result = cursor.fetchone()
                if result:
                    carburant_id = result[0]

                    # Insérer le prix seulement si le carburant existe
                    prix_values = (int(station_data['id']), carburant_id, carburant_valeur, maj)
                    cursor.execute(
                        '''INSERT OR IGNORE INTO Prix (station_id, carburant_id, prix, maj) VALUES (?, ?, ?, ?)''',
                        prix_values)
                else:
                    # Gérer le cas où le carburant n'existe pas
                    print(
                        f"Le carburant '{carburant_nom}' n'existe pas dans la table Carburant. Ignorer l'insertion du prix.")
    else:
        print("Aucun prix de carburant trouvé pour cette station.")

def log_error(message):
    # Journalisez les erreurs dans un fichier de journal ou imprimez-les pour le débogage
    print(message)

def update_fuel_prices(cursor):
    cursor.execute("SELECT DISTINCT carburant_id FROM Prix")
    carburant_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM Carburant")
    valid_carburant_ids = [row[0] for row in cursor.fetchall()]

    invalid_ids = [id for id in carburant_ids if id not in valid_carburant_ids]

    if invalid_ids:
        print("IDs de carburants invalides trouvés dans la table des prix : ", invalid_ids)
        for invalid_id in invalid_ids:
            # Trouver le carburant correspondant dans la table Carburant
            cursor.execute("SELECT id FROM Carburant ORDER BY id LIMIT 1")
            valid_id = cursor.fetchone()[0]

            # Mettre à jour l'ID du carburant dans la table des prix
            cursor.execute("UPDATE Prix SET carburant_id=? WHERE carburant_id=?", (valid_id, invalid_id))

        print("Les IDs de carburants invalides dans la table des prix ont été mis à jour.")

# Code principal
with open('cache/cache_file.json', 'r', encoding='utf-8') as file:
    json_data_list = json.load(file)

create_tables()

for station_data in json_data_list:
    insert_data_from_json(station_data)

# Mettre à jour les IDs de carburants invalides dans la table des prix
conn = sqlite3.connect('db/stations_data.db')
cursor = conn.cursor()
update_fuel_prices(cursor)
conn.commit()
conn.close()

print("Les données ont été insérées avec succès dans la base de données.")

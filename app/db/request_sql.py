import sqlite3


def get_carburant_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    carburants = ["Gazole", "E10", "SP98", "SP95", "E8", "GPLc"]
    carburant_info = {}

    for carburant in carburants:
        cursor.execute('''
            SELECT c.nom, MAX(p.prix), s.nom, s.adresse, s.ville, s.cp
            FROM Prix p
            JOIN Station s ON p.station_id = s.id
            JOIN Carburant c ON p.carburant_id = c.id
            WHERE c.nom = ?
            GROUP BY p.station_id
            ORDER BY p.prix DESC
            LIMIT 1
        ''', (carburant,))
        max_price_info = cursor.fetchone()

        cursor.execute('''
            SELECT c.nom, MIN(p.prix), s.nom, s.adresse, s.ville, s.cp
            FROM Prix p
            JOIN Station s ON p.station_id = s.id
            JOIN Carburant c ON p.carburant_id = c.id
            WHERE c.nom = ?
            GROUP BY p.station_id
            ORDER BY p.prix ASC
            LIMIT 1
        ''', (carburant,))
        min_price_info = cursor.fetchone()

        cursor.execute('''
            SELECT c.nom, AVG(p.prix)
            FROM Prix p
            JOIN Carburant c ON p.carburant_id = c.id
            WHERE c.nom = ?
        ''', (carburant,))
        avg_price_info = cursor.fetchone()

        carburant_info[carburant] = {
            "max_price": max_price_info,
            "min_price": min_price_info,
            "avg_price": avg_price_info[1] if avg_price_info else None
        }

    conn.close()
    return carburant_info

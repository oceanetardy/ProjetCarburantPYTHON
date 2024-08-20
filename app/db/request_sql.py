import sqlite3
import re

def get_carburant_info(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    carburants = ["Gazole", "E10", "SP98", "SP95", "E85", "GPLc"]
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

import os
import matplotlib.pyplot as plt

def generate_carburant_plot(carburant_info, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    carburants = list(carburant_info.keys())
    avg_prices = [carburant_info[carburant]['avg_price'] for carburant in carburants]

    # Vérifier et remplacer les valeurs None par 0
    avg_prices = [price if price is not None else 0 for price in avg_prices]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(carburants, avg_prices, color='burlywood')
    plt.xlabel('Carburants')
    plt.ylabel('Prix moyen (€)')
    plt.title('Prix moyen des carburants en France')
    plt.tight_layout()

    # Ajouter le prix moyen au-dessus de chaque barre
    for bar, price in zip(bars, avg_prices):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f'{price:.2f} €',
            ha='center',
            va='bottom'
        )

    plot_path = os.path.join(output_folder, 'carburant_avg_prices.png')
    plt.savefig(plot_path, transparent=True)
    plt.close()

    return plot_path



def search_stations_by_postal_code(db_path, department_code):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        SELECT s.nom, s.adresse, s.ville, s.cp
        FROM Station s
        WHERE s.cp LIKE ?
    '''
    cursor.execute(query, (department_code + '%',))
    stations = cursor.fetchall()

    conn.close()
    return stations

def is_valid_postal_code(postal_code):
    # Vérifie que le code postal est exactement 5 chiffres
    return re.fullmatch(r'\d{5}', postal_code) is not None

def get_carburant_prices_by_postal_code(db_path, postal_code):
    if not is_valid_postal_code(postal_code):
        return None, "Code postal non valide. Veuillez entrer un code postal à 5 chiffres."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        SELECT 
            COALESCE(s.nom, 'Nom de station non disponible') AS station_nom, 
            COALESCE(s.adresse, 'Adresse non disponible') AS adresse, 
            COALESCE(s.ville, 'Ville non disponible') AS ville, 
            COALESCE(s.cp, 'CP non disponible') AS cp,
            COALESCE(MAX(CASE WHEN c.nom = 'Gazole' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS Gazole,
            COALESCE(MAX(CASE WHEN c.nom = 'E10' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS E10,
            COALESCE(MAX(CASE WHEN c.nom = 'SP98' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS SP98,
            COALESCE(MAX(CASE WHEN c.nom = 'SP95' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS SP95,
            COALESCE(MAX(CASE WHEN c.nom = 'E85' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS E85,
            COALESCE(MAX(CASE WHEN c.nom = 'GPLc' THEN p.prix ELSE NULL END), 'Carburant non disponible') AS GPLc
        FROM Station s
        LEFT JOIN Prix p ON s.id = p.station_id
        LEFT JOIN Carburant c ON p.carburant_id = c.id
        WHERE s.cp = ?
        GROUP BY s.nom, s.adresse, s.ville, s.cp
    '''

    cursor.execute(query, (postal_code,))
    prices = cursor.fetchall()

    conn.close()

    if not prices:
        return None, "Aucune station trouvée pour le code postal spécifié."

    return prices, None
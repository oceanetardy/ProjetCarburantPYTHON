import os
import sqlite3
import matplotlib.pyplot as plt



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

def generate_carburant_plot(carburant_info, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    carburants = list(carburant_info.keys())
    avg_prices = [carburant_info[carburant]['avg_price'] for carburant in carburants]

    # Vérifier et remplacer les valeurs None par 0
    avg_prices = [price if price is not None else 0 for price in avg_prices]

    plt.figure(figsize=(10, 6))
    plt.bar(carburants, avg_prices, color='skyblue')
    plt.xlabel('Carburants')
    plt.ylabel('Prix moyen (€)')
    plt.title('Prix moyen des carburants en France')
    plt.tight_layout()

    plot_path = os.path.join(output_folder, 'carburant_avg_prices.png')
    plt.savefig(plot_path, transparent=True)
    plt.close()

    return plot_path

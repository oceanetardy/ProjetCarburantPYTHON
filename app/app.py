from flask import Flask, render_template, request
import os
from db.request_sql import get_carburant_info, generate_carburant_plot, search_stations_by_department, \
    get_carburant_prices_by_postal_code

app = Flask(__name__)
IMG_FOLDER = os.path.join("static", "IMG")
PLOT_FOLDER = os.path.join("static", "plot")
app.config["IMG_FOLDER"] = IMG_FOLDER
app.config["PLOT_FOLDER"] = PLOT_FOLDER
logoGasGenius = os.path.join(app.config["IMG_FOLDER"], "logoGasGenius.png")
gasstation = os.path.join(app.config["IMG_FOLDER"], "gasstation.jpg")
gaspump = os.path.join(app.config["IMG_FOLDER"], "gaspump.jpg")
feinte = os.path.join(app.config["IMG_FOLDER"], "feinte.png")

@app.route('/')
def home():
    return render_template('home.html', logo=logoGasGenius, gasstation=gasstation)

@app.route('/statistiques-nationales')
def statisticNational():
    db_path = 'db/stations_data.db'
    carburant_info = get_carburant_info(db_path)
    plot_path = generate_carburant_plot(carburant_info, app.config["PLOT_FOLDER"])
    return render_template('nationalstatistic.html', logo=logoGasGenius, gasstation=gasstation, gaspump=gaspump, carburant_info=carburant_info, plot_path=plot_path)

@app.route('/rechercher', methods=['GET', 'POST'])
def findstation():
    db_path = 'db/stations_data.db'
    if request.method == 'POST':
        postal_code = request.form.get('department')
        if postal_code:
            stations = search_stations_by_department(db_path, postal_code)
            prices = get_carburant_prices_by_postal_code(db_path, postal_code)
        else:
            stations = []
            prices = []
    else:
        stations = []
        prices = []

    return render_template('findstation.html', logo=logoGasGenius, gasstation=gasstation, stations=stations, prices=prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

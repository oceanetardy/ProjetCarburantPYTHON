from flask import Flask, render_template
import os
from db.request_sql import get_carburant_info, generate_carburant_plot

app = Flask(__name__)
IMG_FOLDER = os.path.join("static", "IMG")
PLOT_FOLDER = os.path.join("static", "plot")
app.config["IMG_FOLDER"] = IMG_FOLDER
app.config["PLOT_FOLDER"] = PLOT_FOLDER
logoGasGenius = os.path.join(app.config["IMG_FOLDER"], "logoGasGenius.png")
gasstation = os.path.join(app.config["IMG_FOLDER"], "gasstation.jpg")
gaspump = os.path.join(app.config["IMG_FOLDER"], "gaspump.jpg")
# Image pour visuel seulement matplotlib -> Sera géré en Python
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
@app.route('/rechercher')
def findstation():
	return render_template('findstation.html', logo=logoGasGenius, gasstation=gasstation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

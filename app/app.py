from flask import Flask, render_template
import os

app = Flask(__name__)
IMG_FOLDER = os.path.join("static", "IMG")
app.config["IMG_FOLDER"] = IMG_FOLDER
logoGasGenius = os.path.join(app.config["IMG_FOLDER"], "logoGasGenius.png")
gasstation = os.path.join(app.config["IMG_FOLDER"], "gasstation.jpg")

@app.route('/')
def home():
	return render_template('home.html', logo=logoGasGenius, gasstation=gasstation)

@app.route('/statistiques-nationales')
def statisticNational():
	return render_template('nationalstatistic.html', logo=logoGasGenius, gasstation=gasstation)

@app.route('/rechercher')
def findstation():
	return render_template('findstation.html', logo=logoGasGenius, gasstation=gasstation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

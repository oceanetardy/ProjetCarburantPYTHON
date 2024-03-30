from flask import Flask, render_template
import os

app = Flask(__name__)
IMG_FOLDER = os.path.join("static", "IMG")
app.config["IMG_FOLDER"] = IMG_FOLDER


@app.route('/')
def home():
	logoGasGenius = os.path.join(app.config["IMG_FOLDER"], "logoGasGenius.png")
	gasstation = os.path.join(app.config["IMG_FOLDER"], "gasstation.jpg")
	return render_template('home.html', logo=logoGasGenius, gasstation=gasstation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

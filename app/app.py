from flask import Flask, render_template
import os

app = Flask(__name__)
IMG_FOLDER = os.path.join("static", "IMG")
app.config["IMG_FOLDER"] = IMG_FOLDER  # A vérifier


@app.route('/')
def hello():
	logoGasGenius = os.path.join(app.config["IMG_FOLDER"], "logoGasGenius.png")
	return render_template('templateHome.html', logo=logoGasGenius)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('templateHome.html', content="Hello World!", test='test2')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
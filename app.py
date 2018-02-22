from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/test")
def test():
	return "test123";

if __name__ == "__main__":
	app.run()

# http://flask.pocoo.org/docs/0.12/quickstart/ #
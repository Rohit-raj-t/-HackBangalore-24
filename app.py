from flask import Flask, render_template
from database import execute_query

app = Flask(__name__)


@app.route("/")
def par():
    return render_template("index6.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)

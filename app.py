""" Koala Identification App

This app is designed to connect a live feed from a drone to an AI model that
can identify koalas in the feed. The app will then display the feed with
bounding boxes around the koalas.
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main() -> str:
    return render_template("index.html")


@app.route("/live-feed")
def live_feed() -> str:
    return render_template("live-feed.html")


if __name__ == "__main__":
    app.run(debug=True)

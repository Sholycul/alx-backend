#!/usr/bin/env python3

"""Module for running forst instance of our app"""

from flask import Flask, render_template

app = Flask(_name_)


@app.route("/")
def index():
    """Home page"""
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(debug=True)

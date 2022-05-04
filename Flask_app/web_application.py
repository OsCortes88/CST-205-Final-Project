from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap5
from PIL import Image

# Starts Flask application
app = Flask(__name__)

# Used for HTML fomrmating/styles
bootstrap = Bootstrap5(app)

@app.route('/')
def run_home():
    return render_template("upload.html")

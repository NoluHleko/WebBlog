from flask import Flask, render_template
from myblog import app, db


@app.route('/')
def home():
    return render_template('index.html')
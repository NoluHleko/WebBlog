from flask import Flask, render_template
from myblog import app

@app.route('/')
def index():
    render_template('index.html')
from myblog import app,db
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('index.html')
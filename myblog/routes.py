from myblog import app,db
from flask import Flask, render_template
from .models import User

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('admin/register.html')
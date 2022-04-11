import bcrypt
from flask import Flask, flash, render_template, request, redirect, url_for, current_app
from myblog import app,db, bcrypt, login_manager

from .models import User
import os
import secrets

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path,'static/img', photo_name)
    photo.save(file_path)
    return photo_name

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'] )
def register():
    if request.method == "POST": #Checks if user and email already exist and flashes a message
        user=User.query.filter_by(username = request.form.get('username')).first()
        if user:
            flash("The username already exists!",'warning')
            return redirect(url_for('register'))
        email=User.query.filter_by(email=request.form.get('email')).first()
        if email:
            flash("The email is taken!")
            return redirect(url_for('register','warning'))
        name= request.form.get("name")
        username= request.form.get("username")
        email= request.form.get("email")
        password= request.form.get("password")
        repeat_password= request.form.get("repeat_password")
        if password != repeat_password:
            flash('passwords do not match','warning')
            return redirect(url_for('register'))
        password_hash=bcrypt.generate_password_hash(password)
        users = User(name=name, username=username, email=email, password=password_hash)
        db.session.add(users)
        db.session.commit()
        flash('Thank you for registration', 'success')
        return redirect (url_for ("dashboard"))

        
    return render_template('admin/register.html')

from flask_login import login_user, login_required, current_user, logout_user

#######################################################Login###############################
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method=="POST":
        user=User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next =request.args.get('next')
            return redirect(next or url_for('dashboard'))
        flash('Wrong Password, Please try again', 'danger')
    return render_template('admin/login.html')

#######################################################Logout###############################
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@app.route('/addpost')
@login_required
def addpost():
    return render_template ('admin/addpost.html')

from flask import Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post
from myblog import app,db, bcrypt, login_manager


auth = Blueprint("auth",__name__)

#######################################################Register#######################################

@auth.route('/register', methods =['GET', 'POST'] )
def register():
    if request.method == "POST": #Checks if user and email already exist and flashes a message
        user=User.query.filter_by(username = request.form.get('username')).first()
        if user:
            flash("The username already exists!",'warning')
            return redirect(url_for('auth.register'))
        email=User.query.filter_by(email=request.form.get('email')).first()
        if email:
            flash("The email is taken!",'warning')
            return redirect(url_for('auth.register'))
        name= request.form.get("name")
        username= request.form.get("username")
        email= request.form.get("email")
        password= request.form.get("password")
        repeat_password= request.form.get("repeat_password")
        if password != repeat_password:
            flash('passwords do not match','warning')
            return redirect(url_for('auth.register'))
        password_hash=bcrypt.generate_password_hash(password)
        users = User(name=name, username=username, email=email, password=password_hash)
        db.session.add(users)
        db.session.commit()
        flash('Thank you for registration', 'success')
        return redirect (url_for ("views.dashboard"))

        
    return render_template('admin/register.html')

from flask_login import login_user, login_required, current_user, logout_user

#######################################################Login and Logout###############################
@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method=="POST":
        user=User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next =request.args.get('next')
            return redirect(next or url_for('views.dashboard'))
        flash('Wrong Password, Please try again', 'danger')
    return render_template('admin/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




<<<<<<< HEAD
import bcrypt
from flask import Flask, flash, render_template, request, redirect, url_for
from myblog import app,db, Bcrypt
from .models import User
=======
from myblog import app,db
from flask import Flask, render_template
>>>>>>> parent of 2c0454d... making progress


@app.route('/')
def home():
<<<<<<< HEAD
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'] )
def register():
    if request.method == "POST": #Checks if user and email already exist and flashes a message
        user=User.query.filter_by(username = request.form.get('username')).first()
        if user:
            flash("The username already exists!",'warning')
            return redirect(url_for('register'))
        email=User.query.filter_by(email = request.form.get('email')).first()
        if email:
            flash("The email is taken!")
            return redirect(url_for('register','warning'))
        name= request.form.get("name")
        username= request.form.get("username")
        email= request.form.get("email")
        password= request.form.get("password")
        repeat_password= request.form.get("repeat_password",'warning')
        if password != repeat_password:
            flash('passwords do not match','warning')
            return redirect(url_for('register'))
        password_hash =bcrypt.generate_password_hash(password)
        users = User (name=name, username=username, email=email, password=password_hash)
        db.ession.add(users)
        db.session.commit()
        flash('THhank you for registration', 'success')
        return redirect (url_for ("dashboard"))

        
    return render_template('admin/register.html')
=======
    return render_template('index.html')
>>>>>>> parent of 2c0454d... making progress

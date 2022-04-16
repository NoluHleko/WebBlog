from crypt import methods
from turtle import title
import bcrypt
from flask import Flask, flash, render_template, request, redirect, url_for, current_app
from myblog import app,db, bcrypt, login_manager

from .models import User, Post
import os
import secrets
from slugify import slugify
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path,'static/assets/images', photo_name)
    photo.save(file_path)
    return photo_name

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

@app.route ('/post/<int:post_id>/<string:slug>', methods=['POST', 'GET'])
def post(post_id, slug):
    post = Post.query.get_or_404 (post_id)
    return render_template('Post.html', post=post)


@app.route('/aboutme')
def aboutme():
    return render_template('About-Me.html')

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
    posts= Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)


@app.route('/addpost', methods=['POST', 'GET'])
@login_required
def addpost():
    if request.method =="POST":
        title = request.form.get('title')
        body = request.form.get('content')
        photo = save_images(request.files.get('photo'))
        post= Post(title=title, body=body, image=photo, author =current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been submitted", 'success')
        return redirect('dashboard')
    return render_template ('admin/addpost.html')

@app.route ('/updatepost/<id>', methods=["POST", "GET"])
@login_required
def updatepost(id):
    post = Post.query.get_or_404(id)
    if request.method =="POST":
        if request.files.get('photo'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/assets/images/' + post.image))
                post.image = save_images(request.files.get('photo'))
            except:
                post.image = save_images(request.files.get('photo'))
        post.title = request.form.get('title')
        post.body = request.form.get('content')
        db.session.commit()
        flash ('Post updated succesfully', 'success')
        return redirect (url_for('dashboard'))
    return render_template('admin/updatepost.html', post=post)

@app.route('/delete/<id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    try:
        os.unlink(os.path.join(current_app.root_path,'static/assets/images/' + post.image))
        db.session.delete(post)
    except:
        db.session.delete(post)
    db.session.commit()
    flash ('Post deleted succesfully', 'success')
    return redirect (url_for('dashboard'))

@app.route('/contactme', methods=['GET', 'POST'])
def contactme():
    if request.method == "POST":
         flash('message sent', 'success')
         return redirect (url_for('contactme'))
    return render_template ("contactMe.html")

@app.route('/love')
def love():
    return "love is for everyone"
from crypt import methods
import bcrypt
from flask import Blueprint, Flask, flash, render_template, request, redirect, url_for, current_app
from myblog import app,db, bcrypt, login_manager, auth

from .models import User, Post
import os
import secrets



views = Blueprint("views",__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path,'static/assets/images', photo_name)
    photo.save(file_path)
    return photo_name



@views.route('/')
@views.route('/home')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)



@views.route ('/post/<int:post_id>/<string:slug>', methods=['POST', 'GET'])
def post(post_id, slug):
    post = Post.query.get_or_404 (post_id)
    return render_template('Post.html', post=post)



@views.route('/aboutme')
def aboutme():
    return render_template('About-Me.html')



from flask_login import login_required, current_user


@views.route('/dashboard')
@login_required
def dashboard():
    posts= Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)

@views.route('/users')
@login_required
def users():
    users= User.query.order_by(User.id.desc()).all()
    return render_template('admin/users.html', users=users)


@views.route('/deleteuser/<id>')
@login_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    try:

        db.session.delete(user)
        
    except:
        db.session.delete(user)
    db.session.commit()
    flash ('The post was successfully deleted', 'danger')
    return redirect (url_for('views.users'))

    

@views.route('/addpost', methods=['POST', 'GET'])
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



@views.route ('/updatepost/<id>', methods=["POST", "GET"])
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
        return redirect (url_for('views.dashboard'))
    return render_template('admin/updatepost.html', post=post)



@views.route('/delete/<id>')
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
    return redirect (url_for('views.dashboard'))



@views.route('/contactme', methods=['GET', 'POST'])
def contactme():
    if request.method == "POST":
         flash('message sent', 'success')
         return redirect (url_for('views.contactme'))
    return render_template ("contactMe.html")




@views.route('/travel')
def travel():
    return render_template ('travel.html')
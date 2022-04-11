from cProfile import Profile
from email.policy import default
from myblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150))
    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    image=db.Column(db.String(120), default='image.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User',backref=db.backref('author', lazy=True))
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()
db.session.commit()


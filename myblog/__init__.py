from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager






app = Flask(__name__)
login_manager = LoginManager(app)




#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weblog2022.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://iznpzyqrqaiogp:76f9a87a5fbb8a5b9d1d451191b9802ec51a81603bcebe5c598a26f3d4c25bfd@ec2-3-229-252-6.compute-1.amazonaws.com:5432/d6r6q00quh18bi'

app.config['SECRET_KEY']='NOSI199one'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .models import User, Post
from myblog import views,db,auth

from .views import views
from .auth import auth

app.register_blueprint (views, url_prefix ="/")
app.register_blueprint(auth,url_prefix ="/")



login_manager.login_view = "auth.login"
login_manager.login_message_category = ""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager






app = Flask(__name__)

login_manager = LoginManager(app)

from dotenv import load_dotenv

load_dotenv()

from os import environ

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weblog2022.db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

app.config['SECRET_KEY']= environ.get('SECRET_KEY')
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
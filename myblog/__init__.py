from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager






app = Flask(__name__)
login_manager = LoginManager(app)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weblog2022.db'
app.config['SECRET_KEY']='NOSI199one'
db = SQLAlchemy(app)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from .models import User, Post
from myblog import views,db,auth

from .views import views
from .auth import auth

app.register_blueprint (views, url_prefix ="/")
app.register_blueprint(auth,url_prefix ="/")



login_manager.login_view = "auth.login"
login_manager.login_message_category = ""
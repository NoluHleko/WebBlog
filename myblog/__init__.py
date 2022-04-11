from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog.db'
app.config['SECRET_KEY']='NOSI199one'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from .models import User
from myblog import routes,db

from flask_login import LoginManager
login_manager = LoginManager()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
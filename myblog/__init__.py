from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myblog.db'
db = SQLAlchemy(app)

from myblog import routes
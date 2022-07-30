from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from .config import Config


# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)

# ORM instance
db = SQLAlchemy(app)
#db.create_all()
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'

# By design
from app import view, models, func

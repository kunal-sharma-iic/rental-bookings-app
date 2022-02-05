from ensurepip import bootstrap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

"""flask app configuration and database connection using ORM """

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rentals:bookings@localhost/rentals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'yhapkikeyh'
bootstrap = Bootstrap(app)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


db = SQLAlchemy(app)
login = LoginManager()
login.init_app(app)

from app import models
from app import views

login.login_view = 'login'
login.login_message = "Please log in!"
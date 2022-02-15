from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '1am50v3rys3cr3t'
# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorties.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flask_url_shorten2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flask_shorty import routes


# Create Database
@app.before_first_request
def create_tables():
    db.create_all()
    
from flask import g
from scraper import getLinks
from flask_github import GitHub
from flask_session import Session
import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import MetaData

meta = MetaData()
app = Flask(__name__)


# Secret keys!
app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_name = 'testdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

github = GitHub(app)

app.secret_key = os.environ['APP_SECRET_KEY']

#database stuff below here

class Listings(db.Model):
    url = db.Column(db.String(120), primary_key=True)
    imagesLink = db.Column(db.String(120), unique=True, nullable=False)
    titles = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    dateAndTime = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<Listings %r>' % self.url

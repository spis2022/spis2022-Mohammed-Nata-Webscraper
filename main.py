from flask import g
from scraper import getLinks
from flask_github import GitHub
from flask_session import Session
import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session
from pymongo import MongoClient
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
# from sqlalchemy import MetaData
# from sqlalchemy.orm import joinedload
# from flask_pymongo import PyMongo
app = Flask(__name__)


# Secret keys!
app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = MongoClient(os.environ['MONGO_URI'])
db = client.database

github = GitHub(app)

app.secret_key = os.environ['APP_SECRET_KEY']

@app.route('/')
def render_home():
    return render_template('home.html')

#refreshes database with new info from scraper
@app.route('/load-db')
def render_load_db():
  links = getLinks()
  for key,value in links.items():
    # store value in mongoDB database
    db.listings.insert_one(value)
    print("storing record for", key)
  return "db loaded"

# github login stuff
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def new_user():
    return render_template("register.html")
    # return github.authorize()
  
@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        return "Authorization Failed"

    else:
      return "Authorization Succeeded"

@app.route('/listings')
def render_listings():
  # links = getLinks()
  # return render_template('scraper.html', links = links)
  pass
for listing in  db.listings.find():
  print(listing)

if __name__ == "__main__":
  pass
 # app.run(host='0.0.0.0')
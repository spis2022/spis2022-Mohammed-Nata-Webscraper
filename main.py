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
  databaseArchive = []
  newlyScraped = []
  listingsCursor = db.listings.find()
  for listing in listingsCursor:
    databaseArchive.append(listing['link'])  
  links = getLinks()
  for key,value in links.items():
    if key not in databaseArchive:
      print("new entry!!")
      db.listings.insert_one(value)
      print("storing record for", key)
    newlyScraped.append(key)
  for entry in databaseArchive:
    if entry not in newlyScraped:
      db.listings.delete_one({"link":entry})
      print("db deleted", entry)
  return "db loaded"

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        print(user.github_access_token)

@app.route('/login')
def login():
    return github.authorize()
  
@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
      return "Authorization Failed"
    else:
      return oauth_token

@app.route('/listings')
def render_listings():
  listingsCursor = db.listings.find()
  return render_template('listings.html', cursor = listingsCursor)
  pass
@app.route('/collapsingtest')
def render_collapse():
  return render_template('collapseTest.html')

listingsCursor = db.listings.find()
# for listing in listingsCursor:
#   print(type(listing))
#   print(len(listing.keys()))
#   print(listing)

if __name__ == "__main__":
  # pass
  app.run(host='0.0.0.0')
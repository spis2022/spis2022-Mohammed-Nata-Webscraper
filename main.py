from flask import g
from scraper import getLinks
from flask_github import GitHub
from flask_session import Session
import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session
from pymongo import MongoClient
import bcrypt
import datetime
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

# @app.route('/')
# def render_home():
#     return render_template('home.html')

#refreshes database with new info from scraper
def update_time():
  if "username" in session:
    username = session['username']
    filter = {'username': username}
    new_values = { "$set": { 'date': datetime.datetime.now() } }
    db.logins.update_one(filter, new_values)
    print("time updated")

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

@app.route('/listings')
def render_listings():
  update_time()
  listingsCursor = db.listings.find()
  return render_template('listings.html', cursor = listingsCursor)
  pass

@app.route("/", methods=['post', 'get'])
def index():
  message = ''
  date = datetime.datetime.now()
  if "username" in session:
    return redirect(url_for("logged_in"))
  if request.method == "POST":
    username = request.form.get("username")
    
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    username_found = db.logins.find_one({"username": username})
    if username_found:
      message = 'This username already exists in database'
      return render_template('index.html', message=message)
    if password1 != password2:
      message = 'Passwords should match!'
      return render_template('index.html', message=message)
    else:
      hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
      user_input = {'username': username, 'password': hashed, 'date': date}
      db.logins.insert_one(user_input)
      
      user_data = db.logins.find_one({"username": username})
      new_username = user_data['username']

      return render_template('logged_in.html', username=new_username)
  return render_template('index.html')

@app.route('/logged_in')
def logged_in():
  if "username" in session:
    update_time()
    username = session["username"]
    return render_template('logged_in.html', username=username)
  else:
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
  message = 'Please login to your account'
  if "username" in session:
    return redirect(url_for("logged_in"))

  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    username_found = db.logins.find_one({"username": username})
    print(username)
    if username_found:
      username_val = username_found['username']
      passwordcheck = username_found['password']
      
      if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
          session["username"] = username_val
          return redirect(url_for('logged_in'))
      else:
        if "username" in session:
            return redirect(url_for("logged_in"))
        message = 'Wrong password'
        return render_template('login.html', message=message)
  else:
    message = 'username not found'
    return render_template('login.html', message=message)
  return render_template('login.html', message=message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
  if "username" in session:
    session.pop("username", None)
    return render_template("logout.html")
  else:
    return render_template('index.html')

def update_time():
  if "username" in session:
    username = session['username']
    filter = {'username': username}
    new_values = { "$set": { 'date': datetime.datetime.now() } }
    db.logins.update_one(filter, new_values)
    print("time updated")
  else:
    print('user not in session')
if __name__ == "__main__":
  # pass
  app.run(host='0.0.0.0')
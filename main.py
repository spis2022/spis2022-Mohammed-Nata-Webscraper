from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import g
from scraper import getLinks
from flask_github import GitHub
from flask_session import Session
import os
app = Flask(__name__)

# setting up github login
app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
github = GitHub(app)
@app.route('/')
def render_home():
    return render_template('home.html')
# github login stuff
@app.route('/login')
def login():
    return github.authorize()
  
@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        return "Authorization Failed"

    else:
      return "Authorization Succeeded"

@app.route('/scraper')
def render_scraper():
  links = getLinks()
  return render_template('scraper.html', links = links)


if __name__ == "__main__":
 app.run(host='0.0.0.0')
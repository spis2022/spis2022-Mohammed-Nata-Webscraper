from flask import Flask
from flask import render_template
from flask import request
from scraper import getLinks
app = Flask(__name__)
# dictionary for unique function

@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/scraper')
def render_scraper():
  links = getLinks()
  return render_template('scraper.html', links = links)
           
if __name__ == "__main__":
  app.run(host='0.0.0.0')

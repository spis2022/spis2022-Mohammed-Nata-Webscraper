import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# Setting up soup for the general area search page

def getLinks():
 url = requests.get('https://garagesalefinder.com/yard-sales/sammamish-wa/')
 soup = BeautifulSoup(url.text,'html.parser')

adtitles = soup.find("div", class_="small-9 columns").find_all("h2")
for title in adtitles: 
   print(title.text)
  
  # Will extract the links to garage sales from the website and put them into the list linkList
  # I think this is missing some links by only saving ones ending in gallery, figure out why not all links have gallery and if things will still work if I slap it on
links = {}  
for aTag in soup.find_all('a', {'href': True}):
     link = (aTag.get('href'))
if 'garagesalefinder' in link and 'gallery' in link:
      links[link] = {}
     
  # Will extract the corresponding title for each list in the same matching order
# linkToTitle = {}
  
# titleList = []
  
  # Setting up subsidiary soup of the first garage sale on the prior list
  # Intend to either make this a function or put it in a for loop so we can store all this info for every garage sale, but that's for later
  for link in links.keys():
    url2 = requests.get(str(link))
    soup2 = BeautifulSoup(url2.text,'html.parser')
  # Extracting the images and saving them to imageList

    imageList = []
  
    for images in soup2.find_all('img', {'data-lazy':True}):
      imageList.append(images.get('data-lazy'))
    links[link]['images']=imageList
  return links


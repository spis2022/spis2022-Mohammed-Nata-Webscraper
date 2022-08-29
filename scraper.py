import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import sqlite3

#Data base
# connection = sqlite3.connect("scraper.db")
# cursor = connection.cursor()

# Setting up soup for the general area search page
def getLinks(location='sammamish-wa'):
  # soup for listing page
  # change eventually
  response = requests.get('https://garagesalefinder.com/yard-sales/' + location + "/")
  soup = BeautifulSoup(response.text,'html.parser')
  # collects links of listings
  outerDict = {}  
  for aTag in soup.find_all('a', {'href': True}):
    link = (aTag.get('href'))
    if 'garagesalefinder' in link and 'gallery' not in link:
      outerDict[link] = {}
  # building inner dictionary     
  for link in outerDict.keys():
    responseListing = requests.get(str(link))
    soupD = BeautifulSoup(responseListing.text, 'html.parser')
    outerDict[link]['link'] = link
    outerDict[link]['location'] = location
    outerDict[link]['title'] = getTitle(soupD)
    outerDict[link]['description'] = getDescription(soupD)
    outerDict[link]['address'] = getAddress(soupD)
    outerDict[link]['dateAndTime'] = getDate(soupD)
    # Extracting the images and saving them to imageList
    # BELOW IS FOR IMAGES ONLY
    linkGallery = link + "/gallery"
    urlGallery = requests.get(str(linkGallery))
    soupGallery = BeautifulSoup(urlGallery.text,'html.parser')
    imageList = []
    for images in soupGallery.find_all('img', {'data-lazy':True}):
      imageList.append(images.get('data-lazy'))
      outerDict[link]['images']=imageList
  return outerDict

def getTitle(soup):
  titleList = []
  for title in soup.find_all('h2'):
    titleList.append(title.text)
  title = titleList[0]
  return title

def getAddress(soup):
  # find address here
  AddressList = []
  for address in soup.find_all('h1'):
    AddressList.append(address.text)
  address = AddressList[0]
  return address

def getDescription(soup):
  DescriptionList = []
  for description in soup.find_all('p'):
    DescriptionList.append(description.text)
  description = DescriptionList[5]
  return description.strip()

def getDate(soup):
  datesList = []
  # might be a problem for implementing everything together, ideally just want to replace the tags in the "times" div section
  for tag in soup.find_all('br'):
    tag.replace_with(tag.text + ' ')
  for times in soup.find_all('div', {"class": "date-time"}):
    datesList.append((times.text).strip())
  return datesList
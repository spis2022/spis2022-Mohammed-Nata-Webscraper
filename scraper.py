import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# Setting up soup for the general area search page
def getLinks():
  # soup for listing page
  url = requests.get('https://garagesalefinder.com/yard-sales/sammamish-wa/')
  soup = BeautifulSoup(url.text,'html.parser')
  # collects links of listings
  outerDict = {}  
  for aTag in soup.find_all('a', {'href': True}):
    link = (aTag.get('href'))
    if 'garagesalefinder' in link and 'gallery' not in link:
      outerDict[link] = {}
  # building inner dictionary     
  for link in outerDict.keys():
    urlDescription = requests.get(str(link))
    soupD = BeautifulSoup(urlDescription.text, 'html.parser')
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

def getTitle():
  url = requests.get("https://garagesalefinder.com/s/NUcGv/15326-corliss-pl-n-shoreline-wa-98133")
  soup = BeautifulSoup(url.text, 'html.parser')
  titleList = []
  for title in soup.find_all('h2'):
    titleList.append(title.text)
  title = titleList[0]
  return title

def getAddress():
  # find address here
  url = requests.get("https://garagesalefinder.com/s/NUcGv/15326-corliss-pl-n-shoreline-wa-98133")
  soup = BeautifulSoup(url.text, 'html.parser')
  AddressList = []
  for address in soup.find_all('h1'):
    AddressList.append(address.text)
  address = AddressList[0]
  return address

def getDescription():
  url = requests.get("https://garagesalefinder.com/s/NUcGv/15326-corliss-pl-n-shoreline-wa-98133")
  soup = BeautifulSoup(url.text, 'html.parser')
  DescriptionList = []
  for description in soup.find_all('p'):
    DescriptionList.append(description.text)
  description = DescriptionList[5]
  return description.strip()

def getDate():
  url = requests.get("https://garagesalefinder.com/s/NUcGv/15326-corliss-pl-n-shoreline-wa-98133")
  soup = BeautifulSoup(url.text, 'html.parser')
  datesList = []
  # might be a problem for implementing everything together, ideally just want to replace the tags in the "times" div section
  for tag in soup.find_all('br'):
    tag.replace_with(tag.text + ' ')
  for times in soup.find_all('div', {"class": "date-time"}):
    datesList.append((times.text).strip())
  return datesList
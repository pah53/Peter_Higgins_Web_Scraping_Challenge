#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing packages
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo


# In[2]:


#Creating connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[3]:


#Creating database and connection to MongoDB
db = client.mars_articles_db
collection = db.items


# In[4]:


#Creating BeautifulSoup connection to Nasa page
url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


# In[5]:


titles = []
paragraphs = []


results = soup.find_all('div', class_='slide')

for result in results:
    try:
        title = result.find('div', class_="content_title" ).a.text
        titles.append(title)
        paragraph =result.find_all('div', class_="rollover_description_inner")[0].text
        paragraphs.append(paragraph)
        
        print('-----------------')
        print(title)
        print(paragraph)
        
    except AttributeError as e:
        print(e)
        titles_1= titles[1]
        paragraphs_1= paragraphs[1]


# In[6]:


#initilizing chromedriver
get_ipython().system('which chromedriver ')
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[7]:


#scrap the link for the Featured Image from https://www.jpl.nasa.gov/spaceimages.\n",
url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

full_image = browser.find_by_id('full_image')
full_image.click()

soup = BeautifulSoup(browser.html, 'html.parser')
img = soup.find('img', "fancybox-image")

featured_image_url = 'https://www.jpl.nasa.gov'+ img['src']
featured_image_url 


# In[ ]:


#Mars Weather scraping    
url= 'https://twitter.com/marswxreport?lang=en'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.prettify)


# In[ ]:


#Parse through data
tweet = soup.find_all('div', "tweet")
mars_weather = tweet[0].find('p', class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

print(mars_weather)


# In[ ]:


#Looking through the Mars facts webpage
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
len(tables)


# In[ ]:


df=tables[2]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
html_table = df.to_html()
print(html_table)


# In[ ]:


#Mars hemispheres
get_ipython().system('which chromedriver ')
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


#Visiting website
url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html


# In[ ]:


soup = BeautifulSoup(html, 'html.parser')
elements = soup.find_all('div', class_="item")
titles=[]
urls = []
for element in elements:
    title=element.h3.text
    partial_url =element.a['href']
    titles.append(title)
    urls.append('https://astrogeology.usgs.gov'+partial_url)
    print(title)
    print(partial_url)


# In[ ]:


#Scraping the high resolution images
hi_res =[]
for url in urls:
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    img_url = soup.find('div', 'downloads')
    picture=img_url.a['href']
    hi_res.append(picture)
    print(picture)


# In[ ]:


#Creatings dictionaries
data = {'titles': titles, 'imag_HR': hi_res}
Hemisphere_image_urls= pd.DataFrame(data)
Hemisphere_image_urls.head()


# In[ ]:





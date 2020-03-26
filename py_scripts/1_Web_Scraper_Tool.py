#!/Users/marinabennett/PycharmProjects/class/venv/bin/python
#  coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd

timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

filepath = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/'
print(timestamp, file=open(filepath + 'scrape_log.txt', 'a'))

### 1. Breitbart - Very Conservative -----------------------------------

# load the HTML content using requests and save into a variable
breitbart_request = requests.get('https://www.breitbart.com/politics/')
breitbart_homepage = breitbart_request.content

# create soup 
breitbart_soup = BeautifulSoup(breitbart_homepage, 'html.parser')

# locate article URLs
breitbart_tags = breitbart_soup.find_all('h2')

# get article titles, content, dates, and links
breitbart_links = []
breitbart_titles = []
breitbart_dates = []
breitbart_contents = []

for n in np.arange(0, min(len(breitbart_tags), 30)):

    # get article link
    link = breitbart_tags[n].find('a')['href']
    link = "https://www.breitbart.com" + link
    breitbart_links.append(link)
    
    # get article title
    title = breitbart_tags[n].find('a').get_text()
    breitbart_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    date = soup_article.time.attrs['datetime']
    date = date[:-10]
    breitbart_dates.append(date)
    
    # get article content
    body = soup_article.find_all('div', class_='entry-content')
    x = body[0].find_all('p')
    
    # combine paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

    breitbart_contents.append(final_article)

# assembling data
breitbart_data = pd.DataFrame.from_dict({
    'publisher': 'Breitbart',
    'date': breitbart_dates,
    'link': breitbart_links,
    'article_title': breitbart_titles,
    'article_text': breitbart_contents 
})

# make sure it looks nice
breitbart_data.head()

# read in old data
old_breitbart_data = pd.read_csv(filepath + 'data/breitbart_data.csv')
num_breitbart_old = len(old_breitbart_data)

# append new data
breitbart_data = old_breitbart_data.append(breitbart_data).drop_duplicates()

# save new .csv
breitbart_data.to_csv(filepath + 'data/breitbart_data.csv', index = False)
num_breitbart_now = len(breitbart_data)

print('number of entries in old breitbart data: {}'.format(num_breitbart_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new breitbart data: {}'.format(num_breitbart_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_breitbart_now-num_breitbart_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 2. Fox - Conservative ----------------------------------------

# load the HTML content using requests and save into a variable
fox_requests = requests.get('https://www.foxnews.com/politics')
fox_homepage = fox_requests.content

# create a soup to allow BeautifulSoup to work
fox_soup = BeautifulSoup(fox_homepage, 'html.parser')

# locate article links
fox_tags = fox_soup.find_all('article')

# get homepage article links
fox_links = []
fox_text = []
fox_titles = []
fox_dates = []

for n in np.arange(0, len(fox_tags)):
    link = fox_tags[n].find('a')
    link = link.get('href')
    link = "https://foxnews.com" + link
    fox_links.append(link)
    fox_links = [x for x in fox_links if "/v/" not in x]
    fox_links = [x for x in fox_links if "https://foxnews.comhttps://www.foxnews.com" not in x]

# prep for article content
for link in fox_links:
    fox_article_request = requests.get(link)
    fox_article = fox_article_request.content
    fox_article_soup = BeautifulSoup(fox_article, 'html.parser')
    
    # get article metadata
    fox_metadata = fox_article_soup.find_all('script')[2].get_text()
    fox_metadata = fox_metadata.split(",")
    
    for item in fox_metadata:

        # get article title
        if 'headline' in item:
            item = item.replace('\n',"")
            item = item.replace('headline', "")
            item = item.replace(':', "")
            item = item.replace('"', '')
            fox_titles.append(item)
        
        # get article date
        elif 'datePublished' in item:
            item = item.replace('\n',"")
            item = item.replace('datePublished', "")
            item = item.replace(':', "")
            item = item.replace('"', '')
            fox_dates.append(item)
    
    # get article text
    body = fox_article_soup.find_all('div')
    x = body[0].find_all('p')
    
    # combine paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        paragraph = paragraph.replace('\n',"")
        list_paragraphs.append(paragraph)
        
        # removing copyright info and newsletter junk from the article
        final_article = " ".join(list_paragraphs)
        final_article = final_article.replace("This material may not be published, broadcast, rewritten, or redistributed. ©2020 FOX News Network, LLC. All rights reserved. All market data delayed 20 minutes.", " ")
        final_article = final_article.replace("This material may not be published, broadcast, rewritten,", " ")
        final_article = final_article.replace("or redistributed. ©2020 FOX News Network, LLC. All rights reserved.", " ")
        final_article = final_article.replace("All market data delayed 20 minutes.", " ")
        final_article = final_article.replace("Get all the stories you need-to-know from the most powerful name in news delivered first thing every morning to your inbox Subscribed You've successfully subscribed to this newsletter!", " ")
    fox_text.append(final_article)

# join fox data
fox_data = pd.DataFrame.from_dict({
    'publisher': 'Fox',
    'date': fox_dates,
    'link': fox_links,
    'article_title': fox_titles,
    'article_text': fox_text 
})

fox_data.head()

# read in old data
old_fox_data = pd.read_csv(filepath + 'data/fox_data.csv')
num_fox_old = len(old_fox_data)

# append new data
fox_data = old_fox_data.append(fox_data).drop_duplicates()

# save new .csv
fox_data.to_csv(filepath + 'data/fox_data.csv', index = False)
num_fox_now = len(fox_data)

print('number of entries in old fox data: {}'.format(num_fox_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new fox data: {}'.format(num_fox_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_fox_now-num_fox_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 3. Washington Times - Center Right ------------------------------------

# load the HTML content using requests and save into a variable
wt_request = requests.get('https://www.washingtontimes.com/news/politics/')
wt_homepage = wt_request.content

# create soup 
wt_soup = BeautifulSoup(wt_homepage, 'html.parser')

# locate article URLs
wt_tags = wt_soup.find_all('h2', class_='article-headline')

# get article titles, content, dates, and links
wt_links = []
wt_titles = []
wt_dates = []
wt_contents = []

for n in np.arange(0, len(wt_tags)):

    # get article link
    link = wt_tags[n].find('a')['href']
    link = 'https://www.washingtontimes.com' + link
    wt_links.append(link)
    
    # get article title
    title = wt_tags[n].find('a').get_text()
    wt_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    meta = soup_article.find('div', class_='meta').find('span', class_='source').text
    strip = meta.replace(' -\n\t\t\t\n\t\t\t\tAssociated Press\n -\n                      \n                        \n                        ', '')
    strip = strip.replace(' -\n\t\t\t\n\t\t\t\tThe Washington Times\n -\n                      \n                        \n                        ', '')
    date = strip.replace('\n                      \n                    ', '')
    wt_dates.append(date)
    
    # get article content
    for div in soup_article.find_all('div', {'class':'article-toplinks'}):
        div.decompose()
    
    body = soup_article.find_all('div', class_= 'bigtext')  
    x = body[0].find_all('p')
    
    # combine paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs).split("\n")[0]
       
    wt_contents.append(final_article)

# assembling data
wt_data = pd.DataFrame.from_dict({
    'publisher': 'washington_times',
    'date': wt_dates,
    'link': wt_links,
    'article_title': wt_titles,
    'article_text': wt_contents 
})

wt_data.head()

# read in old data
old_wt_data = pd.read_csv(filepath + 'data/wt_data.csv')
num_wt_old = len(old_wt_data)

# append new data
wt_data = old_wt_data.append(wt_data).drop_duplicates()

# save new .csv
wt_data.to_csv(filepath + 'data/wt_data.csv', index = False)
num_wt_now = len(wt_data)

print('number of entries in old wt data: {}'.format(num_wt_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new wt data: {}'.format(num_wt_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_wt_now-num_wt_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 4. Associated Press - Neutral --------------------------------

# load the HTML content using requests and save into a variable
ap_requests = requests.get('https://apnews.com/apf-politics')
ap_homepage = ap_requests.content

# create a soup to allow BeautifulSoup to work
ap_soup = BeautifulSoup(ap_homepage, 'html.parser')

# locate articles
ap_tags = ap_soup.find_all('a', class_='Component-headline-0-2-106')

# get homepage article links
ap_links = []

for link in ap_tags:
    link = link.get('href')
    link = 'https://apnews.com' + link
    ap_links.append(link)

# get article title, date, and content
ap_text = []
ap_titles = []
ap_dates = []

for link in ap_links:
    ap_article_request = requests.get(link)
    ap_article = ap_article_request.content
    ap_article_soup = BeautifulSoup(ap_article, 'html.parser')
    
    # article titles
    title = ap_article_soup.find_all('meta')[14]
    title = title['content']
    ap_titles.append(title)
    
    # article date
    date = ap_article_soup.find_all('meta')[24]
    date = date['content']
    ap_dates.append(date)
    
    # article content: <div class="Article" data-key=Article.
    body = ap_article_soup.find_all('div')
    x = body[0].find_all('p')

    # combine paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        paragraph = paragraph.replace('\n',"")
        paragraph = paragraph.replace('CHICAGO (AP) -',"")
        paragraph = paragraph.replace('DETROIT (AP) -',"")
        paragraph = paragraph.replace('WASHINGTON (AP) -',"")
        paragraph = paragraph.replace('___ Catch up on the 2020 election campaign with AP experts on our weekly politics podcast, “Ground Game.',"")
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
    ap_text.append(final_article)

# join ap data
ap_data = pd.DataFrame.from_dict({
    'publisher': 'AP',
    'date': ap_dates,
    'link': ap_links,
    'article_title': ap_titles,
    'article_text': ap_text 
})

ap_data.head()

# read in old data
old_ap_data = pd.read_csv(filepath + 'data/ap_data.csv')
num_ap_old = len(old_ap_data)

# append new data
ap_data = old_ap_data.append(ap_data).drop_duplicates()

# save new .csv
ap_data.to_csv(filepath + 'data/ap_data.csv', index = False)
num_ap_now = len(ap_data)

print('number of entries in old ap data: {}'.format(num_ap_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new ap data: {}'.format(num_ap_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_ap_now-num_ap_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 5. NBC - Center-Left ----------------------------------------

# load the HTML content using requests and save into a variable
nbc_request = requests.get('https://www.nbcnews.com/politics')
nbc_homepage = nbc_request.content

# create soup 
nbc_soup = BeautifulSoup(nbc_homepage, 'html.parser')

# locate article URLs
nbc_tags = nbc_soup.find_all('h2', class_='teaseCard__headline') + nbc_soup.find_all('h2', class_='title___2T5qK')

# get article titles, content, dates, and links
nbc_links = []
nbc_titles = []
nbc_dates = []
nbc_contents = []

for n in np.arange(0, len(nbc_tags)):

    # get article link
    link = nbc_tags[n].find('a')['href']
    nbc_links.append(link)
    
    # get article title
    title = nbc_tags[n].find('a').get_text()
    nbc_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    if soup_article.time != None:
        date = soup_article.time.attrs['datetime']
        date = date[4:-24] 
    else:
        date = None
    nbc_dates.append(date)
    
    # get article content
    body = soup_article.find_all('div', class_= 'article-body__content')    
    final_article = " ".join([item.text for item in body])
       
    nbc_contents.append(final_article)

# assembling data
nbc_data = pd.DataFrame.from_dict({
    'publisher': 'nbc',
    'date': nbc_dates,
    'link': nbc_links,
    'article_title': nbc_titles,
    'article_text': nbc_contents 
})

# dropping rows that are not text articles (these will have NA in date)
nbc_data = nbc_data.dropna()

nbc_data.head()

# read in old data
old_nbc_data = pd.read_csv(filepath + 'data/nbc_data.csv')
num_nbc_old = len(old_nbc_data)

# append new data
nbc_data = old_nbc_data.append(nbc_data).drop_duplicates()

# save new .csv
nbc_data.to_csv(filepath + 'data/nbc_data.csv', index = False)
num_nbc_now = len(nbc_data)

print('number of entries in old nbc data: {}'.format(num_nbc_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new nbc data: {}'.format(num_nbc_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_nbc_now-num_nbc_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 6. New York Times - Liberal ---------------------------------------

# load the HTML content using requests and save into a variable
nyt_request = requests.get('https://www.nytimes.com/section/politics')
nyt_homepage = nyt_request.content

# create soup 
nyt_soup = BeautifulSoup(nyt_homepage, 'html.parser')

# homepage URLs
nyt_tags_home = nyt_soup.find_all('h2', class_='css-l2vidh e4e4i5l1')

# archive URLs
# nyt_tags_archive = nyt_soup.find_all('div', class_='css-1l4spti') gone from site as of 19/03/3030

# setup for both
nyt_links = []
nyt_titles = []
nyt_dates = []
nyt_contents = []

# homepage articles
for n in np.arange(0, len(nyt_tags_home)):

    # get article link
    link = nyt_tags_home[n].find('a')['href']
    link = "https://www.nytimes.com" + link
    nyt_links.append(link)
    
    # get article title
    title = nyt_tags_home[n].find('a').get_text()
    nyt_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    date = soup_article.time.attrs['datetime']
    date = date[:-15]
    nyt_dates.append(date)
    
    # get article content
    for div in soup_article.find_all("div", {'class': 'css-9tf9ac'}):
        div.decompose()

    body = soup_article.find_all('div', {'class':['css-53u6y8', 'css-1fanzo5']})
    final_article = " ".join([item.text for item in body])
        
    nyt_contents.append(final_article)

# archive articles
for n in np.arange(0, len(nyt_tags_archive)):

    # get article link
    link = nyt_tags_archive[n].find('a')['href']
    link = "https://www.nytimes.com" + link
    nyt_links.append(link)

    # get article title
    title = nyt_tags_archive[n].find('a').get_text()
#    nyt_titles.append(title)
    
    # prep article content
#    article = requests.get(link)
#    article_content = article.content
#    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
#    date = soup_article.time.attrs['datetime']
#    date = date[:-15]
#    nyt_dates.append(date)
        
    # get article content
#    for div in soup_article.find_all("div", {'class': 'css-9tf9ac'}):
#        div.decompose()

#    body = soup_article.find_all('div', attrs = {'class':['css-53u6y8', 'css-1fanzo5 StoryBodyCompanionColumn']})
#    final_article = " ".join([item.text for item in body])
        
#    nyt_contents.append(final_article)

# assembling data
nyt_data = pd.DataFrame.from_dict({
    'publisher': 'new_york_times',
    'date': nyt_dates,
    'link': nyt_links,
    'article_title': nyt_titles,
    'article_text': nyt_contents 
})

nyt_data.head()

# read in old data
old_nyt_data = pd.read_csv(filepath + 'data/nyt_data.csv')
num_nyt_old = len(old_nyt_data)

# append new data
nyt_data = old_nyt_data.append(nyt_data).drop_duplicates()

# save new .csv
nyt_data.to_csv(filepath + 'data/nyt_data.csv', index = False)
num_nyt_now = len(nyt_data)

print('number of entries in old nyt data: {}'.format(num_nyt_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new nyt data: {}'.format(num_nyt_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_nyt_now-num_nyt_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 7. Politico - Liberal ------------------------------------------

# load the HTML content using requests and save into a variable
politico_request = requests.get('https://www.politico.com/politics')
politico_homepage = politico_request.content

# create soup 
politico_soup = BeautifulSoup(politico_homepage, 'html.parser')

# locate article URLs
politico_tags = politico_soup.find_all('h3')

# get article titles, content, dates, and links
politico_links = []
politico_titles = []
politico_dates = []
politico_contents = []

for n in np.arange(0, len(politico_tags)):

    # get article link
    link = politico_tags[n].find('a')['href']
    politico_links.append(link)
    
    # get article title
    title = politico_tags[n].find('a').get_text()
    politico_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    date = soup_article.time.attrs['datetime']
    date = date[:-9]
    politico_dates.append(date)
    
    # get article content
    body = soup_article.find_all('p', attrs={'class':'story-text__paragraph'})
    final_article = " ".join([item.text for item in body])
    
    politico_contents.append(final_article)

# assembling data
politico_data = pd.DataFrame.from_dict({
    'publisher': 'politico',
    'date': politico_dates,
    'link': politico_links,
    'article_title': politico_titles,
    'article_text': politico_contents 
})

# dropping rows that are not text articles (these will have NA in text)
politico_data = politico_data.dropna()

politico_data.head()

# read in old data
old_politico_data = pd.read_csv(filepath + 'data/politico_data.csv')
num_politico_old = len(old_politico_data)

# append new data
politico_data = old_politico_data.append(politico_data).drop_duplicates()

# save new .csv
politico_data.to_csv(filepath + 'data/politico_data.csv', index = False)
num_politico_now = len(politico_data)

print('number of entries in old politico data: {}'.format(num_politico_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new politico data: {}'.format(num_politico_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_politico_now-num_politico_old), file=open(filepath + 'scrape_log.txt', 'a'))


### 8. Buzzfeed - Very Liberal ----------------------------------------------

# load the HTML content using requests and save into a variable
buzz_request = requests.get('https://www.buzzfeednews.com/section/politics')
buzz_homepage = buzz_request.content

# create soup
buzz_soup = BeautifulSoup(buzz_homepage, 'html.parser')

# locate article URLs
buzz_tags = buzz_soup.find_all('h2')

# get article titles, content, dates, and links
buzz_links = []
buzz_titles = []
buzz_dates = []
buzz_contents = []

for n in np.arange(0, min(len(buzz_tags), 30)):

    # get article link
    link = buzz_tags[n].find('a')['href']
    buzz_links.append(link)
    
    # get article title
    title = buzz_tags[n].find('a').get_text()
    buzz_titles.append(title)
    
    # prep article content
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    
    # get publication datetime
    date = soup_article.find_all('div', class_='news-article-header__timestamps')
    date = " ".join([item.text for item in date]).replace('\n', '')
    buzz_dates.append(date)
    
    # get article content
    body = soup_article.find_all('div', attrs={'data-module':'subbuzz-text'})
    article = " ".join([item.text for item in body]).replace('\n', '')
    final_article = re.sub(r' {[^}]*}', '', article)

    buzz_contents.append(final_article)

# assembling data
buzz_data = pd.DataFrame.from_dict({
    'publisher': 'buzzfeed',
    'date': buzz_dates,
    'link': buzz_links,
    'article_title': buzz_titles,
    'article_text': buzz_contents 
})

buzz_data.head()

# read in old data
old_buzz_data = pd.read_csv(filepath + 'data/buzzfeed_data.csv')
num_buzz_old = len(old_buzz_data)

# append new data
buzz_data = old_buzz_data.append(buzz_data).drop_duplicates()

# save new .csv
buzz_data.to_csv(filepath + 'data/buzzfeed_data.csv', index = False)
num_buzz_now = len(buzz_data)

print('number of entries in old buzzfeed data: {}'.format(num_buzz_old), file=open(filepath + 'scrape_log.txt', 'a'))
print('total number of entries in new buzzfeed data: {}'.format(num_buzz_now), file=open(filepath + 'scrape_log.txt', 'a'))
print('difference: {}'.format(num_buzz_now-num_buzz_old), file=open(filepath + 'scrape_log.txt', 'a'))


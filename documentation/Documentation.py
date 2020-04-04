#!/usr/bin/env python
# coding: utf-8

# # Documentation

# In[6]:


import requests
import re
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import warnings

warnings.simplefilter(action='ignore')


# In[4]:


class WebScraper:
    """
    A class used to scrape articles from 8 different U.S. media outlets and save as a .csv file.
    
    ...
    
    Methods
    -------
    get_Breitbart()
        Scrapes new articles from breitbart.com/politics/ and returns a dataframe.
    save_Breitbart()
        Appends new Breitbart articles to dataframe of old Breitbart articles and saves as a .csv file.
    check_Breitbart()
        Prints number of new Breitbart articles and number of total Breitbart articles in saved .csv.
        
    get_FoxNews()
        Scrapes new articles from foxnews.com/politics/ and returns a dataframe.
    save_FoxNews()
        Appends new Fox articles to dataframe of old Fox articles and saves as a .csv file.
    check_FoxNews()
        Prints number of new Fox articles and number of total Fox articles in saved .csv.
        
    get_WashingtonTimes()
        Scrapes new articles from washingtontimes.com/news/politics/ and returns a dataframe.
    save_WashingtonTimes()
        Appends new articles to Washington Times dataframe of old Washington Times articles and saves as a .csv file.
    check_WashingtonTimes()
        Prints number of new Washington Times articles and number of total Washington Times articles in saved .csv.
        
    get_AP()
        Scrapes new articles from apnews.com/apf-politics and returns a dataframe.
    save_AP()
        Appends new AP articles to dataframe of old AP articles and saves as a .csv file.
    check_AP()
        Prints number of new AP articles and number of total AP articles in saved .csv.
        
    get_NYT()
        Scrapes new articles from nytimes.com/section/politics and returns a dataframe.
    save_NYT()
        Appends new NYT articles to dataframe of old NYT articles and saves as a .csv file.
    check_NYT()
        Prints number of new NYT articles and number of total NYT articles in saved .csv.
        
    get_NBC()
        Scrapes new articles from nbcnews.com/politics and returns a dataframe.
    save_NBC()
        Appends new articles to dataframe of old articles and saves as a .csv file.
    check_NBC()
        Prints number of new NBC articles and number of total NBC articles in saved .csv.
        
    get_Politico()
        Scrapes new articles from politico.com/politics and returns a dataframe.
    save_Politico()
        Appends new Politico articles to dataframe of old Politico articles and saves as a .csv file.
    check_Politico()
        Prints number of new Politico articles and number of total Politico articles in saved .csv.
        
    get_Buzzfeed()
        Scrapes new articles from buzzfeednews.com/section/politics and returns a dataframe.
    save_Buzzfeed()
        Appends new Buzzfeed articles to dataframe of old Buzzfeed articles and saves as a .csv file.
    check_Buzzfeed()
        Prints number of new Buzzfeed articles and number of total Buzzfeed articles in saved .csv.
        
    """ 
    def get_Breitbart():
        """
        Scrapes new articles from breitbart.com/politics/ and returns a dataframe.
        """
        # load the HTML content using requests and save into a variable
        breitbart_request = requests.get('https://www.breitbart.com/politics/')
        breitbart_homepage = breitbart_request.content
        
        # create soup 
        breitbart_soup = BeautifulSoup(breitbart_homepage, 'html.parser')
        
        # locate article URLs
        breitbart_tags = breitbart_soup.find_all('h2')
        
        # setup
        number_of_articles = min(len(breitbart_tags), 30)

        breitbart_links = []
        breitbart_titles = []
        breitbart_dates = []
        breitbart_contents = []
        
        # get article titles, content, and links
        for n in np.arange(0, number_of_articles):

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
        
        return breitbart_data
    
    def save_Breitbart():
        """
        Appends new Breitbart data the the old Breitbart data and saves entire df as a .csv file.
        """
        # read in old data
        old_breitbart_data = pd.read_csv('data/breitbart_data.csv')
        num_old = len(old_breitbart_data)

        # append new data
        breitbart_data = old_breitbart_data.append(breitbart_data).drop_duplicates()

        # save new .csv
        breitbart_data.to_csv("data/breitbart_data.csv", index = False)
        num_now = len(breitbart_data)

    def check_Breitbart():
        """
        Prints number of entries in old Breitbart data and total number of entries in new Breitbart data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
    
    def get_FoxNews():
        """
        Scrapes new articles from foxnews.com/politics/ and returns a dataframe.
        """
        # load the HTML content using requests and save into a variable
        fox_requests = requests.get('https://www.foxnews.com/politics')
        fox_homepage = fox_requests.content
        # create a soup to allow BeautifulSoup to work
        fox_soup = BeautifulSoup(fox_homepage, 'html.parser')
        # locate article links
        fox_tags = fox_soup.find_all('article')
        # setup
        fox_links = []
        fox_text = []
        fox_titles = []
        fox_dates = []
        number_of_articles = 30
        # get homepage article links
        for n in np.arange(0, number_of_articles):
            link = fox_tags[n].find('a')
            link = link.get('href')
            link = "https://foxnews.com" + link
            fox_links.append(link)
            fox_links = [x for x in fox_links if "/v/" not in x]
            
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
            
            return fox_data

    def save_Fox():
        """
        Appends new Fox data the the old Fox data and saves entire df as a .csv file.
        """
        # read in old data
        old_fox_data = pd.read_csv('data/fox_data.csv')
        num_old = len(old_fox_data)

        # append new data
        fox_data = old_fox_data.append(fox_data).drop_duplicates()

        # save new .csv
        fox_data.to_csv("data/fox_data.csv", index = False)
        num_now = len(fox_data)
        
    def check_Fox():
        """
        Prints number of entries in old Fox data and total number of entries in new Fox data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        
    
    def get_WashingtonTimes():
        """
        Scrapes new articles from washingtontimes.com/news/politics/ and returns a dataframe.
        """
        # load the HTML content using requests and save into a variable
        wt_request = requests.get('https://www.washingtontimes.com/news/politics/')
        wt_homepage = wt_request.content
        # create soup 
        wt_soup = BeautifulSoup(wt_homepage, 'html.parser')
        # locate article URLs
        wt_tags = wt_soup.find_all('h2', class_="article-headline")
        # setup
        number_of_articles = len(wt_tags)

        # get article titles, content, and links
        wt_links = []
        wt_titles = []
        wt_dates = []
        wt_contents = []
        
        # get article titles, content, and links
        for n in np.arange(0, number_of_articles):

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
            meta = soup_article.find("div", class_="meta").find("span", class_="source").text
            strip = meta.replace(' -\n\t\t\t\n\t\t\t\tAssociated Press\n -\n                      \n                        \n                        ', '')
            strip = strip.replace(' -\n\t\t\t\n\t\t\t\tThe Washington Times\n -\n                      \n                        \n                        ', '')
            date = strip.replace('\n                      \n                    ', '')
            wt_dates.append(date)

            # get article content
            for div in soup_article.find_all("div", {'class':'article-toplinks'}): 
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
        
        return wt_data
    
    def save_WashingtonTimes():
        """
        Appends new Washington Times data the the old Washington Times data and saves entire df as a .csv file.        
        """
        # read in old data
        old_wt_data = pd.read_csv('data/wt_data.csv')
        num_old = len(old_wt_data)

        # append new data
        wt_data = old_wt_data.append(wt_data).drop_duplicates()

        # save new .csv
        wt_data.to_csv("data/wt_data.csv", index = False)
        num_now = len(wt_data)

    def check_WashingtonTimes():
        """
        Returns number of entries in old Washington Times data and total number of entries in new Washington Times data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        
    
    def get_AP():
        """
        Scrapes new articles from apnews.com/apf-politics and returns a dataframe.
        """ 
        # load the HTML content using requests and save into a variable
        ap_requests = requests.get('https://apnews.com/apf-politics')
        ap_homepage = ap_requests.content
        
        # create a soup to allow BeautifulSoup to work
        ap_soup = BeautifulSoup(ap_homepage, 'html.parser')
        
        # locate articles
        ap_tags = ap_soup.find_all('a', class_="Component-headline-0-2-105")
        
        # setup
        number_of_articles = min(len(ap_tags), 30)

        ap_links = []
        ap_text = []
        ap_titles = []
        ap_dates = []
        
        # get homepage article links
        for link in ap_tags:
            link = link.get('href')
            link = "https://apnews.com" + link
            ap_links.append(link)
            
        # prep for article content
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
        
        return ap_data
        
    def save_AP():
        """
        Appends new AP data the the old AP data and saves entire df as a .csv file.
        """
        # read in old data
        old_ap_data = pd.read_csv('data/ap_data.csv')
        num_old = len(old_ap_data)

        # append new data
        ap_data = old_ap_data.append(ap_data).drop_duplicates()

        # save new .csv
        ap_data.to_csv("data/ap_data.csv", index = False)
        num_now = len(ap_data)
    
    def check_AP():
        """
        Prints number of entries in old AP data and total number of entries in new AP data.
        """
        # see number of articles
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        print("difference: {}".format(num_now-num_old))
            
    def NBC():
        """
        Scrapes new articles from nbcnews.com/politics and returns a dataframe.
        """ 
        # load the HTML content using requests and save into a variable
        nbc_request = requests.get('https://www.nbcnews.com/politics')
        nbc_homepage = nbc_request.content

        # create soup 
        nbc_soup = BeautifulSoup(nbc_homepage, 'html.parser')

        # locate article URLs
        nbc_tags = nbc_soup.find_all('h2', class_="teaseCard__headline") + nbc_soup.find_all('h2', class_="title___2T5qK")

        # setup
        number_of_articles = len(nbc_tags)

        # get article titles, content, and links
        nbc_links = []
        nbc_titles = []
        nbc_dates = []
        nbc_contents = []

        # get article titles, content, and links
        for n in np.arange(0, number_of_articles):

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

        return nbc_data
        
    def save_NBC():
        """
        Appends new NBC data the the old NBC data and saves entire df as a .csv file.
        """
        # read in old data
        old_nbc_data = pd.read_csv('data/nbc_data.csv')
        num_old = len(old_nbc_data)

        # append new data
        nbc_data = old_nbc_data.append(nbc_data).drop_duplicates()

        # save new .csv
        nbc_data.to_csv("data/nbc_data.csv", index = False)
        num_now = len(nbc_data)
    
    def check_NBC():
        """
        Prints number of entries in old NBC data and total number of entries in new NBC data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))

    def NYT():
        """
        Scrapes new articles from nytimes.com/section/politics and returns a dataframe.
        """
        # load the HTML content using requests and save into a variable
        nyt_request = requests.get('https://www.nytimes.com/section/politics')
        nyt_homepage = nyt_request.content

        # create soup 
        nyt_soup = BeautifulSoup(nyt_homepage, 'html.parser')

        # homepage URLs
        nyt_tags_home = nyt_soup.find_all('h2', class_="css-l2vidh e4e4i5l1")

        # archive URLs
        nyt_tags_archive = nyt_soup.find_all('div', class_='css-1l4spti')

        # setup 
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
            for div in soup_article.find_all("div", {'class':'css-9tf9ac'}): 
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
            body = soup_article.find_all('div', attrs = {'class':['css-53u6y8', 'css-1fanzo5 StoryBodyCompanionColumn']})
            final_article = " ".join([item.text for item in body])

            nyt_contents.append(final_article)

        # assembling data
        nyt_data = pd.DataFrame.from_dict({
            'publisher': 'new_york_times',
            'date': nyt_dates,
            'link': nyt_links,
            'article_title': nyt_titles,
            'article_text': nyt_contents 
        })

        return nyt_data
    
    def save_NYT():
        """
        Appends new NYT data the the old NYT data and saves entire df as a .csv file.
        """
        # read in old data
        old_nyt_data = pd.read_csv('data/nyt_data.csv')
        num_old = len(old_nyt_data)

        # append new data
        nyt_data = old_nyt_data.append(nyt_data).drop_duplicates()

        # save new .csv
        nyt_data.to_csv("data/nyt_data.csv", index = False)
        num_now = len(nyt_data)
    
    def check_NYT():
        """
        Prints number of entries in old NYT data and total number of entries in new NYT data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))

    
    def Politico():
        """
        Scrapes new articles from politico.com/politics and returns a dataframe.
        """
        # load the HTML content using requests and save into a variable
        politico_request = requests.get('https://www.politico.com/politics')
        politico_homepage = politico_request.content

        # create soup 
        politico_soup = BeautifulSoup(politico_homepage, 'html.parser')

        # locate article URLs
        politico_tags = politico_soup.find_all('h3')

        # setup
        number_of_articles = len(politico_tags)

        # get article titles, content, and links
        politico_links = []
        politico_titles = []
        politico_dates = []
        politico_contents = []

        # get article titles, content, and links
        for n in np.arange(0, number_of_articles):

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

        return politico_data
        
    def save_Politico():
        """
        Appends new Politico data the the old Politico data and saves entire df as a .csv file.
        """
        # read in old data
        old_politico_data = pd.read_csv('data/politico_data.csv')
        num_old = len(old_politico_data)

        # append new data
        politico_data = old_politico_data.append(politico_data).drop_duplicates()

        # save new .csv
        politico_data.to_csv("data/politico_data.csv", index = False)
        num_now = len(politico_data)
    
    def check_Politico():
        """
        Prints number of entries in old Politico data and total number of entries in new Politico data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
            
    
    def get_Buzzfeed():
        """
        Scrapes new articles from buzzfeednews.com/section/politics and returns a dataframe
        """
        # load the HTML content using requests and save into a variable
        buzz_request = requests.get('https://www.buzzfeednews.com/section/politics')
        buzz_homepage = buzz_request.content

        # create soup 
        buzz_soup = BeautifulSoup(buzz_homepage, 'html.parser')

        # locate article URLs
        buzz_tags = buzz_soup.find_all('h2')

        # setup
        number_of_articles = min(len(buzz_tags), 30)

        # get article titles, content, and links
        buzz_links = []
        buzz_titles = []
        buzz_dates = []
        buzz_contents = []

        # get article titles, content, and links
        for n in np.arange(0, number_of_articles):

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
            date = soup_article.find_all('div', class_="news-article-header__timestamps")    
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

        return buzz_data
        
    def save_Buzzfeed():
        """
        Appends new Buzzfeed data the the old Buzzfeed data and saves entire df as a .csv file. 
        """
        # read in old data
        old_buzz_data = pd.read_csv('data/buzzfeed_data.csv')
        num_old = len(old_buzz_data)

        ## append new data
        buzz_data = old_buzz_data.append(buzz_data).drop_duplicates()

        ## save new .csv
        buzz_data.to_csv("data/buzzfeed_data.csv", index = False)
        num_now = len(buzz_data)
    
    def check_Buzzfeed():
        """
        Prints number of entries in old Buzzfeed data and total number of entries in new Buzzfeed data.
        """
        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))


# In[ ]:


class DataPrep():
    """
    Returns a merged dataset, articles about candidates and sentences about candidates from 8 scraped sources.
    """
    def __init__(self):
        self.candidates = ['Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg', 
                           'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']
        self._full_data = None
        self._article_data = None
        self._sentence_data = None
        
    def full_data(self):
        """
        Returns fully merged dataset from articles scraped from 8 different U.S. media outlets
        """
        # load all data sets
        breitbart = pd.read_csv('data/breitbart_data.csv')
        fox = pd.read_csv('data/fox_data.csv')
        wt = pd.read_csv('data/wt_data.csv')
        ap = pd.read_csv('data/ap_data.csv')
        nbc = pd.read_csv('data/nbc_data.csv')
        nyt = pd.read_csv('data/nyt_data.csv')
        politico = pd.read_csv('data/politico_data.csv')
        buzzfeed = pd.read_csv('data/buzzfeed_data.csv')
        
        # make dates comparable
        fox['date'] = [x.split('T')[0] for x in fox['date']]
        wt['date'] = [x.replace(' -\n\t\t\t\n\t\t\t\tAssociated Press\n -    Updated:', '') for x in wt['date']]
        wt['date'] = [x.replace(' -\n\t\t\t\n\t\t\t\tThe Washington Times\n -    Updated:', '') for x in wt['date']]
        wt['date'] = [parse(x) for x in wt['date']]
        ap['date'] = [x.split('T')[0] for x in ap['date']]
        nbc = nbc.copy().dropna()
        nbc['date'] = [parse(x) for x in nbc['date']]
        buzzfeed['date'] = [x.replace('Posted on ', '').replace('Last updated on ', '') for x in buzzfeed['date']]
        buzzfeed['date'] = [x.strip() for x in buzzfeed['date']]
        buzzfeed['date'] = [x.split(',')[0:2] for x in buzzfeed['date']]
        buzzfeed['date'] = [''.join(x) for x in buzzfeed['date']]
        buzzfeed['date'] = [parse(x) for x in buzzfeed['date']]
        
        # merge
        self._full_data = pd.concat([
            breitbart,
            fox,
            wt,
            ap,
            nbc,
            nyt,
            politico,
            buzzfeed
        ])
        
        
        return self._full_data
    
    def article_data(self):
        """
        Returns articles that mention various U.S. candidates for president in 2020.
        """
        article_data = self.full_data()

        # identify candidates 
        article_data['Trump'] = pd.np.where(article_data['article_text'].str.contains('Trump'), 1, 0)
        article_data['Sanders'] = pd.np.where(article_data['article_text'].str.contains('Bernie'), 1, 
                                              (np.where(article_data['article_text'].str.contains('Sanders'), 1, 0)))
        article_data['Biden'] = pd.np.where(article_data['article_text'].str.contains('Biden'), 1, 0)
        article_data['Warren'] = pd.np.where(article_data['article_text'].str.contains('Warren'), 1, 0)
        article_data['Buttigieg'] = pd.np.where(article_data['article_text'].str.contains('Buttigieg'), 1, 0)
        article_data['Bloomberg'] = pd.np.where(article_data['article_text'].str.contains('Bloomberg'), 1, 0)
        article_data['Klobuchar'] = pd.np.where(article_data['article_text'].str.contains('Klobuchar'), 1, 0)
        article_data['Yang'] = pd.np.where(article_data['article_text'].str.contains('Yang'), 1, 0)
        article_data['Steyer'] = pd.np.where(article_data['article_text'].str.contains('Steyer'), 1, 0)
        article_data['Gabbard'] = pd.np.where(article_data['article_text'].str.contains('Gabbard'), 1, 0)
        
        # limit to only articles where candidate is mentioned
        article_data['candidates_mentioned'] = article_data[self.candidates].sum(axis = 1)
        article_data = article_data[article_data['candidates_mentioned'] != 0]
       
        self._article_data = article_data
            
        return self._article_data
    
    def save_article_data(self):
        """
        Saves articles that mention various U.S. candidates for president in 2020 as a csv.
        """
        # read in old data
        old_data = pd.read_csv('data/article_data.csv')
        num_old = len(old_data)

        # append new data
        article_data = old_data.append(self.article_data()).drop_duplicates()
        
        # save new .csv
        article_data.to_csv("data/article_data.csv", index = False)
        num_now = len(article_data)

        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        print("difference: {}".format(num_now - num_old))

    def sentence_data(self):
        """
        Returns articles that mention various U.S. candidates for president in 2020.
        """
        sentence_data = self.full_data()

        # articles to sentences
        # create article id #
        data_for_sentences = sentence_data[['article_text', 'article_title', 'date', 'link', 'publisher']].copy()
        data_for_sentences = data_for_sentences.reset_index()
        data_for_sentences = data_for_sentences.reset_index().rename(columns = {'level_0': 'article_id'}).drop(columns = 'index')
        
        # split article text to sentences
        sentences = data_for_sentences['article_text'].copy().str.split('.').apply(pd.Series, 1).stack()

        # add correct article id # to each sentence
        sentences.index.droplevel(-1) 
        sentences.name = 'article_text'
        sentences = sentences.reset_index().drop(columns = 'level_1').rename(columns = {'level_0': 'article_id'})
        
        # drop original article text
        data_for_sentences = data_for_sentences.drop(columns = 'article_text')
        
        # merge sentence article text
        sentence_data = data_for_sentences.merge(sentences, how='left', on='article_id')
        
        # clean up
        mask = sentence_data['article_text'].astype(str).str.len() < 15
        sentence_data.loc[mask, 'article_text'] = ''
        sentence_data = sentence_data[(sentence_data['article_text'] != '')]
        
        # identify candidates 
        sentence_data['Trump'] = pd.np.where(sentence_data['article_text'].str.contains('Trump'), 1, 0)
        sentence_data['Sanders'] = pd.np.where(sentence_data['article_text'].str.contains('Bernie'), 1, 
                                              (np.where(sentence_data['article_text'].str.contains('Sanders'), 1, 0)))
        sentence_data['Biden'] = pd.np.where(sentence_data['article_text'].str.contains('Biden'), 1, 0)
        sentence_data['Warren'] = pd.np.where(sentence_data['article_text'].str.contains('Warren'), 1, 0)
        sentence_data['Buttigieg'] = pd.np.where(sentence_data['article_text'].str.contains('Buttigieg'), 1, 0)
        sentence_data['Bloomberg'] = pd.np.where(sentence_data['article_text'].str.contains('Bloomberg'), 1, 0)
        sentence_data['Klobuchar'] = pd.np.where(sentence_data['article_text'].str.contains('Klobuchar'), 1, 0)
        sentence_data['Yang'] = pd.np.where(sentence_data['article_text'].str.contains('Yang'), 1, 0)
        sentence_data['Steyer'] = pd.np.where(sentence_data['article_text'].str.contains('Steyer'), 1, 0)
        sentence_data['Gabbard'] = pd.np.where(sentence_data['article_text'].str.contains('Gabbard'), 1, 0)
        
        # limit to only articles where candidate is mentioned
        sentence_data['candidates_mentioned'] = sentence_data[self.candidates].sum(axis = 1)
        sentence_data = sentence_data[sentence_data['candidates_mentioned'] != 0]
       
        self._sentence_data = sentence_data
            
        return self._sentence_data
    
    def save_sentence_data(self):
        """
        Saves sentences that mention various U.S. candidates for president in 2020 as a csv.
        """
        # read in old data
        old_data = pd.read_csv('data/sentence_data.csv')
        num_old = len(old_data)

        # append new data
        sentence_data = old_data.append(self.sentence_data()).drop_duplicates()
        
        # save new .csv
        sentence_data.to_csv("data/sentence_data.csv", index = False)
        num_now = len(sentence_data)

        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        print("difference: {}".format(num_now - num_old))


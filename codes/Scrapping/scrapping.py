import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup #Pull data out of HTML and XML.
from selenium import webdriver
import time
import re

url_rank_serie = 'https://www.imdb.com/chart/toptv/'
url_imdb_base = 'https://www.imdb.com'
url_serie_ = f'?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=12230b0e-0e00-43ed-9e59-8d5353703cce&pf_rd_r=BFQY8EMES4H7BK35D10R&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_tt_'

"""Scrapping"""


def get_html_from_link(page_link):
    '''
        Get HTML from web page and parse it.

        :param page_link: link of the webpage we want to scrap
        :type page_link: string
        :return: BeautifulSoup object (HTML parsed)
        :rtype: bs4.BeautifulSoup
    '''

    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


html_all = get_html_from_link(url_rank_serie)
#print(html_all.prettify())


def get_link_to_serie(root_html):

    """
    This function extract the link to access the series information page.
    
    :param root_html: BeautifulSoup Element that contains all books links.
    :type book_html: bs4.BeautifulSoup.
    :return: list of all serie links in the page.
    :rtype: list(str).
    """
    serie_links = []
    reg = re.compile('/title/+')
    for elem in root_html.find_all('td', {'class':'titleColumn'}):
        for elements in elem.find_all('a', {'href' : reg}):
            attribut = elements["href"]
            serie_links.append(attribut)
    #len(serie_links)
    return(serie_links)

serie_links=get_link_to_serie(html_all)
#serie_links


def get_info_serie(serie_html):
    
    """
    Return series informations.
    
    :param serie_html: BeautifulSoup element that contains serie infos.
    :type serie_html: bs4.element.Tag.
    :return:
            - serie_title: tile of the TV serie.
            - serie_genre: genre-s of the TV serie.
            - serie_nb_season:
            - serie_type: the serie can be TV Mini-Series or TV Series.
            - serie_actors : actors who play in the TV serie.
            - serie_creator : creator-s of the TV serie
            - serie_origin: origins/country of the TV serie.
            - serie_language: speaking language of the TV serie.
            - serie_nb_episode:
            - serie_certification : certificate of the TV serie (Tous public, 12, 16...).
            - serie_rating: rating of the TV serie.
    :rtype: tuple(list(str), string, string, list(str), list(str), string)
    """
    
    serie_title = serie_html.find('h1').text.strip()
    
    serie_genre=[]
    reg_search = re.compile('/search/title+')
    for div in serie_html.find_all("div", {"class":"see-more inline canwrap"}):
        for a in div.find_all("a", {"href": reg_search}):
            genre = a.text
            serie_genre.append(genre)
            
            
    nb_season=[]
    reg_season = re.compile('/title/')
    for div in serie_html.find_all("div", {"class":"seasons-and-year-nav"}):
        for c in div.find_all("a", {"href": reg_season}):
                season_not_filtered = c.text
                nb_season.append(season_not_filtered)
                serie_nb_season = ""
                if nb_season != 1:
                        serie_nb_season = nb_season[0]
                        
                        
    serie_nb_episode=serie_html.find('span', {'class':'bp_sub_heading'}).text
    
    
    reg = re.compile('/title/+')
    serie_type = serie_html.find("a", {"href": reg, "title":"See more release dates"}).text
    
    
    serie_actors=[]
    reg_name = re.compile('/name/nm+')
    for div in serie_html.find_all("div", {"class":"article", "id":"titleCast"}):
        for a in div.find_all("a", {"href": reg_name}):
            actors = a.text
            if actors != '':
                serie_actors.append(actors)
                
                
    serie_creators=[]
    for div in serie_html.find_all("div", {"class":"credit_summary_item"}):
        creators = ""
        if div.find("h4", {"class":"inline"}).text == "Creator:":
            for c in div.find_all("a", {"href": reg_name}):
                creators = c.text
                serie_creators.append(creators)
        elif div.find("h4", {"class":"inline"}).text == "Creators:":
            for c in div.find_all("a", {"href": reg_name}):
                creators = c.text
                serie_creators.append(creators)
                
    
    serie_origin=[]
    for div in serie_html.find_all("div", {"class":"txt-block"}):
        for h in div.find_all("h4", {"class":"inline"}):
            country = ""
            if h.text == "Country:":
                for a in div.find_all("a", {"href": reg_search}):
                    country = a.text
                    serie_origin.append(country)
    
    serie_language = ""
    for div in serie_html.find_all("div", {"class":"txt-block"}):
        for h in div.find_all("h4", {"class":"inline"}):
            if h.text == "Language:":
                for a in div.find_all("a", {"href": reg_search}):
                    serie_language = a.text
                    
                    
    
    certif =[]
    serie_certification = ""
    certificate_not_filtered = ""
    for div in serie_html.find_all("div", {"class":"txt-block"}):
        for h in div.find_all("h4", {"class":"inline"}):
            if h.text == "Certificate:":
                for s in div.find_all("span"):
                    certificate_not_filtered = s.text
                    certif.append(certificate_not_filtered)
                    if len(certif) != 1:
                        serie_certification = certif[0]
                        
                        
    serie_rating = serie_html.find('span', {'itemprop':'ratingValue'}).text
                        
    
    return(serie_title, serie_genre, serie_nb_season, serie_nb_episode, serie_type, serie_actors, serie_creators, serie_origin, serie_language, serie_certification,  serie_rating)


def get_serie_storyline(serie_html):
    
    """
    Return series storyline from the serie web page.
    
    :param serie_html: BeautifulSoup element that contains serie infos.
    :type serie_html: bs4.element.Tag.
    :return: storyline of the TV series.
    :rtype: tuple(string)
    """
    
    for div in serie_html.find_all("div", {"id":"titleStoryLine"}):
        for story in div.find_all("div", {"class":"inline canwrap"}):
            storyline = story.find("span").text
    
    return(storyline)



# Deal with all the information except the storyline.
%%time  # ~4min
serie_details = []

# Initiate the rank number.
rank_number = 0

# Take the first 100 series.
for n in range(len(serie_links)-150):
    
    rank_number = n + 1
    # Add rank_number at the en of the url.
    url_serie_rank = url_serie_ + str(rank_number)
    
    # Get the entire url of the page that contains serie informations.
    link_serie = url_imdb_base + serie_links[n] + url_serie_rank
    #print(link_serie) 
    
    html = get_html_from_link(link_serie)
    
    # Apply get_info_serie function to return every link informations.
    info = get_info_serie(html)
    # Add rank to the list return by the function get_info_serie.
    info = (rank_number,) + info
    
    # Info contains tuples : add them to a list.
    serie_details.append(info)
    #print(rank_number)

    
print(serie_details)



# Deal with the storylines.

%%time # ~3min30

serie_resume = []

#Initiate the rank number.
rank_number = 0

for n in range(len(serie_links)-150):
    
    rank_number = n + 1
    # Add rank_number at the en of the url.
    url_serie_rank = url_serie_ + str(rank_number)
    
    # Get the entire url of the page that contains serie informations.
    link_serie = url_imdb_base + serie_links[n] + url_serie_rank
    #print(link_serie) 
    
    html_story = get_html_from_link(link_serie)
    
    # Apply get_info_storyline function to return every storyline.
    serie_storyline = get_serie_storyline(html_story)
    
    serie_resume.append(serie_storyline)

    #print(rank_number) 



#Get list of rank numbers to insert into dataframe.

rank_number = 0
rank=[]

for n in range(len(serie_links)-150):
    
    rank_number = n + 1
    
    rank.append(rank_number)
    
#print(rank)



"""Put datas into dataframe"""
# Dataframe for all the oonformations except storylines.
df_serie = pd.DataFrame(serie_details, 
                        columns = ["Rank", "Title", "Genre", "Number_of_season", "Number_of_episodes", "Type", "Actors", 
                                   "Creators", "Origin", "Language", "Certification", "Rating"])

df_serie.to_csv('C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\series_data.csv', 
                index=False, header=True)


# Dataframe for storylines.
df_storyline = pd.DataFrame(serie_resume, columns=["Storyline"], index=rank)

df_storyline.to_csv('C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\series_storylines.csv', 
                header=True)
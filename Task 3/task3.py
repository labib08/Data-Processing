from typing import Dict, List
import pandas as pd
import json
import requests
import bs4
import urllib
import unicodedata
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
from robots import process_robots, check_link_ok

def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename.

    csv_dict = {}
    link_url_list = []
    seed_url_list = []
    words_list = []
    # All the link urls from the dictionary is fetched and stored
    # in another dictionary as a list.
    for key, value in link_dictionary.items():
        for url in value:
            link_url_list.append(url)
    link_url_list = sorted(link_url_list)
    csv_dict['link_url'] = link_url_list
    # All the links are visited and preprocessed just like in task2.
    for link_to_extract in csv_dict['link_url']:
        html_text = requests.get(link_to_extract)
        soup = BeautifulSoup(html_text.content, 'html.parser')
        information = soup.find('div', {"id" : "mw-content-text"})

        for elem in information.find_all('div', class_ = 'printfooter'):
            elem.clear()
        for elem in information.find_all('div', {"id" : "toc"}):
            elem.clear()
        for elem in information.find_all('table', class_ = 'ambox'):
            elem.clear()
        for elem in information.find_all('div', class_ = 'asbox'):
            elem.clear()
        for elem in information.find_all('span', class_ = 'mw-editsection'):
            elem.clear()
        for elem in information.find_all('th', class_ = 'infobox-label'):
            elem.clear()

        new_data = information.get_text(separator=" ")
        new_data = new_data.lower()
        new_data = unicodedata.normalize('NFKD', new_data)
        new_data = re.sub(r'[^A-Za-z\s]', ' ', new_data)
        new_data = re.sub(r'\s+', ' ', new_data)
        tokens = nltk.word_tokenize(new_data)

        stop_words = set(stopwords.words('english'))
        no_stopwords = [w for w in tokens if not w in stop_words]
        new_tokens = [i for i in no_stopwords if len(i)>1]
        porterStemmer = PorterStemmer()
        stemmed = [porterStemmer.stem(w) for w in new_tokens]
        string = ' '.join(stemmed)
        words_list.append(string)
    # The words are then stored in the dictionary 
    csv_dict['words'] = words_list
    # The seed urls belonging to particular link urls
    # are stored in the dictionary
    for link_1 in link_url_list:
        for key, value in link_dictionary.items():
            for link_2 in value:
                if link_1 == link_2:
                    seed_url_list.append(key)
    
    
    csv_dict['seed_url'] = seed_url_list
    # Finally a csv is created
    dataframe = pd.DataFrame(csv_dict)
    dataframe.to_csv(csv_filename)
    return dataframe
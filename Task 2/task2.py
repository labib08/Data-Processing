import json
from bs4 import BeautifulSoup
import requests
import bs4
import urllib
import unicodedata
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok

def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.

    word_dict = {}
    html_text = requests.get(link_to_extract)
    # Using beautiful soup to get the contents of this page.
    soup = BeautifulSoup(html_text.content, 'html.parser')
    information = soup.find('div', {"id" : "mw-content-text"})

    # Removing specific elements from the page.
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
    # Changing all characters to their casefold and normalizing them.
    new_data = new_data.lower()
    new_data = unicodedata.normalize('NFKD', new_data)
    # Converting all non-alphabetic characters to single space
    # characters.
    new_data = re.sub(r'[^A-Za-z\s]', ' ', new_data)
    new_data = re.sub(r'\s+', ' ', new_data)
    # The text is then converted to explicit tokens.
    tokens = nltk.word_tokenize(new_data)
    # Then all the stop words in nltk's list of English stopwords
    # are removed from the token.
    stop_words = set(stopwords.words('english'))
    no_stopwords = [w for w in tokens if not w in stop_words]
    # Then all the tokens that are less than two characters long
    # are removed from the text.
    new_tokens = [i for i in no_stopwords if len(i)>1]
    # Each token is then converted to Porter stemming algorithm
    porterStemmer = PorterStemmer()
    stemmed = [porterStemmer.stem(w) for w in new_tokens]
    word_dict[link_to_extract] = stemmed
    # A json file is then created.
    json_object = json.dumps(word_dict)
 
    with open(json_filename, "w") as outfile:
        outfile.write(json_object)
        
    with open(json_filename) as json_file:
        sample_json = json.load(json_file)
        
    print(sample_json)
    return {}
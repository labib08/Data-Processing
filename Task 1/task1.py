import pandas as pd
import json
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import urllib.parse
import re
from robots import process_robots, check_link_ok

# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000

def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    # Crawl each url in the starting_link list, and output
    # the links you find to a JSON file, with each starting
    # link as the key and the list of crawled links for the
    # value.
  
    my_dict = {}
    for seed_url in starting_links:
        my_list = []

        # The name of the domain is parsed from the link
        parsed = urllib.parse.urlsplit(seed_url)
        http_marker = seed_url[0:7]
        webpage_name = parsed.path.split("/")[-2]
        compiling_name = "^/" + webpage_name
        domain = urlparse(seed_url).netloc + '/' + webpage_name

        # The contents of the link is fetched
        key_link = seed_url
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        robots_url = 'http://115.146.93.142/robots.txt'
        page = requests.get(robots_url)
        robot_rules = process_robots(page.text)

        visited = {}
        visited[seed_url] = True
        pages_visited = 1

        
        # It removes the seed page
        links = soup.findAll('a')
        
        # We search for all links within the HTML document and store them in
        # the link variable 

        seed_link = soup.findAll('a', href=re.compile(http_marker)) 

        to_visit_relative = [l for l in links if l not in seed_link and "href" in l.attrs]


        to_visit = []
        for link in to_visit_relative:
            
            link = link['href']
            # Skip any links which Wikipedia has asked us not to visit.
            if not check_link_ok(robot_rules, link):
                continue
            if domain in urljoin(seed_url, link):
                if not "#" in urljoin(seed_url, link):
                    to_visit.append(urljoin(seed_url, link))  
        
        
        # Visit all the links and fetch any all the links inside them and so on and so forth.
        while (to_visit):
        # Impose a limit to avoid breaking the site 
            if pages_visited == SAFE_PAGE_LIMIT:
                break
            
            link = to_visit.pop(0)
            
            if link not in my_list:
                my_list.append(link)
            
            # Fetch the webpage
            page = requests.get(link)
            robot_rules = process_robots(page.text)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            # Mark the item as visited, i.e., add to visited list, remove from to_visit
            visited[link] = True
            new_links = soup.findAll('a', href=re.compile(compiling_name))
            for new_link in new_links:
                # Skip the links that don't have href values (links that don't actually exist or don't lead anywhere)
                if "href" not in new_link.attrs:
                    continue
                new_item = new_link['href']
                # Skip any links which Wikipedia has asked us not to visit.
                if not check_link_ok(robot_rules, new_item):
                    continue
                # Need to concat with base_url to get an absolute link, 
                # an example item <a href="/wiki/Category:Marvel_Cinematic_Universe_images_by_film_series"> 
                new_url = urljoin(link, new_item)
                # Check it's not already in the list before adding it.
                if new_url not in visited and new_url not in to_visit:
                    to_visit.append(new_url)
            # Increase the number of pages we've visited so the page limit is enforced.
            pages_visited = pages_visited + 1
        my_dict[key_link] = sorted(my_list)
                

    json_object = json.dumps(my_dict)
    
    # Writing to sample.json
    with open(json_filename, "w") as outfile:
        outfile.write(json_object)
    with open(json_filename) as json_file:
        sample_json = json.load(json_file)

    print(sample_json)
    return {}
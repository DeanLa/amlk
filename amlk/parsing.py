from amlk import *
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def get_article(url):
    '''gets link to article and returns the contents'''
    r = requests.get(url)
    if r.status_code == 200:
        return str(r.content)

def _parse_mako(html):
    '''gets html from mako and parses the needed text'''
    try:
        soup = BeautifulSoup(html, "html.parser")
    except:
        log("Couldn't beautifulsoup issue")
        return None, None, None

    # Extract title
    try:
        title = [p.get_text() for p in soup.find_all("h1", text=True)][0]
    except:
        log("Couldn't parse title")
        title = ''

    # Extract subtitle
    try:
        subtitle = [p.get_text() for p in soup.find_all("h2", text=True)][0]
    except:
        log("Couldn't parse subtitle")
        subtitle = ''

    # Extract paragraphs
    try:
        paragraphs = [p.get_text() for p in soup.find_all("p", text=True)]
    except:
        log("Couldn't parse paragraph")
        paragraphs = []

    return title, subtitle, paragraphs

def _parse_ynet(html):
    '''gets html from ynet and parses the needed text'''

    # Extract title
    try:
        title = re.findall(r'\"headline\": \"(.*)\"', html)[0]
    except:
        log("Couldn't parse title")
        title = ''

    # Extract subtitle
    try:
        subtitle = re.findall(r'\"description\": \"(.*)\"', html)[0]
    except:
        log("Couldn't parse subtitle")
        subtitle = ''

    # Extract paragraphs
    try:
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p", text=True)]
    except:
        log("Couldn't parse paragraphs")
        paragraphs = []

    return title, subtitle, paragraphs



def _parse_walla(html):
    '''gets html from walla and parses the needed text'''
    try:
        soup = BeautifulSoup(html, "html.parser")
    except:
        log("Couldn't parse Beautiful soup")
        return None, None, None

    # Extract title
    try:
        title = [p.get_text() for p in soup.find_all("h1", text=True)][0]
    except:
        log("Couldn't parse title")
        title = ''

    # Extract subtitle
    try:
        subtitle = [p.get_text() for p in soup.find_all(True, {"class": "subtitle"}, text=True)][0]
    except:
        log("Couldn't parse subtitle")
        subtitle = ''

    # Extract paragraphs
    try:
        paragraphs = [p.get_text() for p in soup.find_all("p", text=True)]
    except:
        log("Couldn't parse paragraph")
        paragraphs = []

    return title, subtitle, paragraphs

def which_domain(url):
    '''gets url and returns domain'''
    domains = ['ynet','walla','mako']
    for domain in domains:
        if domain in url:
            return domain
    return None
    
def parse_article(html, domain):
    '''gets html and parses it'''
    if domain is None:
        return None,None,None
    
    if domain == 'walla':
        parsed = _parse_walla(html)
    elif domain == 'ynet':
        parsed = _parse_ynet((html))
    elif domain == 'mako':
        parsed = _parse_mako(html)
    else:
        return None,None,None
    return parsed

def url_pipeline(title, subtitle, paragraphs):
    cols = ['article_id', 'domain', 'url', 'amlk', 'title', 'lang', 'created', 'user', 'extV', 'header1', 'header2', 'tags', 'content', 'teaser']
    rows = [(1,'', '', '', '','','','','',title, subtitle,'', paragraphs,'')]
    df = pd.DataFrame(rows, columns=cols)
    return df
from amlk import *
import requests
import re
from bs4 import BeautifulSoup

def get_article(url):
    '''gets link to article and returns the contents'''


def _parse_mako(html):
    '''gets html from mako and parses the needed text'''

def _parse_ynet(html):
    '''gets html from ynet and parses the needed text'''
    with open(html, "r") as f:
        content = f.read()

    # Extract title
    titles = re.findall(r'\"headline\": \"(.*)\"', content)
    for t in titles:
        title = t.decode('UTF-8')[::-1]

    # Extract subtitle
    subtitles = re.findall(r'\"description\": \"(.*)\"', content)
    for t in subtitles:
        subtitle = t.decode('UTF-8')[::-1]

    print("Title: " + title)
    print("Subtitle: " + subtitle)

    # Extract paragraphs
    soup = BeautifulSoup(content.decode('UTF-8'), "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    for count, p in enumerate(paragraphs):
        print("Paragraph " + str(count) + ": " + p[::-1])


def _parse_walla(html):
    '''gets html from walla and parses the needed text'''

def which_domain(url):
    '''gets url and returns domain'''

def parse_article(html, domain):
    '''gets html and parses it'''
    if domain == 'walla':
        parsed = _parse_walla(html)
    elif domain == 'ynet':
        parsed = _parse_ynet((html))
    elif domain == 'mako':
        parsed = _parse_mako(html)
    return parsed


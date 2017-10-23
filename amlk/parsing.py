from amlk import *
import requests

def get_article(url):
    '''gets link to article and returns the contents'''


def _parse_mako(html):
    '''gets html from mako and parses the needed text'''

def _parse_ynet(html):
    '''gets html from mako and parses the needed text'''

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
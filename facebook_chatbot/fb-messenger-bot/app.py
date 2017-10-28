# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import json
from datetime import datetime
from ...amlk import *
import requests
from flask import Flask, request
import re
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import numpy as np
import string

app = Flask(__name__)



# dfhandling.py
# def create_sentences(inp):
#     '''splits a given article to sentences'''
#     out = []
#     if inp == None: return []
#     for i, row in enumerate(inp):
#         _new_sents = []
#         all_punc = re.findall('\. |\r|\n|\! |\? |\.\.\.', row)
#         for punc in all_punc:
#             ind = row.find(punc) + len(punc)
#             _new_sents.append(row[0:ind - len(punc)] + ' ' + punc)
#             row = row[ind:]
#         out.extend([(sent, i, j) for j, sent in enumerate(_new_sents) if len(sent) > 5])
#     return out
#
#
# def get_text(lst, ind):
#     '''returns lst[ind] if possible, else None'''
#     try:
#         return lst[ind]
#     except:
#         return None
#
#
# def add_sent_cols(df, df_sents_col='sentences'):
#     '''creates columns for each sentence in df'''
#     maxsents = df.sentences.map(len).max()
#     data = df
#     for i in range(maxsents):
#         data['col_' + str(i)] = df[df_sents_col].map(lambda x: get_text(x, i))
#     return data
#
#
# def tokenize(sent, to_low=True):
#     '''sentence as an input, returns the tokenized word in a list '''
#     newsent = [sent[0]]
#     for ch in sent[1:]:
#         if ch in string.punctuation:
#             if not newsent[-1].isalpha():
#                 newsent.append(ch)
#             else:
#                 newsent += [' ', ch, ' ']
#         else:
#             if newsent[-1] in string.punctuation and ch.isalpha():
#                 newsent.append(' ')
#             newsent.append(ch)
#     words = [x for x in ''.join(newsent).split(' ') if x != '']
#     if to_low:
#         return [w.lower() for w in words]
#     else:
#         return words
#
#
# def sent_to_token(sent):
#     try:
#         if type(sent) != unicode:
#             sent = sent.decode('utf-8')
#         return [i[1] for i in hebtokenizer.tokenize(sent)]
#     except:
#         return []
#
#
# def to_ngrams(words, n=3):
#     # take ngrams
#     out_ngrams = []
#     try:
#         for w in words:
#             for i in range(max(len(w) - n + 1, 1)):
#                 out_ngrams.append(w[i:i + n])
#         return out_ngrams
#     except:
#         return []
#
#
# # In[13]:
#
# def make_df(df):
#     # extract sentenses from raw text content
#     df['sentences'] = df.content.map(create_sentences)
#     df['num_of_sents'] = df.sentences.map(len)
#     # add sentences as columns
#     df = add_sent_cols(df)
#     # find all not-sentence columns and melt
#     maxcol = list(df.columns).index('col_0')
#     df_melt = df.melt(df.columns[:maxcol])
#     df_melt.rename(str, {'variable': 'sent_loc', 'value': 'sent'}, inplace=True)
#     # add sentence location and filter empty content
#     df_melt.sent_loc = df_melt.sent_loc.map(lambda x: int(x.split('_')[1]))
#     df_melt = df_melt[~df_melt.sent.isnull()]
#
#     df_melt['paragraph'] = df_melt.sent.map(lambda x: x[1])
#     df_melt['loc_in_par'] = df_melt.sent.map(lambda x: x[2])
#     df_melt['sent'] = df_melt.sent.map(lambda x: x[0])
#     df_melt['sent_words'] = df_melt.sent.map(sent_to_token)
#     df_melt['header1_words'] = df_melt.header1.map(sent_to_token)
#     df_melt['header2_words'] = df_melt.header2.map(sent_to_token)
#
#     df_melt['ng_sent'] = df_melt.sent_words.map(lambda x: set(to_ngrams(x)))
#     df_melt['ng_head1'] = df_melt.header1_words.map(lambda x: set(to_ngrams(x)))
#     df_melt['ng_head2'] = df_melt.header2_words.map(lambda x: set(to_ngrams(x)))
#     return df_melt

# # pipeline.py
# def url_pipeline(title, subtitle, paragraphs):
#     cols = ['article_id', 'domain', 'url', 'amlk', 'title', 'lang', 'created', 'user', 'extV', 'header1', 'header2', 'tags', 'content', 'teaser']
#     rows = [(1,'', '', '', '','','','','',title, subtitle,'', paragraphs,'')]
#     df = pd.DataFrame(rows, columns=cols)
#     return df

# def _parse_mako(html):
#     '''gets html from mako and parses the needed text'''
#     try:
#         soup = BeautifulSoup(html, "html.parser")
#     except:
#         log("Couldn't beautifulsoup issue")
#         return None, None, None
#
#     # Extract title
#     try:
#         title = [p.get_text() for p in soup.find_all("h1", text=True)][0]
#     except:
#         log("Couldn't parse title")
#         title = ''
#
#     # Extract subtitle
#     try:
#         subtitle = [p.get_text() for p in soup.find_all("h2", text=True)][0]
#     except:
#         log("Couldn't parse subtitle")
#         subtitle = ''
#
#     # Extract paragraphs
#     try:
#         paragraphs = [p.get_text() for p in soup.find_all("p", text=True)]
#     except:
#         log("Couldn't parse paragraph")
#         paragraphs = []
#
#     return title, subtitle, paragraphs


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
    domains = ['ynet', 'walla', 'mako']
    for domain in domains:
        if domain in url:
            return domain
    return None


def parse_article(html, domain):
    '''gets html and parses it'''
    if domain is None:
        return None, None, None

    if domain == 'walla':
        parsed = _parse_walla(html)
    elif domain == 'ynet':
        parsed = _parse_ynet(html)
    elif domain == 'mako':
        parsed = _parse_mako(html)
    else:
        return None, None, None
    return parsed


# app.py
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":
        for entry in data["entry"]:
            if "messaging" in entry:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):  # someone sent us a message
                        try:
                            sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                            recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                            message_text = messaging_event["message"]["text"]  # the message's text
                        except:
                            return "ok", 200

                        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_text)
                        if len(urls) == 0:
                            rank = re.findall("[1-5]",message_text)
                            if len(rank) == 0:
                                send_message(sender_id, u'שלח לינק לכתבה לקבלת אמ;לק')
                            else:
                                send_message(sender_id, u'תודה!')
                        else:
                            domain = which_domain(urls[0])
                            if domain not in ['ynet', 'walla', 'mako']:
                                send_message(sender_id, u'זוהי גרסה ראשונית של הבוט, האתרים הנתמכים הם ynet, mako ו-walla')
                            else:
                                try:
                                    #domain = "mako"
                                    #urls[0] = "http://www.deanla.com"
                                    log("URL " + urls[0])
                                    r = requests.get(urls[0])
                                    log("Got request")
                                    if r.status_code == 200:
                                        log("Status code 200")
                                        log(domain)
                                        t, s, ps = parse_article(str(r.content), domain)
                                        #log(t.decode("utf-8"))
                                        #log(s.decode("utf-8"))
                                        if domain == "ynet":
                                            sub = s.decode("utf-8")
                                            title = t.decode("utf-8")
                                        else:
                                            sub = s
                                            title = t

                                        log("Finished parsing")

                                        # Get TLDR from model
                                        #data_frame = url_pipeline(title, sub, ps)
                                        #df = make_df(data_frame)
                                        #log(df.shape)
                                        #log("Built data frame")

                                        #send_message(sender_id, title)
                                        send_message(sender_id, sub)
                                        send_message(sender_id, u'לצורכי שיפור נשמח אם תדרג את האמ;לק בין 1-5')

                                        #send_message(sender_id, ps[0])
                                    else:
                                        send_message(sender_id, u'הלינק ששלחת לא תקין')
                                except Exception as e:
                                    log(e)
                                    send_message(sender_id, u'שגיאה בקריאת הכתבה')

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
    return "ok", 200

def send_message(recipient_id, message_text):

    #log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


#if __name__ == '__main__':
    #app.run(debug=True)

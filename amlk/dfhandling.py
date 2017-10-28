from __future__ import division
from amlk import *
import pandas as pd
import numpy as np
import pickle
import re
import string

from collections import Counter


def create_sentences(inp):
    '''splits a given article to sentences'''
    out = []
    if inp == None: return []
    for i, row in enumerate(inp):
        _new_sents = []
        all_punc = re.findall('\. |\r|\n|\! |\? |\.\.\.', row)
        for punc in all_punc:
            ind = row.find(punc) + len(punc)
            _new_sents.append(row[0:ind - len(punc)] + ' ' + punc)
            row = row[ind:]
        out.extend([(sent, i, j) for j, sent in enumerate(_new_sents) if len(sent) > 5])
    return out


def get_text(lst, ind):
    '''returns lst[ind] if possible, else None'''
    try:
        return lst[ind]
    except:
        return None


def add_sent_cols(df, df_sents_col='sentences'):
    '''creates columns for each sentence in df'''
    maxsents = df.sentences.map(len).max()
    data = df
    for i in range(maxsents):
        data['col_' + str(i)] = df[df_sents_col].map(lambda x: get_text(x, i))
    return data


def tokenize(sent, to_low=True):
    '''sentence as an input, returns the tokenized word in a list '''
    newsent = [sent[0]]
    for ch in sent[1:]:
        if ch in string.punctuation:
            if not newsent[-1].isalpha():
                newsent.append(ch)
            else:
                newsent += [' ', ch, ' ']
        else:
            if newsent[-1] in string.punctuation and ch.isalpha():
                newsent.append(' ')
            newsent.append(ch)
    words = [x for x in ''.join(newsent).split(' ') if x != '']
    if to_low:
        return [w.lower() for w in words]
    else:
        return words


def sent_to_token(sent):
    try:
        if type(sent) != unicode:
            sent = sent.decode('utf-8')
        return [i[1] for i in hebtokenizer.tokenize(sent)]
    except:
        return []


def to_ngrams(words, n=3):
    # take ngrams
    out_ngrams = []
    try:
        for w in words:
            for i in range(max(len(w) - n + 1, 1)):
                out_ngrams.append(w[i:i + n])
        return out_ngrams
    except:
        return []


# In[13]:

def make_df(df):
    # extract sentenses from raw text content
    df['sentences'] = df.content.map(create_sentences)
    df['num_of_sents'] = df.sentences.map(len)
    # add sentences as columns
    df = add_sent_cols(df)
    # find all not-sentence columns and melt
    maxcol = list(df.columns).index('col_0')
    df_melt = df.melt(df.columns[:maxcol])
    df_melt.rename(str, {'variable': 'sent_loc', 'value': 'sent'}, inplace=True)
    # add sentence location and filter empty content
    df_melt.sent_loc = df_melt.sent_loc.map(lambda x: int(x.split('_')[1]))
    df_melt = df_melt[~df_melt.sent.isnull()]

    df_melt['paragraph'] = df_melt.sent.map(lambda x: x[1])
    df_melt['loc_in_par'] = df_melt.sent.map(lambda x: x[2])
    df_melt['sent'] = df_melt.sent.map(lambda x: x[0])
    df_melt['sent_words'] = df_melt.sent.map(sent_to_token)
    df_melt['header1_words'] = df_melt.header1.map(sent_to_token)
    df_melt['header2_words'] = df_melt.header2.map(sent_to_token)

    df_melt['ng_sent'] = df_melt.sent_words.map(lambda x: set(to_ngrams(x)))
    df_melt['ng_head1'] = df_melt.header1_words.map(lambda x: set(to_ngrams(x)))
    df_melt['ng_head2'] = df_melt.header2_words.map(lambda x: set(to_ngrams(x)))
    return df_melt




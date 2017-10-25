from tqdm import tqdm
from amlk import *
import pandas as pd
import json
import _thread

df = pd.read_csv('../DH17/chrome_data.csv', names=['article_id','domain','url','amlk','title','lang','created','user','extV'])
print ('Loaded table')
g = df.groupby('domain').article_id.agg('count').sort_values(ascending=False)
domains = g.iloc[:3].index.tolist()
df = df[df.domain.isin(domains)][['article_id', 'domain', 'url', 'amlk', 'title', 'lang', 'created']]

def download_articles(urls, start_i, end_i, thread_name, save_after=500):
    contents = {}
    for i in range(start_i, end_i):
        url = urls[i]
        print (i,'   ', url)
        try:
            contents[url] = get_article(url)
        except:
            pass
        if i % save_after == 0:
            filename = '../DH17/article_contents/contents_{}_{}.json'.format(i,thread_name)
            with open(filename, 'w') as f:
                f.write(json.dumps(contents, indent=2))
                # del (contents)
                contents = {}
    filename = '../DH17/article_contents/contents_{}_{}_left_over.json'.format(i, thread_name)
    with open(filename, 'w') as f:
        f.write(json.dumps(contents, indent=2))

urls = df.url.tolist()
try:
    _thread.start_new_thread(download_articles, (urls, 22501, 22800, "th_1", 500))
    _thread.start_new_thread(download_articles, (urls, 22801, 23100, "th_2", 500))
    _thread.start_new_thread(download_articles, (urls, 23101, 23400, "th_3", 500))
    _thread.start_new_thread(download_articles, (urls, 23401, 23700, "th_4", 500))
    _thread.start_new_thread(download_articles, (urls, 23701, 24000 , "th_5", 500))
except:
    print ("nope")

while True:
    pass
# start_i=0
# contents = {}
# save_after = 500
# for i in tqdm(range(start_i, len(urls))):
#     url = urls[i]
#     # if url in contents: continue
#     contents[url] = get_article(url)
#     if i % save_after == 0:
#         filename = '../DH17/article_contents/contents_{}.json'.format(i)
#         with open(filename, 'w') as f:
#             f.write(json.dumps(contents, indent=2))
#             # del (contents)
#             contents = {}
# filename = '../DH17/article_contents/contents_{}.json'.format(i)
# with open(filename, 'w') as f:
#     f.write(json.dumps(contents, indent=2))
#     # del (contents)
#     contents = {}

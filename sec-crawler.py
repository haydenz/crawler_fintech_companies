#!/usr/bin/env python3

import nltk
# nltk.download('punkt')
import requests
from bs4 import BeautifulSoup
import re
import sys
import pandas as pd
import os
from os.path import dirname, abspath, join
from operator import itemgetter

url_comments = 'https://www.sec.gov/rules/proposed/s73199.shtml'

def html_download(url):
    if url is None:
        return None
    try:
        response = requests.get(url)
    except Exception as error:
        print("Open the url failed, error: {}".format(error))
        return None
    if response.status_code != 200:
        return None
    return response.content

def html_pharse(html_content):
    comments_list = []
    if html_content is None:
        return None
    soup = BeautifulSoup(html_content, "lxml", from_encoding = "gb18030") # replaced 'html.parser'
    comments = soup.find_all('li')

    for comment in comments:
        comment_info_dict = { "txt_length": "",
                              "sentence": "",
                              "comment_name" : "",
                              "txt_name": "",
                              "txt_url" : "",
                              "txt_content": "",
                              }
        comment_info_dict["comment_name"] = comment.text
        for txt in comment.find_all("a"):
            comment_info_dict["txt_url"] = "https://www.sec.gov" + txt.attrs["href"]
            comment_info_dict["txt_name"] = txt.text         
        comments_list.append(comment_info_dict)

    return comments_list

def txt_length(html_content):
    if html_content is None:
        return 0

    soup = BeautifulSoup(html_content, "lxml", from_encoding = "gb18030")
    text = str(soup.body)
    return text, len(text)

def comments_selector(comments_list):
    desired_list = []
    key_words = ['expert', 'knowledge', 'sophisticated investor']

    for c in comments_list:
        txt_raw = html_download(c["txt_url"])
        c["txt_content"], c["txt_length"] = txt_length(txt_raw)
        matches = []

        for k in key_words:
            for match in re.finditer(k, c["txt_content"].lower()):
                    start = match.start()
                    end = match.end()
                    splits = nltk.sent_tokenize(c["txt_content"][max(start-20,0):min(end+20, c["txt_length"])]) # generate full sentences
                    for s in splits:
                        if k in s:
                            matches.append(s) 
        
        c['sentence'] = matches
        if len(matches) != 0:
            desired_list.append(c)

    # order by the length
    ordered_list = sorted(desired_list, key=itemgetter('txt_length'), reverse=True)
    df = pd.DataFrame(ordered_list).loc[:, ["txt_length","sentence","comment_name","txt_name","txt_url"]]
    df.to_csv(join(os.getcwd(), "result.csv"))
    print("Finished! The total number of matches is %i" % len(desired_list))

if __name__ == '__main__':
    html_content = html_download(url_comments)
    raw_data = html_pharse(html_content)
    comments_selector(raw_data)

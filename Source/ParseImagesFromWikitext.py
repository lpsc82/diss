# -*- coding: utf-8 -*-

import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import mwparserfromhell as mwp
import os
from textstat.textstat import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import porter, RSLPStemmer
from nltk.corpus import stopwords
from mwtemplates import TemplateEditor
import ApiInterface as ai
import codecs
import wikitextparser as wtp
import DatabaseInterface as di

database = di.DataInterface()

articles = database.getAllAnalyzedArticles()

for article in articles:

    try:    
        with open("../content/"+article['ba_name'].replace("/","_")+"_"+article['ba_lang']+"_wiki.dat", "r") as file:        

            content = file.read()
            wtparsed = wtp.parse(content)

            for link in wtparsed.wikilinks:
                if "File:" in link.target or "Image:" in link.target:
                    imagetitle = link.target.replace("File:","").replace("Image:","")
                    extension = imagetitle.split('.')[-1]
                    type = ai.getExtensionType(extension)
                    typeID = database.getMediaTypeID(type)
                    database.insertMedia(article['ba_id'], imagetitle, typeID)
                    print("Image %s inserted in article %s" % (imagetitle, article['ba_id']))
    except FileNotFoundError:
        print('Not a valid file.')
        continue

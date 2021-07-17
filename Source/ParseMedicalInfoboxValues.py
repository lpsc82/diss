# -*- coding: utf-8 -*-

import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import mwparserfromhell as mwp
import os
from mwtemplates import TemplateEditor
import ApiInterface as ai
import codecs
import wikitextparser as wtp
import DatabaseInterface as di

database = di.DataInterface()

articles = database.getAllAnalyzedArticles()

infoboxesquery = database.getAllInfoboxes()
infoboxes = {}
for info in infoboxesquery:
    infoboxes[info["info_name"]] = info["info_id"]

counter = 0

for article in articles:
    
    print(len(articles) - counter)
    counter = counter+1

    with open("../content/"+article['ba_name'].replace("/","_")+"_"+article['ba_lang']+"_wiki.dat", "r") as file:

        content = file.read()

        te = TemplateEditor(content)

        for(key, value) in te.templates.items():
            if key in infoboxes:
                for temp in value[0].parameters.keys():
                    print("Inserted key %s value %s infobox %s article %s" % (temp, value[0].parameters[temp], key, article["ba_name"]))
                    database.insertInfoboxValue(str(temp), str(value[0].parameters[temp]), article["ba_id"], str(infoboxes[key]))

# -*- coding: utf-8 -*-
 
import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle")
articles = c.fetchall()
print("Total of %s articles", (len(articles),))

def returnQueryJson(url):
    requestResult = http.urlopen(url).read().decode("utf8")
    result = json.loads(requestResult, encoding="utf8")
    return result

def updateBrokenArticle(articleID):
    c.execute("update BaseArticle set ba_broken=True where ba_id=%s", (articleID,))

counter = 0

for article in articles:
    print("Current article: %s" % (article['ba_name'],))
    print(len(articles) - counter)
    counter = counter +1
    content = returnQueryJson("https://"+article['ba_lang']+".wikipedia.org/w/api.php?action=query&titles="+urllib.parse.quote(article["ba_name"])+"&prop=links&utf8&format=json")
    if "-1" in content["query"]["pages"]:
        print("Article %s of id %s is broken" % (article["ba_name"], article["ba_id"]))
        updateBrokenArticle(article["ba_id"])

conn.commit()

# -*- coding: utf-8 -*-
 
import mysql.connector
import urllib.request as http
import urllib
import json
import re
from html.parser import HTMLParser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

def returnQueryJson(url):
    requestResult = http.urlopen(url).read().decode("utf8")
    result = json.loads(requestResult, encoding="utf8")
    return result
       
def processArticles():
    # Get all articles
    # Get all corresponding categories
    # Insert categories
    # Insert category links

    c.execute("SELECT * FROM BaseArticle WHERE ba_analyzed = TRUE")
    articles = c.fetchall()
    
    counter = 0

    for article in articles:
        if (article['ba_id']) not in [717, 1527]:
            print("Article %s" % (article['ba_name'].encode('utf8'),))
            print(article['ba_id'])
            print ("%s / %s" % (counter, len(articles)))
            counter = counter +1
            categoryUrl = ("https://en.wikipedia.org/w/api.php?action=query&prop=categories&redirects&titles=" +
                urllib.parse.quote(article['ba_name']) + "&formatversion=2&utf8&clshow=!hidden&format=json")
            tempCategories = returnQueryJson(categoryUrl)
            categories = tempCategories['query']['pages'][0]['categories']

            while "continue" in tempCategories:
                continueCode = tempCategories['continue']['clcontinue']
                tempCategories = returnQueryJson(categoryUrl+"&clcontinue=" + continueCode)
                categories.extend(tempCategories['query']['pages'][0]['categories'])
            
            # Insert categories in database
            for category in categories:
                print("Inserting category %s" % (category['title'].encode('utf8'),))
                
                c.execute("SELECT * FROM Category WHERE cat_name = %s", (category['title'],))
                tempCat = c.fetchall()
                if not tempCat:            
                    c.execute("INSERT INTO Category (cat_name) VALUES (%s)", (category['title'],))
                    conn.commit()
                    c.execute("SELECT * FROM Category WHERE cat_name = %s", (category['title'],))
                    tempCat = c.fetchall()

                c.execute("INSERT IGNORE INTO CategoryLink (cl_article, cl_category) VALUES (%s, %s)",
                    (article['ba_id'], tempCat[0]['cat_id']))
                conn.commit()

    print("Finished")

processArticles()

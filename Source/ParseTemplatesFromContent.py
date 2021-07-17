# -*- coding: utf-8 -*-
 
import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics
from mwtemplates import TemplateEditor

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle WHERE ba_analyzed = TRUE")
articles = c.fetchall()

def loadMedicineTemplates():
    entemplates = []
    detemplates = []
    pttemplates = []
    catemplates = []
    ittemplates = []
    rutemplates = []
    frtemplates = []  
    
    with open("../dataset/templates/pt_templates.txt", "r") as ptfile:  
        for line in ptfile:
            pttemplates.append(line.replace("\n",""))  
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "pt"))  
    
            
    with open("../dataset/templates/en_templates.txt", "r") as ptfile:
        for line in ptfile:
            entemplates.append(line.replace("\n",""))
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "en"))

    with open("../dataset/templates/fr_templates.txt", "r") as ptfile:
        for line in ptfile:
            frtemplates.append(line.replace("\n",""))
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "fr")) 

    with open("../dataset/templates/de_templates.txt", "r") as ptfile:  
        for line in ptfile:
            detemplates.append(line.replace("\n",""))  
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "de"))  
    
    with open("../dataset/templates/ca_templates.txt", "r") as ptfile:  
        for line in ptfile:
            catemplates.append(line.replace("\n",""))  
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "ca"))  

    with open("../dataset/templates/it_templates.txt", "r") as ptfile:  
        for line in ptfile:
            ittemplates.append(line.replace("\n",""))  
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "it"))  

    with open("../dataset/templates/ru_templates.txt", "r") as rufile:  
        for line in rufile:
            rutemplates.append(line.replace("\n",""))  
            c.execute("INSERT INTO MedicineTemplate(medtemp_name, medtemp_lang) VALUES (%s,%s)",
                    (line.replace("\n",""), "ru"))  
       

    return entemplates,pttemplates,frtemplates, detemplates, catemplates, ittemplates, rutemplates  


def findSelectTemplates(articleText, article):
    te = TemplateEditor(articleText)

    for(key, value) in te.templates.items():
        if key in entemplates or key in pttemplates or key in frtemplates or key in detemplates or key in catemplates or key in ittemplates or key in rutemplates:
            c.execute("SELECT * FROM MedicineTemplate WHERE medtemp_name=%s and medtemp_lang=%s", (key,article['ba_lang']))
            templates = c.fetchall()
            if len(templates) > 0:
                print("\t"+key)
                c.execute("INSERT INTO MedicineTemplateArticle(medba_article, medba_template) VALUES (%s,%s)",
                    (article['ba_id'], templates[0]['medtemp_id']))

    conn.commit()

entemplates, pttemplates, frtemplates, detemplates, catemplates, ittemplates, rutemplates = loadMedicineTemplates()

for article in articles:
    with open("../content/"+article['ba_name'].replace("/","_")+"_"+article['ba_lang']+"_wiki.dat", "r") as file:
        content = file.read()
        print("Article: " + article["ba_name"])
        findSelectTemplates(content,article)

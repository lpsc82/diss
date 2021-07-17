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

def insertTemplate(key, val, article):
    c.execute("INSERT IGNORE INTO Template (temp_article, temp_key, temp_value) VALUES " +
        "(%s, %s, %s)", (article, str(key), str(val)))
    conn.commit()


DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle where ba_analyzed=True")
articles = c.fetchall()

infoboxResources = ["ICD11", "ICD10", "ICD9", "ICDO", "OMIM", "DiseasesDB", "MedlinePlus",
    "eMedicineSubj", "eMedicineTopic", "MeSH", "GeneReviewsNBK", "GeneReviewsName", "Orphanet", "CID11", "CID10",
    "CID9", "CIDO", "MeshID"]

for article in articles:

    with open("../content/"+article['ba_name'].replace("/","_")+"_"+article['ba_lang']+"_wiki.dat", "r") as file:

        content = file.read()

        # Extract table number

        wtparsed = wtp.parse(content)

        tablenumber = 0 

        c.execute("UPDATE BaseArticle SET ba_list = %s WHERE ba_id = %s", (article['ba_list'], article['ba_id']))

        # Extract captions

        # Extract remaining templates

        # Extract missing external resources

        te = TemplateEditor(content)

        keyCount = 0

        for (key, value) in te.templates.items():

            # This is done separately to other Classification templates because these are not templates but keys/values in templates

            if(key == "Medical resources" or key=="Infobox medical condition" or key == "Infobox Maladie"): ### TODO
                temp = value[0].parameters
                # Infobox medical condition
                if "GeneReviewsNBK" in temp and "GeneReviewsName" in temp:
                    val1 = temp["GeneReviewsNBK"]
                    val2 = temp["GeneReviewsName"]
                    if val1 != "" and val2 != "":
                        insertTemplate("GeneReviews", str(val1) + "/" + str(val2), article['ba_id'])
                if "GeneReviewsNBK2" in temp and "GeneReviewsName2" in temp:
                    val1 = temp["GeneReviewsNBK2"]
                    val2 = temp["GeneReviewsName2"]
                    if val1 != "" and val2 != "":
                        insertTemplate("GeneReviews", str(val1) + "/" + str(val2), article['ba_id'])
                if "Orphanet" in temp:
                    val = temp["Orphanet"]
                    if val != "":
                        insertTemplate("Orphanet", val, article['ba_id'])
                # Medical resources
                if "NORD" in temp:
                    val = temp["NORD"]
                    if val != "":
                        insertTemplate("NORD", val, article['ba_id'])
                if "GARDNum" in temp and "GARDName" in temp:
                    val1 = temp["GARDNum"]
                    val2 = temp["GARDName"]
                    if val1 != "" and val2 != "":
                        insertTemplate("GARD", str(val1) + "/" + str(val2), article['ba_id'])
                if "AO" in temp:
                    val = temp["AO"]
                    if val != "":
                        insertTemplate("AO", val, article['ba_id'])
                if "RP" in temp:
                    val = temp["RP"]
                    if val != "":
                        insertTemplate("RP", val, article['ba_id'])
                if "WO" in temp:
                    val = temp["WO"]
                    if val != "":
                        insertTemplate("WO", val, article['ba_id'])
                if "OrthoInfo" in temp:
                    val = temp["OrthoInfo"]
                    if val != "":
                        insertTemplate("OrthoInfo", val, article['ba_id'])
                if "NCI" in temp:
                    val = temp["NCI"]
                    if val != "":
                        insertTemplate("NCI", val, article['ba_id'])
                if "Scholia" in temp:
                    val = temp["Scholia"]
                    if val != "":
                        insertTemplate("Scholia", val, article['ba_id'])
                if "SNOMED CT" in temp:
                    val = temp["SNOMED CT"]
                    if val != "":
                        insertTemplate("SNOMED CT", val, article['ba_id'])
            
            if(key == "Infobox medical condition (new)"):
                temp = value[0].parameters
                for templatekey in list(temp.keys()):
                    if temp[templatekey] != "":
                        keyCount = keyCount + 1
            if(key == "Infobox medical condition" or key == "Info/Patologia" or key == "Infobox Maladie"): ###TODO
                temp = value[0].parameters
                for templatekey in list(temp.keys()):
                    if temp[templatekey] != "" and templatekey not in infoboxResources:
                        keyCount = keyCount + 1
        
        c.execute("UPDATE BaseArticle SET ba_list = %s, ba_keycount=%s WHERE ba_id = %s", (tablenumber, keyCount, article['ba_id']))
        conn.commit()

        print("Article %s of id %s has %s lists and %s extra keys" % (article['ba_name'], article['ba_id'], tablenumber, keyCount))





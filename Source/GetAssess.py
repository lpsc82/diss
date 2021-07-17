#!/usr/bin/python3

#Passa os users que forem admin a 'true'

from lxml import html, etree
import mysql.connector
import requests
import urllib.request as http
import urllib
import json
import sys
import os

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

b_file= open("../dataset/B.txt", "r")
c_file= open("../dataset/C.txt", "r")
fa_file= open("../dataset/FA.txt", "r")
ga_file= open("../dataset/GA.txt", "r")
list_file= open("../dataset/List.txt", "r")
start_file= open("../dataset/Start.txt", "r")

for assess in b_file:
    parsed_assess = assess.replace("\n", " ")
    c.execute("Update BaseArticle set ba_assess='B' where ba_name=%s", (assess,))
    print (parsed_assess)
    
conn.commit()

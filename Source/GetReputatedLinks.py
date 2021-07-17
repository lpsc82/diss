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

lang = "en"
if len(sys.argv) > 1:    
    lang = " ".join(sys.argv[1:])

if lang == "en": #TODO: adicionar linguas/admins
    # English

    english_file = open("../dataset/reputated_sites.txt", "r")

    print("Starting")

    for username in english_file:
        parsed_username = username.replace("\n", "")
        c.execute("UPDATE OuterLinksTo SET ol_reputated=True WHERE ol_url LIKE CONCAT('%', %s, '%')", (parsed_username,))
        print("LINK: %s" % (parsed_username))

else:
    print("Insert valid language")

conn.commit()

#!/usr/bin/python3

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

if lang == "en":

    english_file = open("../dataset/sections.txt", "r")

    print("Starting")

    for username in english_file:
        parsed_username = username.replace("\n", "")
        c.execute("UPDATE Section SET sec_recommended=True WHERE sec_name=%s", (parsed_username,))
        print("NAME: %s" % (parsed_username))

else:
    print("Insert valid language")

conn.commit()

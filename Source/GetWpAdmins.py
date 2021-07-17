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
    # English

    english_file = open("../dataset/wp_admins.txt", "r")

    print("Starting")

    for username in english_file:
        parsed_username = username.replace("\n", "")
        c.execute("Update User set user_wp=True where user_name=%s", (parsed_username,))
        print("Username: %s" % (parsed_username,))

elif lang == "pt":
    # Portuguese

    portuguese_file = open("../dataset/portuguese_admins.txt", "r")

    print("Starting portuguese")

    for username in portuguese_file:
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("PT Username: %s" % (parsed_username,))
else:
    print("Insert valid language")

conn.commit()

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

lang = "zz"
if len(sys.argv) > 1:    
    lang = " ".join(sys.argv[1:])

if lang == "en":
    english_file = open("../dataset/admins/en_admins.txt", "r")

    print("Starting English")

    for username in english_file:
        parsed_username = username.replace("\n", "")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("Username: %s" % (parsed_username,))

elif lang == "pt":
    portuguese_file = open("../dataset/admins/pt_admins.txt", "r")  

    print("Starting portuguese")  

    for username in portuguese_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("PT Username: %s" % (parsed_username,))  

elif lang == "fr":
    fr_file = open("../dataset/admins/fr_admins.txt", "r")

    print("Starting french")

    for username in fr_file:
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("FR Username: %s" % (parsed_username,))

elif lang == "de":
    de_file = open("../dataset/admins/de_admins.txt", "r")  

    print("Starting Deutsch")  

    for username in de_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("DE Username: %s" % (parsed_username,))  

elif lang == "ca":
    ca_file = open("../dataset/admins/ca_admins.txt", "r")  

    print("Starting Catalan")  

    for username in ca_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("CA Username: %s" % (parsed_username,))  

elif lang == "it":
    it_file = open("../dataset/admins/it_admins.txt", "r")  

    print("Starting Italian")  

    for username in it_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("IT Username: %s" % (parsed_username,))  

elif lang == "ru":
    ru_file = open("../dataset/admins/ru_admins.txt", "r")  

    print("Starting Russian")  

    for username in ru_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("RU Username: %s" % (parsed_username,))  

elif lang == "ar":
    ar_file = open("../dataset/admins/ar_admins.txt", "r")  

    print("Starting Arabian")  

    for username in ar_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("AR Username: %s" % (parsed_username,))  

elif lang == "id":
    id_file = open("../dataset/admins/id_admins.txt", "r")  

    print("Starting Indonesian")  

    for username in id_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("ID Username: %s" % (parsed_username,))  

elif lang == "tr":
    tr_file = open("../dataset/admins/tr_admins.txt", "r")  

    print("Starting Turkish")  

    for username in tr_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("TR Username: %s" % (parsed_username,))  

elif lang == "el":
    el_file = open("../dataset/admins/el_admins.txt", "r")  

    print("Starting Greek")  

    for username in el_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("EL Username: %s" % (parsed_username,))  

elif lang == "hi":
    hi_file = open("../dataset/admins/hi_admins.txt", "r")  

    print("Starting Hindi")  

    for username in hi_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("HI Username: %s" % (parsed_username,))  

elif lang == "bn":
    bn_file = open("../dataset/admins/bn_admins.txt", "r")  

    print("Starting Bengali")  

    for username in bn_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("BN Username: %s" % (parsed_username,))  

elif lang == "fa":
    fa_file = open("../dataset/admins/fa_admins.txt", "r")  

    print("Starting Persian")  

    for username in fa_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("FA Username: %s" % (parsed_username,))  

elif lang == "zh":
    zh_file = open("../dataset/admins/zh_admins.txt", "r")  

    print("Starting Chinese")  

    for username in zh_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("ZH Username: %s" % (parsed_username,))  

elif lang == "ja":
    zh_file = open("../dataset/admins/ja_admins.txt", "r")  

    print("Starting Japanese")  

    for username in zh_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("ZH Username: %s" % (parsed_username,))  

elif lang == "he":
    he_file = open("../dataset/admins/he_admins.txt", "r")  

    print("Starting Hebrew")  

    for username in he_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("HE Username: %s" % (parsed_username,))  

elif lang == "ur":
    ur_file = open("../dataset/admins/ur_admins.txt", "r")  

    print("Starting Urdu")  

    for username in ur_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("UR Username: %s" % (parsed_username,))  

elif lang == "ko":
    ko_file = open("../dataset/admins/ko_admins.txt", "r")  

    print("Starting Korean")  

    for username in ko_file:  
        parsed_username = username.replace("\n", " ")
        c.execute("Update User set user_admin=True where user_name=%s", (parsed_username,))
        print("KO Username: %s" % (parsed_username,))  

else:
    print("Insert valid language")

conn.commit()
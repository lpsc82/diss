# -*- coding: utf-8 -*-

from lxml import html, etree
import requests
import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics
import time
import sys
import logging

logging.basicConfig(filename='debug.log', level=logging.INFO)

first = True
cicle = 2000

def parseCategoryPage(pageName, lang):
    
    global first
    global cicle
    print("Category: " + pageName)
    logging.info("Category" + pageName)

    # get pages
    ### Categoria: titulo da página
    if lang =="en":
        catstring = "Category:"
    elif lang=="pt":
        catstring = "Categoria:"
    elif lang=="de":
        catstring = "Kategorie:"
    elif lang=="zh":
        catstring = "Category:"
    elif lang=="ca":
        catstring = "Categoria:"
    elif lang=="fr":
        catstring = "Catégorie:"
    elif lang=="bn":
        catstring = "বিষয়শ্রেণী:"
    elif lang=="ru":
        catstring = "Категория:"
    elif lang=="ur":
        catstring = "زمرہ:"
    elif lang=="ja":
        catstring = "Category:"
    elif lang=="tr":
        catstring = "Kategori:"
    elif lang=="ko":
        catstring = "분류:"
    elif lang=="it":
        catstring = "Template:"
    elif lang=="fa":
        catstring = "رده:الگو:"
    elif lang=="el":
        catstring = "Κατηγορία:"
    
    if first:
        page = requests.get("https://"+lang+".wikipedia.org/wiki/"+catstring+urllib.parse.quote(pageName))
    else:
        page = requests.get("https://"+lang+".wikipedia.org/wiki/"+urllib.parse.quote(pageName))

    tree = html.fromstring(page.content)

    templateElements = tree.xpath('//div[@id="mw-pages"]/descendant::a')

    pages = []

    for elem in templateElements:
        if elem.text is not None and ("Template:" in elem.text or "Predefinição:" in elem.text or "Vorlage:" in elem.text or "Plantilla:" in elem.text or
         "Modèle" in elem.text or "قالب:" in elem.text or "টেমপ্লেট:" in elem.text or "Шаблон:" in elem.text or "سانچہ:" in elem.text or "Şablon:" in elem.text or
         "틀:" in elem.text or "الگو:" in elem.text or  "Шаблон::" in elem.text or "תבנית:" in elem.text):         
            if lang == "en":
                pages.append(elem.text.replace("Template:",""))
            if lang == "pt":
                pages.append(elem.text.replace("Predefinição:",""))
            if lang == "de":                                        
                pages.append(elem.text.replace("Vorlage:",""))
            if lang == "zh":
                pages.append(elem.text.replace("Template:",""))
            if lang == "ca":                                        
                pages.append(elem.text.replace("Plantilla:",""))
            if lang == "fr":
                pages.append(elem.text.replace("Modèle:",""))
            if lang == "ar":                                        
                pages.append(elem.text.replace("قالب:",""))
            if lang == "bn":
                pages.append(elem.text.replace("টেমপ্লেট:",""))
            if lang == "ru":                                        
                pages.append(elem.text.replace("Шаблон:",""))
            if lang == "ur":
                pages.append(elem.text.replace("سانچہ:",""))
            if lang == "ja":
                pages.append(elem.text.replace("Template:",""))     
            if lang == "tr":                                        
                pages.append(elem.text.replace("Şablon:",""))
            if lang == "ko":
                pages.append(elem.text.replace("틀:",""))
            if lang == "it":
                pages.append(elem.text.replace("Template:",""))
            if lang == "fa":
                pages.append(elem.text.replace("الگو:",""))
            if lang == "el":                                        
                pages.append(elem.text.replace("Πρότυπο:",""))
            if lang == "he":                                        
                pages.append(elem.text.replace("תבנית:",""))           

    
    # get subcategories
    subcatElements = tree.xpath('//div[@id="mw-subcategories"]/descendant::a')

    for category in subcatElements:
        if category.text is not None:            
            print("SubCategoryText: " + category.text)
            if lang == "tr":
                first = False
                print ("NOT FIRST !!!")
            
            subpages = parseCategoryPage(category.text, lang)
                    
            pages = pages + subpages
            
    
    return pages

if len(sys.argv) > 1:    
    ilang = " ".join(sys.argv[1:])

    if ilang == "pt":
        with open("../dataset/pt_templates.txt", "w+") as file:
            templates = parseCategoryPage("!Predefinições_sobre_medicina","pt")
            file.writelines("\n".join(templates))
    elif ilang == "en":    
        with open("../dataset/en_templates.txt", "w+") as file:
            templates = parseCategoryPage("Medicine_templates","en")
            file.writelines("\n".join(templates))
    elif ilang == "de":   
        with open("../dataset/de_templates.txt", "w+") as file:
            templates = parseCategoryPage("Vorlage:Medizin","de")
            file.writelines("\n".join(templates))
    elif ilang == "zh":    
        with open("../dataset/zh_templates.txt", "w+") as file:
            templates = parseCategoryPage("医学模板","zh")
            file.writelines("\n".join(templates))
    elif ilang == "hi":    
        print ("Hindi doesn't have Medicine Templates!")
    elif ilang == "ca":    
        with open("../dataset/ca_templates.txt", "w+") as file:
            templates = parseCategoryPage("Plantilles_de_medicina","ca")
            file.writelines("\n".join(templates))
    elif ilang == "fr":    
        with open("../dataset/fr_templates.txt", "w+") as file:
            templates = parseCategoryPage("Modèle_médecine","fr")
            file.writelines("\n".join(templates))
    elif ilang == "ar":    
        with open("../dataset/ar_templates.txt", "w+") as file:
            templates = parseCategoryPage("تصنيف","ar")
            file.writelines("\n".join(templates))
    elif ilang == "bn":    
        with open("../dataset/bn_templates.txt", "w+") as file:
            templates = parseCategoryPage("চিকিৎসাবিদ্যা_টেমপ্লেট","bn")
            file.writelines("\n".join(templates))
    elif ilang == "ru":    
        with open("../dataset/ru_templates.txt", "w+") as file:
            templates = parseCategoryPage("Медицина","ru")
            file.writelines("\n".join(templates))
    elif ilang == "ur":    
        with open("../dataset/ur_templates.txt", "w+") as file:
            templates = parseCategoryPage("زمرہ","ur")
            file.writelines("\n".join(templates))
    elif ilang == "ja":    
        with open("../dataset/ja_templates.txt", "w+") as file:
            templates = parseCategoryPage("医学関連のテンプレート","ja")
            file.writelines("\n".join(templates))
    elif ilang == "tr":    
        with open("../dataset/tr_templates.txt", "w+") as file:
            templates = parseCategoryPage("Tıp_şablonları","tr")
            file.writelines("\n".join(templates))
    elif ilang == "ko":    
        with open("../dataset/ko_templates.txt", "w+") as file:
            templates = parseCategoryPage("의학에_관한_틀","ko")
            file.writelines("\n".join(templates))
    elif ilang == "it":    
        with open("../dataset/it_templates.txt", "w+") as file:
            templates = parseCategoryPage("Template_-_medicina","it")
            file.writelines("\n".join(templates))
    elif ilang == "fa":    
        with open("../dataset/fa_templates.txt", "w+") as file:
            templates = parseCategoryPage("پزشکی","fa")
            file.writelines("\n".join(templates))
    elif ilang == "el":
        with open("../dataset/el_templates.txt", "w+") as file:
            templates = parseCategoryPage("Ιατρικά_πρότυπα","el")
            file.writelines("\n".join(templates))
    elif ilang == "he":
        with open("../dataset/he_templates.txt", "w+") as file:
            templates = parseCategoryPage("תבניות_ניווט_-_רפואה","he")
            file.writelines("\n".join(templates))

    else:
        print ("Invalid language!")
else:
    print ("Select a language...")

# -*- coding: utf-8 -*-

import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import mwparserfromhell as mwp
import os
import textstat
import syllapy
from nltk.stem.snowball import SnowballStemmer
import snowballstemmer
import spacy
from spacy.lang.ar import Arabic
from spacy.lang.id import Indonesian
from spacy.lang.tr import Turkish
from spacy.lang.hi import Hindi
from spacy.lang.bn import Bengali
from spacy.lang.fa import Persian
from spacy.lang.he import Hebrew
from spacy.lang.ur import Urdu
from spacy.lang.ko import Korean
from bangla_stemmer.stemmer.stemmer import BanglaStemmer
from PersianStemmer import PersianStemmer
from konlpy.tag import Okt
from konlpy.utils import pprint
import ApiInterface as ai
import codecs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import sys

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle where ba_analyzed=True")
articles = c.fetchall()

if len(sys.argv) > 1:    
    lang = " ".join(sys.argv[1:])
    counter = 0

for article in articles:
    if article['ba_lang'] == lang:

        print(counter)
        counter = counter +1
        print("Analyzing %s in %s" % (article['ba_name'], article['ba_lang']))

        revisionQueryStr = ("https://"+article['ba_lang']+".wikipedia.org/w/api.php?action=query" +
            "&prop=revisions&redirects&titles=" +
            urllib.parse.quote(article['ba_name']) + 
            "&rvprop=ids%7Ctimestamp%7Cuser%7Ccomment%7Ccontent&formatversion=2&format=json&utf8")

        revision = ai.returnQueryJson(revisionQueryStr)

        content = revision["query"]["pages"][0]["revisions"][0]["content"]

        with codecs.open('../content/'+article['ba_name'].replace('/','_')+'_'+article['ba_lang']+'_wiki.dat', 'w', 'utf-8') as conFile:
            conFile.write(content)


        wikitext = mwp.parse(content)
        cleantext = wikitext.strip_code()
        articlename = article["ba_name"]
        destinationPath = "../content/"+articlename.replace('/','_')+"_"+article['ba_lang']+"_clean.dat"

        with open(destinationPath, "w") as output:
            output.write(cleantext)

        syl = textstat.syllable_count(cleantext)
        wrds = textstat.lexicon_count(cleantext, removepunct=True)
        stc = textstat.sentence_count(cleantext)

        if article['ba_lang'] == "en":
            textstat.set_lang("en")
            flesch = textstat.flesch_reading_ease(cleantext)
            kincaid = textstat.flesch_kincaid_grade(cleantext)
        
        elif article['ba_lang'] == "pt":
            textstat.set_lang("en")
            flesch = textstat.flesch_reading_ease(cleantext) + 42
            kincaid = -1
        
        elif article['ba_lang'] == "tr":
            flesch = 198.825-40.175*(syl/wrds)-2.610*(wrds/stc)#Atesman formula
            kincaid =-1
        
        elif article['ba_lang'] == "fr":
            textstat.set_lang("fr")
            flesch = textstat.flesch_reading_ease(cleantext)            
            kincaid = -1

        elif article['ba_lang'] == "de":
            textstat.set_lang("de")
            flesch = textstat.flesch_reading_ease(cleantext)
            kincaid = -1
        
        elif article['ba_lang'] == "it":
            textstat.set_lang("it")
            flesch = textstat.flesch_reading_ease(cleantext)
            kincaid = -1
        
        elif article['ba_lang'] == "ru":
            textstat.set_lang("ru")
            flesch = textstat.flesch_reading_ease(cleantext)
            kincaid = -1

        else:
            flesch = -1
            kincaid = -1
        articlelength = len(cleantext)

        stemmedStopped = []
        stopped = []
  

        if article['ba_lang'] == "en":
            nlp = spacy.load("en_core_web_sm")
            snow_stemmer = SnowballStemmer(language='english') 
        elif article['ba_lang'] == "pt":
            nlp = spacy.load("pt_core_news_sm")
            snow_stemmer = SnowballStemmer(language='portuguese')
        elif article['ba_lang'] == "fr":
            nlp = spacy.load("fr_core_news_sm")
            snow_stemmer = SnowballStemmer(language='french')
        elif article['ba_lang'] == "de":
            nlp = spacy.load("de_core_news_sm")
            snow_stemmer = SnowballStemmer(language='german')
        elif article['ba_lang'] == "it":
            nlp = spacy.load("it_core_news_sm")
            snow_stemmer = SnowballStemmer(language='italian')    
        elif article['ba_lang'] == "ca":
            nlp = spacy.load("es_core_news_sm")
            snow_stemmer = SnowballStemmer(language='spanish')
        elif article['ba_lang'] == "ru":
            nlp = spacy.load("ru_core_news_sm")
            snow_stemmer = SnowballStemmer(language='russian')
        elif article['ba_lang'] == "ar":
            nlp = Arabic()
            snow_stemmer = SnowballStemmer(language='arabic')
        elif article['ba_lang'] == "id":
            nlp = Indonesian()
            stemmer = snowballstemmer.stemmer('indonesian')
        elif article['ba_lang'] == "el":
            nlp = spacy.load("el_core_news_sm")
            stemmer = snowballstemmer.stemmer('greek')
        elif article['ba_lang'] == "tr":
            nlp = Turkish()
            stemmer = snowballstemmer.stemmer('turkish')
        elif article['ba_lang'] == "hi":
            nlp = Hindi()
            stemmer = snowballstemmer.stemmer('hindi')
        elif article['ba_lang'] == "bn":
            nlp = Bengali() #* bengla stemmer
        elif article['ba_lang'] == "fa": #* persian stemmer
            nlp = Persian()
        elif article['ba_lang'] == "zh":
            nlp = spacy.load("zh_core_web_sm")
            snow_stemmer = SnowballStemmer(language='arabic') 
        elif article['ba_lang'] == "ja":
            nlp = spacy.load("ja_core_news_sm")
            snow_stemmer = SnowballStemmer(language='russian') 
        elif article['ba_lang'] == "he":
            nlp = Hebrew()
            snow_stemmer = SnowballStemmer(language='arabic') 
        elif article['ba_lang'] == "ur":
            nlp = Urdu()
            snow_stemmer = SnowballStemmer(language='arabic') 
        elif article['ba_lang'] == "ko":
            nlp = spacy.load("xx_ent_wiki_sm")
            okt  = Okt() # konlpy
        
            
        else:
            print("ERROR: Language not found: " + article['ba_lang'] )
            print("Proceed?")
            input()

        doc = nlp(cleantext) 

        for token in doc: #token + stop => spacy
            if token.is_stop == False:
                stopped.append(token.text)

        if article['ba_lang'] in {"id", "el", "tr", "hi"}:
            print(article['ba_lang'])
            for w in stopped:
                stemmedStopped.append(stemmer.stemWords(w))

        elif article['ba_lang'] == "bn":
            for w in stopped:
                stemmedStopped.append(BanglaStemmer().stem(w))
        
        elif article['ba_lang'] == "fa":
            ps = PersianStemmer()
            for w in stopped:
                stemmedStopped.append(ps.run(w))
        
        elif article['ba_lang'] == "ko":
            for w in stopped:
                stemmedStopped.append(okt.morphs(w, norm=True, stem=True))
 
        else:
            for w in stopped:
                stemmedStopped.append(snow_stemmer.stem(w)) ### stem => snowball
        
        if article['ba_lang'] in {"xx"}:
            c.execute("Update BaseArticle set ba_flesch=%s, ba_kincaid=%s, ba_length=%s, ba_vectorsize=-1 where ba_id=%s",
                (flesch, kincaid, articlelength, article['ba_id']))
        
        else:
            c.execute("Update BaseArticle set ba_flesch=%s, ba_kincaid=%s, ba_length=%s, ba_vectorsize=%s where ba_id=%s",
                (flesch, kincaid, articlelength, len(stemmedStopped), article['ba_id']))
        conn.commit()
        print("Article %s of id %s reanalyzed" % (article['ba_name'], article['ba_id']))
        print("Flesch %s, kincaid %s, article length %s, stemmed size %s" % (flesch, kincaid, articlelength, len(stemmedStopped)))




        

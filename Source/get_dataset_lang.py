#!/usr/bin/python3

from lxml import html, etree
import requests
import urllib.request as http
import urllib
import json
import sys
import os
import time

en_titles = []
sec_titles = []

if len(sys.argv) != 2:
    sys.exit("Args error - insert language")

lang = " ".join(sys.argv[1:])

dataset = open("../dataset/datasets/2021-01-01-dataset.txt", "r")

i = 2
append_write = "w+"

destination = open("../dataset/dataset_" + lang + ".txt", append_write)

not_found = 0

for line in dataset:
    try:
        sline= line.strip()        
        title = sline
        en_titles.append(title)

        entitle = title

        #if language is english, just replicate titles
        if lang == "en":
            sectitle = title
        else:

            searchStr = "https://en.wikipedia.org/w/api.php?action=query&titles="+urllib.parse.quote(title)+"&prop=langlinks&lllimit=500&utf8&format=json"

            requestResult = http.urlopen(searchStr).read().decode("utf8")
            result = json.loads(requestResult, encoding="utf8")

            found = False
            if "langlinks" in next(iter(result["query"]["pages"].values())): 
                for link in next(iter(result["query"]["pages"].values()))["langlinks"]:

                    if link["lang"] == lang:
                        found = True
                        sec_titles.append(link["*"])
                        sectitle = link["*"]
            
            if not(found):
                sectitle = "Not Found"
                sec_titles.append("Not Found")
                not_found +=1
                #print(not_found)

        destination.write(entitle + "\t" + sectitle + "\n")
        print(i)

        #too many not founds -> lang arg error check
        if (i==6 and not_found == 5) or (i==11 and not_found == 10) or (i==21 and not_found == 20) :
            print ("CHECK LANG ERROR !!!")
            time.sleep(5)
                
        i += 1
    except:
        print("Stopped at : " + str(i))
        destination.close()
        sys.exit()

print("Not found: " + str(not_found))

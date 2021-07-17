# -*- coding: utf-8 -*-
 
import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle WHERE ba_analyzed = TRUE")
articles = c.fetchall()

def calculateVolatility(article):
    
    articleID = article['ba_id']

    ## Volatiliy

    # Median Revert Time (median revision distance times)

    c.execute("select rev_date, rev_id, rev_article, rev_comment, rev_tags, user_name, ba_lang from Revision, User, BaseArticle  where rev_article=%s and "+
        "rev_user = user_id and rev_article = ba_id order by rev_date desc", (articleID,))
    result = c.fetchall()

    reverts_blocks = {}
    revert_times = []
    revert_count=0

    for rev in result:      #TODO: Adicionar linguas
        #print(rev['ba_lang'])
        if rev['ba_lang'] in {"en", "fr"}:
            if "revert" in rev['rev_comment'].lower(): 
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]
        
        if rev['ba_lang'] in {"pt"}:
            if "revertidas" in rev['rev_comment'].lower(): 
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    try:
                        reverted_user = rev['rev_comment'].split("/")[1].split("|")[0]
                    except IndexError:
                        reverted_user = "null"
                    print(reverted_user)
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"de"}:
            if "rückgängig gemacht" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:

                    revert_count = revert_count +1
                    try:
                        reverted_user = rev['rev_comment'].split("rückgängig")[0].split("|")[1].split("]]")[0]
                    except IndexError:
                        reverted_user = "null"
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]
        
        if rev['ba_lang'] in {"ca"}:
            if "revertides" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"it"}:
            if "annull" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"ru"}:
            if "откат" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    try:
                        reverted_user = rev['rev_comment'].split("|")[1].split("]]")[1].split("/")[1]
                    except IndexError:
                        reverted_user = "null"
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]
        
        if rev['ba_lang'] in {"ar"}:
            if "استرجاع تعديلات" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]
        
        if rev['ba_lang'] in {"id"}:
            if "menolak" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"tr"}:
            if "geri al" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"el"}:
            if "αναστροφή" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"hi"}:
            if "reverted" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"bn"}:
            if "বাতিল" in rev['rev_comment'].lower():
                print('\n' + rev['rev_comment'])
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    print("User:: " + reverted_user)
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"fa"}:
            if "خنثی‌سازی " in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]
        
        if rev['ba_lang'] in {"zh"}:
            if "回退" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"ja"}:
            if "取り消し" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"he"}:
            if "שוחזר" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"ur"}:
            if ("ترمیم رد کر دی گئی ہے۔" in rev['rev_comment'].lower()):
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]

        if rev['ba_lang'] in {"ko"}:
            if "판 편집을 되돌림" in rev['rev_comment'].lower():
                if len(rev['rev_comment'].split("|")) > 1:
                    revert_count = revert_count +1
                    reverted_user = rev['rev_comment'].split("|")[1].split("]]")[0]
                    reverts_blocks[reverted_user] = datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                if rev['user_name'].lower() in reverts_blocks:
                    revert_times.append(int((reverts_blocks[rev['user_name'].lower()] - datetime.strptime(rev['rev_date'], "%Y-%m-%dT%H:%M:%SZ")).seconds/60))
                    del reverts_blocks[rev['user_name'].lower()]                 
        

    if len(reverts_blocks) > 0:
        print("Article " + article['ba_name'])
        print("Skipped " + str(len(reverts_blocks)) + " reverts")
        print("Out of " + str(revert_count))

    if len(revert_times) >= 1:
        return statistics.median(revert_times)
    else:
        return 0

csv_output_metrics = open("../results/volatility.csv", "w+")
csv_writer_metrics = None

metrics = []

first=True

counter = 0

for article in articles:

    print(counter)
    print (article['ba_lang'])
        
    counter = counter +1

    if counter in {}:
        continue

    volatility = calculateVolatility(article)

    temp_metric = {}

    temp_metric['volatility'] = volatility
    
    temp_metric['id'] = article['ba_id']
    temp_metric['lang'] = article['ba_lang']
    temp_metric['name'] = article['ba_name']

    metrics.append(temp_metric)

    if first:
        csv_writer_metrics = csv.DictWriter(csv_output_metrics, fieldnames=temp_metric.keys())
        csv_writer_metrics.writeheader()
        first=False

    csv_writer_metrics.writerow(temp_metric)





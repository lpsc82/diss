# -*- coding: utf-8 -*-
 
import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics
import sys

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle WHERE ba_analyzed = TRUE")
articles = c.fetchall()

counter = 0

if len(sys.argv) > 1:    
    counter = int(sys.argv[1])

def calculateIntermediateMetrics(article):
    print("Start analyzing article %s" % article['ba_name'])
    intermediate_metrics = {}

    articleID = article['ba_id']

    currDate = datetime.now()

    ## Authority ##

    # Number of unique editors
    
    c.execute(("select count(distinct rev_user) as res from Revision"
        " where rev_article = %s group by rev_article"),
        (articleID, ))
    result = c.fetchone()
    intermediate_metrics['numUniqueEditors'] = result['res']

    # Total number of edits

    c.execute(("Select count(rev_id) as res from Revision where rev_article = %s"),
        (articleID, ))
    result = c.fetchone()
    intermediate_metrics['numEdits'] = result['res']

    # Connectivity 
    
    c.execute(("select count(*) as res from (select rev_article, count(rev_article), "
        "ba_name from (select rev_user as user from Revision where rev_article=%s"
        " group by rev_user) as revusers, Revision, BaseArticle where "
        "Revision.rev_user=revusers.user and ba_id=rev_article group by rev_article) as finaltable"),
        (articleID, ))
    result = c.fetchone()
    intermediate_metrics['connectivity'] = result['res']

    # Number of edits by anonymous users edits

    c.execute(("select count(rev_id) as res from User, Revision where"
        " rev_user = user_id and user_anonymous = TRUE and rev_article = %s"),
        (articleID, ))
    result = c.fetchone()
    intermediate_metrics['numAnonEdits'] = result['res']

    # Number of registered user edits
    
    c.execute(("select count(rev_id) as res from User, Revision where"
        " rev_user = user_id and user_anonymous = FALSE and rev_article = %s"),
        (articleID, ))
    result = c.fetchone()
    intermediate_metrics['numRegisteredEdits'] = result['res']

    # Number of external links

    c.execute(("select count(ol_url) as res from OuterLinksTo "
        "where ol_origin = %s"),
        (articleID,))
    result = c.fetchone()
    intermediate_metrics['numExternalLinks'] = result['res']

    # Number of reverts
  
    c.execute(("select count(rev_id) as res from Revision where rev_article = %s" ###TODO
        " and (rev_comment LIKE \"%Révocation%\" OR rev_comment LIKE \"%Revert%\" OR rev_comment LIKE \"%Revers%\" OR rev_comment LIKE \"%Rückgängig gemacht%\" " 
        " OR rev_comment LIKE \"%Revertides%\" OR rev_comment LIKE \"%Annull%\" OR rev_comment LIKE \"%откат%\" OR rev_comment LIKE \"%استرجاع تعديلات%\" OR rev_comment LIKE \"%Menolak%\" "
        " OR rev_comment LIKE \"%Geri al%\" OR rev_comment LIKE \"%αναστροφή%\" OR rev_comment LIKE \"%বাতিল%\" OR rev_comment LIKE \"%دستی%\" OR rev_comment LIKE \"%خنثی‌سازی%\" "
        " OR rev_comment LIKE \"%回退%\" OR rev_comment LIKE \"% 取り消し%\" OR rev_comment LIKE \"%שוחזר%\" OR rev_comment LIKE \"%ترمیم رد کر دی گئی ہے۔%\" OR rev_comment LIKE \"%판 편집을 되돌림%\"  )"), 
        (articleID,))
    result = c.fetchone()
    intermediate_metrics['numReverts'] = result['res']

    ## Completeness ##

    # Number of internal broken links

    c.execute(("select count(il_destination) as res from InnerLinksTo, BaseArticle "
        "where il_origin = %s and ba_id=il_destination and ba_broken=True"),
        (articleID,))
    result = c.fetchone()
    intermediate_metrics['numBrokenLinks'] = result['res']

    # Number of internal links

    c.execute(("select count(il_destination) as res from InnerLinksTo "
        "where il_origin = %s"),
        (articleID,))
    result = c.fetchone()
    intermediate_metrics['numInnerLinks'] = result['res']

    # Article Length (character count)
    intermediate_metrics['articleLength'] = article['ba_length']
    

    ## Complexity

    # Flesch readability score    
    intermediate_metrics['flesch'] = article['ba_flesch']

    # Kincaid readability score
    intermediate_metrics['kincaid'] = article['ba_kincaid']

    ## Informativeness

    # Infonoise

    intermediate_metrics['infoNoise'] = 1 - (article['ba_vectorsize'] / article['ba_length'])

    # Diversity (unique editors/total edits)

    intermediate_metrics['diversity'] = intermediate_metrics['numUniqueEditors'] / intermediate_metrics['numEdits']

    # Number of images

    c.execute("select count(media_id) as res from Media where media_article = %s",
        (articleID,))
    result = c.fetchone()
    intermediate_metrics['numMedia'] = result['res']

    ## Consistency

    # Admin edit share

    c.execute("select count(*) as res from User, Revision where rev_article=%s and "+
        "rev_user=user_id and user_admin=True",
        (articleID,))
    result = c.fetchone()
    adminRevs = result['res']

    intermediate_metrics['adminShare'] = (adminRevs/intermediate_metrics['numEdits'])

    # Age (in days)

    #data da ultima edição
    c.execute(("select rev_date as res from Revision where rev_article = %s "
        "order by rev_date limit 1 offset 0"), 
        (articleID,))
    result = c.fetchone()
    firstRevDate = datetime.strptime(result['res'], "%Y-%m-%dT%H:%M:%SZ")
    delta = currDate - firstRevDate
    age = delta.days
    intermediate_metrics['age'] = age

    ## Currency

    # currency

    c.execute(("select rev_date as res from Revision where rev_article = %s "
        "order by rev_date desc limit 1 offset 0"),
        (articleID,))
    result = c.fetchone()
    lastRevDate = datetime.strptime(result['res'], "%Y-%m-%dT%H:%M:%SZ")
    delta = currDate - lastRevDate
    currency = delta.days
    intermediate_metrics['currency'] = currency

    ## Volatiliy

    # Median Revert Time (median revision distance times) ### -> VolatilityCalc script

    c.execute("select rev_date as res from Revision where rev_article=%s and "+
        "rev_comment like \"%Revert%\" or rev_comment like \"%Révocation%\" or rev_comment like \"%Rückgängig gemacht%\" or rev_comment like \"%Revertides%\" OR rev_comment LIKE \"%Annull%\" OR rev_comment LIKE \"%откат%\" "
        "OR rev_comment LIKE \"%استرجاع تعديلات%\" OR rev_comment LIKE \"%Menolak%\" OR rev_comment LIKE \"%Geri döndü%\" OR rev_comment LIKE \"%Αναιρέθηκε%\" OR rev_comment LIKE \"%ট্যাগ: পূর্বাবস্থায় ফেরত%\" "
        "OR rev_comment LIKE \"%دستی%\" OR rev_comment LIKE \"%خنثی‌سازی%\" OR rev_comment LIKE \"%已回退%\" OR rev_comment LIKE \"% 取り消し%\" OR rev_comment LIKE \"%שוחזר%\" OR rev_comment LIKE \"%ترمیم رد کر دی گئی ہے۔%\"   order by rev_date desc", (articleID,)) 
    result = c.fetchall()
    if len(result) >= 2:
        revertTimes = [(datetime.strptime(i['res'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(j['res'], "%Y-%m-%dT%H:%M:%SZ")).days
            for i, j in zip(result[:-1], result[1:])]
        intermediate_metrics['medianRevertTime'] = statistics.median(revertTimes)
    else:
    intermediate_metrics['medianRevertTime'] = 0

    return intermediate_metrics
    

def authority(numUniqueEditors, numEdits, connectivity, numReverts, numExternalLinks, numRegisteredEdits, numAnonEdits):
    
    authority = 0.2*numUniqueEditors+0.2*numEdits+0.1*connectivity+0.3*numReverts+0.2*numExternalLinks+0.1*numRegisteredEdits+0.2*numAnonEdits
    
    return authority
    # CALCULATE AUTHORITY
    # get number of unique editors: done
    # get total number of reviews: done
    # get connectivity -> find every article reviewed by a user (impossible without dumps) started, not finished
    # get num of anonymous user edits: done
    # get num of registered user edits: done
    # get num of external links: database needs refill (currently empty) otherwise done
    # get num of reverts (check every revision comment for the word Revert): done


def completeness(numBrokenLinks, numInnerLinks, articleLength):
    completeness = 0.4*numBrokenLinks+0.4*numInnerLinks+0.2*articleLength
    return completeness

    # CALCULATE COMPLETENESS
    # Num of Internal Broken Links (maybe get every page, if no result then it's broken?): recheck implementation
    # Num Internal Links: done
    # Article Length: post processing -> retreive character count (only have wordcount so far)
    
# READABILITY SCORE
def readability(flesch, kincaid):
    readability = 0.5 * flesch - 0.5 * kincaid
    return readability


# CALCULATE INFORMATIVENESS
def informativeness(infoNoise, diversity, numMedia):
    informativeness = 0.6*infoNoise-0.6*diversity+0.3*numMedia
    return informativeness

# get ratio between number of preprocessed tokens and total characters (possible?)
# get num of unique editors/num edits: done
# get num of media: done

# CALCULATE COnsistency
def consistency(adminShare, age):
    consistency = 0.6*adminShare+0.5*age
    return consistency

# get admin edit share (only possible if i retrieve admins first and compare lists)
# get article age (first review) in days: done

# CALCULATE CURRENCY
def currency(currency):    
    return currency

# get time difference between 00:00 28/1/18 and the last review

# CALCULATE VOLATILITY

def volatility(volatility):
    return volatility
    

csv_output_metrics = open("../results/iq_metrics.csv", "w+")
csv_writer_metrics = None

csv_output_measurements = open("../results/iq_measurements.csv", "w+")
csv_writer_measurements = None

metrics = []

first=True

for article in articles[counter:]:
    print (">>Counter: ", counter)
    print(len(articles)-counter)
    counter = counter + 1

    intermediate_metrics = calculateIntermediateMetrics(article)

    temp_metric = {}

    temp_metric['authority'] = authority(intermediate_metrics['numUniqueEditors'],
        intermediate_metrics['numEdits'], intermediate_metrics['connectivity'],
        intermediate_metrics['numReverts'], intermediate_metrics['numExternalLinks'],
        intermediate_metrics['numRegisteredEdits'], intermediate_metrics['numAnonEdits'])

    temp_metric['completeness'] = completeness(intermediate_metrics['numBrokenLinks'],
        intermediate_metrics['numInnerLinks'], intermediate_metrics['articleLength'])

    temp_metric['complexity'] = readability(intermediate_metrics['flesch'],
        intermediate_metrics['kincaid'])

    temp_metric['informativeness'] = informativeness(intermediate_metrics['infoNoise'],
        intermediate_metrics['diversity'], intermediate_metrics['numMedia'])

    temp_metric['consistency'] = consistency(intermediate_metrics['adminShare'],
        intermediate_metrics['age'])

    temp_metric['currency'] = intermediate_metrics['currency']

    temp_metric['volatility'] = intermediate_metrics['medianRevertTime']
    
    temp_metric['id'] = article['ba_id']
    temp_metric['lang'] = article['ba_lang']
    temp_metric['name'] = article['ba_name']
    intermediate_metrics['id'] = article['ba_id']
    intermediate_metrics['lang'] = article['ba_lang']
    intermediate_metrics['name'] = article['ba_name']

    metrics.append(temp_metric)

    if first:
        csv_writer_metrics = csv.DictWriter(csv_output_metrics, fieldnames=temp_metric.keys())
        csv_writer_metrics.writeheader()
        csv_writer_measurements = csv.DictWriter(csv_output_measurements, fieldnames=intermediate_metrics.keys())
        csv_writer_measurements.writeheader()
        first=False

    print(str(temp_metric))
    csv_writer_metrics.writerow(temp_metric)
    csv_writer_measurements.writerow(intermediate_metrics)






import mysql.connector
import urllib.request as http
import urllib
import json
from html.parser import HTMLParser
import csv
from datetime import datetime
import statistics
from mwtemplates import TemplateEditor

DB_NAME = "dados"
conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
c = conn.cursor(dictionary=True)

c.execute("SELECT * FROM BaseArticle WHERE ba_analyzed = TRUE")
articles = c.fetchall()

csv_output_measurements = open("../results/medicine_metrics.csv", "w+")
csv_writer_measurements = None

first = True

measurements = []

for article in articles:
    article_measurements = {}

    print(article['ba_name'] + " : " + str(article['ba_id']))

#Informativeness

    # Number infobox
    c.execute("SELECT count(distinct infopair_info) as res from InfoboxPair WHERE infopair_article=%s", (article['ba_id'],))
    article_measurements['numInfobox'] = c.fetchone()['res']

    ## nº values
    c.execute("SELECT count(distinct infopair_value) as res from InfoboxPair WHERE infopair_article=%s and infopair_value != ''", (article['ba_id'],))
    article_measurements['InfoboxValues'] = c.fetchone()['res']

    ## nº images
    c.execute("SELECT count(distinct infopair_value) as res from InfoboxPair WHERE infopair_article=%s and infopair_value != '' and infopair_key = 'image'", (article['ba_id'],))
    article_measurements['InfoboxImages'] = c.fetchone()['res']

    # nº Medicine Templates
    c.execute("SELECT count(medba_id) as res from MedicineTemplateArticle where medba_article=%s", (article['ba_id'],))
    article_measurements['numTemplates'] = c.fetchone()['res']
    
    # Number infobox
    c.execute("SELECT count(distinct infopair_info) as res from InfoboxPair WHERE infopair_article=%s", (article['ba_id'],))
    article_measurements['numInfobox'] = c.fetchone()['res']

# Authority
    
    # Number of WP admins edits
    c.execute("select count(rev_id) as res from User, Revision where rev_user = user_id and user_wp = TRUE and rev_article = %s" ,(article['ba_id'],))
    article_measurements['numWpEdits'] = c.fetchone()['res']

    # TaskForce Translated
    c.execute("select count(ba_translated) as res from BaseArticle WHERE ba_translated = TRUE and ba_id = %s" ,(article['ba_id'],))
    article_measurements['translated'] = c.fetchone()['res']

    # nº Codifications (infobox/templates) https://en.wikipedia.org/wiki/Template:Medical_resources
    c.execute("select count(distinct(temp_key)) as res from Template WHERE temp_article = %s" ,(article['ba_id'],))
    article_measurements['codes'] = c.fetchone()['res']

    # nº Reputated External Links https://www.nlm.nih.gov/portals/researchers.html https://www.nlm.nih.gov/services/databases_subject.html
    c.execute("select count(ol_url) as res from OuterLinksTo WHERE ol_reputated = TRUE and ol_origin = %s" ,(article['ba_id'],))
    article_measurements['repLinks'] = c.fetchone()['res']

#Completeness

    # nº Recommended sections  https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Medicine-related_articles#Content_sections
    c.execute("select count(sec_id) as res from Section where sec_recommended = TRUE and sec_article = %s" ,(article['ba_id'],))
    article_measurements['numRecSections'] = c.fetchone()['res']


    article_measurements['id'] = article['ba_id']
 
    article_measurements['name'] = article['ba_name']

    if first:
        csv_writer_measurements = csv.DictWriter(csv_output_measurements, fieldnames=article_measurements.keys())
        csv_writer_measurements.writeheader()
        first=False

    print(str(article_measurements))
    csv_writer_measurements.writerow(article_measurements)
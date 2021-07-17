# -*- coding: utf-8 -*-

import urllib.request as http
import urllib
import json
import mwparserfromhell as mw
import re
import DatabaseInterface as di
from mwtemplates import TemplateEditor
from html.parser import HTMLParser
from textstat.textstat import textstat
import logging
import codecs
import time

logger = logging.getLogger("mainlogger")

database = di.DataInterface()

def returnQueryJson(url):
    requestResult = http.urlopen(url).read().decode("utf8")
    result = json.loads(requestResult, encoding="utf8")
    return result
       
def processQuery(query, wordcount, lang):
    article = database.getArticle(query)
    logger.info(u'Analyzing %s' % (query, ))
    print("Analyzing " + query)
    if article != None and article['ba_analyzed'] == True and article['ba_lang'] == lang:
        logger.info('Already analyzed')
        return article['ba_id']
    
    #conteudo em wikitext - para usar bibliotecas
    revisionQueryStr = ("https://"+lang+".wikipedia.org/w/api.php?action=query" +
               "&prop=revisions&redirects&titles=" +
                urllib.parse.quote(query) + 
                "&rvprop=ids%7Ctimestamp%7Cuser%7Ccomment%7Ccontent%7Ctags&formatversion=2&format=json&utf8")
    #info toda
    parsedQueryStr = ("https://"+lang+".wikipedia.org/w/api.php?action=parse" +
                "&utf8&formatversion=2&redirects&format=json&page=" +
                urllib.parse.quote(query))

    #lista de revisoes        
    revisionListQueryStr = ("https://"+lang+".wikipedia.org/w/api.php?action=query&utf8&redirects&prop=revisions&titles=" +
                urllib.parse.quote(query) +
                "&rvprop=flags|timestamp|user|userid|comment|size|tags&formatversion=2&rvlimit=500&format=json")

    revision = returnQueryJson(revisionQueryStr)
    parsed = returnQueryJson(parsedQueryStr)

    tempRevisions = returnQueryJson(revisionListQueryStr)
    revisionList = tempRevisions
    #loop continue: encontrar todas as revisoes que tenham mais de 500 resultados (continua na pagina seguinte)
    while "continue" in tempRevisions:
        continueCode = tempRevisions['continue']['rvcontinue']
        tempRevisions = returnQueryJson(revisionListQueryStr+"&rvcontinue="+
            tempRevisions['continue']['rvcontinue'])
        revisionList['query']['pages'][0]['revisions'].extend(tempRevisions['query']['pages'][0]['revisions'])

    plainText = stripTags(parsed["parse"]["text"])

    pageTitle = parsed["parse"]["title"]

    #escreve o conteudo num ficheiro .dat
    with codecs.open('../content/'+pageTitle.replace('/','_')+'_wiki.dat', 'w', 'utf-8') as conFile:
        conFile.write(revision["query"]["pages"][0]["revisions"][0]["content"])

    # Insert Article
    wikitextPath = "../content/" + pageTitle
    wikibaseItem = None
    if "wikibase_item" in parsed["parse"]["properties"]:
        wikibaseItem = parsed["parse"]["properties"]["wikibase_item"]
    articleID = database.updateArticle(name=pageTitle, lang=lang, contentPath=wikitextPath, wikiID=wikibaseItem
        , wordCount=wordcount, readability=textstat.flesch_reading_ease(plainText))

    # Insert Links
    for links in parsed['parse']['links']:
        if 'exists' in links:
            exists = True
        else:
            exists = False
        linkedArticle = database.insertArticle(links['title'], exists, lang)
        database.insertInnerLink(articleID, linkedArticle)

    # Insert Sections
    for section in parsed['parse']['sections']:
        database.insertSection(name=section['line'], article=articleID, level=section['level'],
            secNumber=section['number'], index=section['index'])

    # Insert External Links
    for extLink in parsed['parse']['externallinks']:
        database.insertOuterLinksTo(articleID, extLink)

    # Insert Languages
    for language in parsed['parse']['langlinks']:
        languageID = database.getLanguageID(language['lang'], language['langname'])
        database.insertTranslatedIn(articleID, languageID, language['title'])

    # Process media
    for image in parsed['parse']['images']:
        extension = image.split('.')[-1]
        type = getExtensionType(extension)
        typeID = database.getMediaTypeID(type)
        database.insertMedia(articleID, image, typeID)

    # Insert revision data
    for item in revisionList['query']['pages'][0]['revisions']:
        try:
            username = item['user']
        except KeyError:
            username = "hidden"
        user = database.getUser(username)
        if user is None:
            user = database.insertUser(username, ("anon" in item))
        minorChange = ("minor" in item)
        try:
            comment = item['comment']
        except KeyError:
            comment = ""
        database.insertRevision(articleID, user, item['timestamp'],
            minorChange, comment, item['size'], comment.join(item['tags']))

    return articleID

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def stripTags(text):
        s = MLStripper()
        s.feed(text)
        strippedText = s.get_data()
        strippedText = re.sub(r'(\n)+', '\n', strippedText)
        return strippedText

def getExtensionType(ext):
    try:
        return {
            'svg': 'image',
            'jpg': 'image',
            'png': 'image',
            'jpeg': 'image',
            'gif': 'image',
            'webm': 'video',
            'mp4': 'video',
            'mpeg4': 'video',
            'avi': 'video',
            'ogg': 'audio',
            'mp3': 'audio',
            'flac': 'audio',
            'mid': 'audio'
        }[ext.lower()]
    except KeyError:
        return 'image' 


def resolveRedirects(query, lang):
    resolverStr = ("https://"+lang+".wikipedia.org/w/api.php?action=query&titles="
        + urllib.parse.quote(query) + "&redirects&utf8&formatversion=2&format=json")
    resolverResult = returnQueryJson(resolverStr)

    result = query
    if 'redirects' in resolverResult['query']:
        result = resolverResult['query']['redirects'][0]['to']
    return result

def sectionHierarchy():
    sectionList = database.getAllSections()
    for section in sectionList:
        secNumber = section['sec_number']
        article = section['sec_article']
        logger.info(u'Updating section %s of article %s' % (secNumber, article))
        splitNum = secNumber.split('.')
        if len(splitNum) == 1:
            continue
        parentSecNumber = '.'.join(splitNum[:-1])
        parentSectionID = database.getSectionID(article, parentSecNumber)
        database.updateSectionParent(section['sec_id'], parentSectionID) 


def processTemplates(article, text):
    te = TemplateEditor(text)
    logger.info(u'Extract templates from article %s' % article)

    for (key, value) in te.templates.items(): #Devolve pares do template key (CID) / value (valor)
        if(key == "CID11" or key == "ICD11"):
            #store cid11
            for temp in value:
                database.insertTemplate(key, str(temp.parameters[1]), article)        
        if(key == "CID10" or key == "ICD10"):
            #store cid10
            for temp in value:
                if(len(temp.parameters) > 2):
                    val = str(temp.parameters[1]) + str(temp.parameters[2])
                    if temp.parameters[3] != "":
                        val += "." + str(temp.parameters[3])
                else:
                    val = str(temp.parameters[1])
                database.insertTemplate(key, val, article)
        if(key == "CID9" or key == "ICD9"):
            #store cid9
            for temp in value:
                database.insertTemplate(key, str(temp.parameters[1]), article)
        if(key == "EMedicine2" or key == "EMedicine"):
            #store emedicine2
            for temp in value:
                database.insertTemplate("eMedicine", str(temp.parameters[1]) + "/" + str(temp.parameters[2]), article)
        if(key == "CIDO" or key == "ICDO"):
            for temp in value:
                database.insertTemplate(key, str(temp.parameters[1]) + "/" + str(temp.parameters[2]), article)
        if(key == "OMIM2" or key == "DiseasesDB2" or key == "MedlinePlus2"):
            for temp in value:
                database.insertTemplate(key, str(temp.parameters[1])[:-1], article)


        #parse infobox
        #https://en.wikipedia.org/wiki/Category:Medicine_external_link_templates
        if(key == "Info/Patologia" or key == "Medical resources" or
            key == "Infobox medical condition" or key == "Medical condition classification and resources"):
            temp = value[0].parameters
            if "eMedicine" in temp:
                val = temp["eMedicine"]
                if val != "":
                    database.insertTemplate("eMedicine", val, article)
            if "MeshID" in temp:
                val = temp["MeshID"]
                if val != "":
                    database.insertTemplate("MeshID", val, article)
            if "MedlinePlus" in temp:
                val = temp["MedlinePlus"]
                if val != "":
                    database.insertTemplate("MedlinePlus", val, article)
            if "DiseasesDB" in temp:
                val = temp["DiseasesDB"]
                if val != "":
                    database.insertTemplate("DiseasesDB", val, article)
            if "OMIM" in temp:
                val = temp["OMIM"]
                if val != "":
                    database.insertTemplate("OMIM", val, article)
            if "eMedicineSubj" in temp and "eMedicineTopic" in temp:
                val1 = temp["eMedicineSubj"]
                val2 = temp["eMedicineTopic"]
                if val1 != "" and val2 != "":
                    database.insertTemplate("eMedicine", str(val1) + "/" + str(val2), article)
            if "MeSH" in temp:
                val = temp["MeSH"]
                if val != "":
                    database.insertTemplate("MeSH", val, article)
            for i in range(1,10):
                if ("MeSH" + str(i)) in temp:
                    val = temp[("MeSH" + str(i))]
                    if val != "":
                        database.insertTemplate(("MeSH"+str(i)), val, article)
                else:
                    break
                            
#resolve redirects (para nomes parecidos - funcionalidade da wikipédia)
def getSearchResults(query, lang):
    searchStr = ("https://"+lang+".wikipedia.org/w/api.php?action=query&srwhat=nearmatch&list=search&srsearch="
        + urllib.parse.quote(query) + "&utf8=&formatversion=2&format=json")
    searchResult = returnQueryJson(searchStr)

    resultList = []
    for item in searchResult['query']['search']:
        resultList.append([item['title'], item['wordcount']])

    if not resultList:
        return None
    result = resultList[0]
    newQuery = resolveRedirects(result[0], lang)

    if newQuery != query:
        result = getSearchResults(newQuery, lang)

    return result

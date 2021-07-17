# -*- coding: utf-8 -*-

import mysql.connector
import urllib.request as http
import logging
import time

logger = logging.getLogger("mainlogger")

class SharedData:
    def __init__(self):
        DB_NAME = "dados"
        self.conn = mysql.connector.connect(user='root', password='root', host='localhost', database=DB_NAME, collation='utf8mb4_general_ci', auth_plugin='mysql_native_password')
        self.c = self.conn.cursor(dictionary=True)

class DataInterface:
    shared = None
    def __init__(self):
        if not DataInterface.shared:
            DataInterface.shared = SharedData()

    def getArticleID(self, name, lang):
        self.shared.c.execute("SELECT * FROM BaseArticle WHERE " +
            "ba_name = %s AND ba_lang = %s", (name, lang))
        results = self.shared.c.fetchall()
        if not results:
            logger.info('Article %s not found' % (name,))
            return None
        logger.info('Article %s found' % (name,))
        return results[0]['ba_id']

    def getArticle(self, name):
        self.shared.c.execute("SELECT * FROM BaseArticle WHERE " +
            "ba_name = %s and ba_analyzed = 1", (name,))
        results = self.shared.c.fetchall()
        if not results:
            logger.info('Article %s not found' % (name,))
            return None
        logger.info('Article %s found' % (name,))
        return results[0]

    def getSectionID(self, article, secNum):
        self.shared.c.execute("SELECT * FROM Section WHERE sec_article = %s AND sec_number = %s",
            (article, secNum))
        results = self.shared.c.fetchall()
        if not results:
            logger.info('Section %s not found %s' % (article, secNum))
            return None
        logger.info('Section %s found %s' % (article, secNum))
        return results[0]['sec_id']

    def getAllSections(self):
        self.shared.c.execute("SELECT * FROM Section")
        results = self.shared.c.fetchall()
        return results

    def updateSectionParent(self, id, parentID):
        self.shared.c.execute("UPDATE Section SET sec_parent = %s WHERE sec_id = %s",
            (parentID, id))
        self.shared.conn.commit()

    def insertLanguage(self, lang, name):
        self.shared.c.execute("INSERT IGNORE INTO Language " +
            "(lang_code, lang_name) VALUES (%s, %s)", (lang, name))
        self.shared.conn.commit()

    def insertTranslatedIn(self, articleID, langID, name):
        self.shared.c.execute("INSERT IGNORE INTO TranslatedIn "+
            "(ti_article, ti_language, ti_name) VALUES (%s, %s, %s)", (articleID, langID, name))
        self.shared.conn.commit()

    def getLanguageID(self, lang, name):
        self.shared.c.execute("SELECT * FROM Language WHERE " +
            "lang_code = %s", (lang,))
        results = self.shared.c.fetchall()
        if not results:
            logger.info('Language %s not found' % (lang,))
            self.insertLanguage(lang, name)
            self.shared.c.execute("SELECT * FROM Language WHERE " +
                "lang_code = %s", (lang,))
            results = self.shared.c.fetchall()
        logger.info('Language %s found' % (lang,))
        return results[0]['lang_id']

    def getTranlsatedIn(self, articleID, langID):
        self.shared.c.execute("SELECT * FROM TranslatedIn WHERE ti_article = %s AND ti_language = %s",
            (articleID, langID))
        results = self.shared.c.fetchall()
        return (not (not results))

    def insertInnerLink(self, originID, destinationID):
        self.shared.c.execute("INSERT IGNORE INTO InnerLinksTo " +
            "(il_origin, il_destination) VALUES (%s, %s)", (originID, destinationID))
        self.shared.conn.commit()

    def updateArticle(self, name, lang, contentPath=None, healthRelated=True, wikiID=None, wordCount=None, readability=None):
        articleID = self.insertArticle(name, True, lang)
        
        self.shared.c.execute("UPDATE BaseArticle SET " +
            "ba_contentPath = %s, ba_wikiID = %s, ba_wordCount = %s" +
            ", ba_flesch = %s, ba_analyzed = 1 WHERE ba_id = %s",
            (contentPath, wikiID, wordCount,
            readability, articleID))
        self.shared.conn.commit()
        return articleID

    def insertArticle(self, name, exists, lang):
        id = self.getArticleID(name, lang)
        if id is None:
            self.shared.c.execute("INSERT IGNORE INTO BaseArticle " +
                "(ba_name, ba_analyzed, ba_lang) VALUES (%s, 0, %s)", (name, lang))
            self.shared.conn.commit()
            id = self.getArticleID(name, lang)
        return id

    def insertSection(self, name, article, parentSection=None, numberOfTables=None, level=None, secNumber=None, index=None):
        self.shared.c.execute("INSERT IGNORE INTO Section (sec_name, sec_article, sec_parent, sec_numberOfTables, sec_level, sec_number, sec_index)"+
            "VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, article, parentSection, numberOfTables, level, secNumber, index))
        self.shared.conn.commit()

    def insertOuterLinksTo(self, origin, url):
        self.shared.c.execute("INSERT IGNORE INTO OuterLinksTo (ol_origin, ol_url) " +
            "VALUES (%s, %s)", (origin, url))
        self.shared.conn.commit()

    def getOuterLinksTo(self, origin, destination):
        self.shared.c.execute("SELECT * FROM OuterLinksTo WHERE ol_origin = %s AND ol_destination = %s",
            (origin, destination))
        results = self.shared.c.fetchall()
        return (not (not results))
        
    def conceptExists(self, concept):
        self.shared.c.execute("SELECT * from Concept, BaseArticle WHERE concept_en = ba_id AND ba_name = %s",
            (concept,))
        results = self.shared.c.fetchall()
        return (not (not results))

    def insertConcept(self, concept_en, date):
        self.shared.c.execute("INSERT INTO Concept (concept_en, concept_date)"
            + " VALUES (%s, %s)", (concept_en, date))
        self.shared.conn.commit()

    def updateConcept(self, en_id, concept_lang, lang_id):
        print ("UPDATE Concept SET %s = %s WHERE concept_en = %s" % (concept_lang, lang_id, en_id))
        self.shared.c.execute("UPDATE Concept SET concept_pt=%s WHERE concept_en=%s", (lang_id, en_id))
        self.shared.conn.commit()
        
    def getConceptId(self, en_id):
        self.shared.c.execute("SELECT * FROM Concept WHERE concept_en = %s",
            (en_id,))
        result = self.shared.c.fetchall()
        if not result:
            return None
        else:
            return result[0]['concept_id']
    
    def getEnId(self, term):
        self.shared.c.execute("SELECT * FROM BaseArticle WHERE ba_name = %s",
            (term,))
        result = self.shared.c.fetchall()
        return result[0]['ba_id']

    def getUser(self, name):
        logger.warn('Looking for user %s' % (name,))
        self.shared.c.execute("SELECT * FROM User WHERE user_name = %s",
            (name,))
        result = self.shared.c.fetchall()
        if not result:
            logger.warn('User not found')
            return None
        else:
            logger.info('User found')
            return result[0]['user_id']

    def insertUser(self, name, anonymous):
        logger.info('Inserting user %s' % (name,))
        self.shared.c.execute("INSERT INTO User (user_name, user_anonymous) VALUES " +
            "(%s, %s)", (name, int(anonymous)))
        self.shared.conn.commit()
        return self.shared.c.lastrowid

    def insertRevision(self, article, user, revDate, minor, comment, size, tags):
        logger.info('Inserting revision for article %s' % (article,))
        self.shared.c.execute("INSERT INTO Revision (rev_article, rev_user, rev_date, rev_minor, rev_comment, rev_size, rev_tags)" +
            " VALUES (%s, %s, %s, %s, %s, %s, %s)", (article, user, revDate, int(minor), comment, size, tags))
        self.shared.conn.commit()

    def getMediaTypeID(self, type):
        self.shared.c.execute("SELECT * FROM MediaType WHERE mt_name = %s",
            (type,))
        result = self.shared.c.fetchall()
        if not result:
            logger.warning('Media type not found')
            return None
        else:
            logger.info('Media type %s found' % (result[0]['mt_name'], ))
            return result[0]['mt_id']

    def insertMedia(self, article, name, filetype):
        
        self.shared.c.execute("INSERT IGNORE INTO Media (media_article, media_name, media_type) " +
            "VALUES (%s, %s, %s)", (article, name, filetype))
        self.shared.conn.commit()

    def insertTemplate(self, key, val, article):
        logger.info("Template %s with value %s in article %s" % (key, val, article))
        self.shared.c.execute("INSERT IGNORE INTO Template (temp_article, temp_key, temp_value) VALUES " +
            "(%s, %s, %s)", (article, str(key), str(val)))
        self.shared.conn.commit()

    def getAllAnalyzedArticles(self):
        self.shared.c.execute("SELECT * FROM BaseArticle where ba_analyzed=True")
        return self.shared.c.fetchall()
    
    def getInfoboxID(self, name):
        self.shared.c.execute("SELECT * FROM Infobox where info_name=%$", (name,))
        return self.shared.c.fetchall()[0]["info_id"]

    def getAllInfoboxes(self):
        self.shared.c.execute("SELECT * FROM Infobox")
        return self.shared.c.fetchall()

    def insertInfoboxValue(self, key, value, article, infobox):
        self.shared.c.execute("INSERT INTO InfoboxPair(infopair_key, infopair_value, "+
            "infopair_article, infopair_info) VALUES(%s,%s,%s,%s)", (key, value, article, infobox))
        self.shared.conn.commit()
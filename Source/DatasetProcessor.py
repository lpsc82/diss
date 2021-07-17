import csv
import ApiInterface as ai
import logging
import datetime
import sys
import time

logger = logging.getLogger("mainlogger")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log to file
logging.basicConfig(filename='debug.txt',level=logging.INFO)
filehandler = logging.FileHandler("debug.txt", "w")
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

# Log to stdout too
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)

datasetList = [] #lista de duplas

datestr = "2021-01-01"

counter = 1

ilang = "zz"
if len(sys.argv) > 1:    
    ilang = " ".join(sys.argv[1:])
else:
    print("Insert language")

#cria datasetList de artigos a partir do dataset  
def processDataset(file):
    with open(file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        for row in csvreader:
            datasetList.append(row)

def processLanguageConcept(concept, lang):
    result = ai.getSearchResults(concept, lang) #resolve redirects
    logger.info("<<< Analyzing concept: %s, %s >>>" % (concept, str(counter)))
    articleID = ai.processQuery(concept, result[1], lang) #result[1] -> word count
    return articleID

logger.info("Processing query list")

if ilang == "en": # coluna de base

    processDataset("../dataset/dataset_en.txt") 

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        article_en_id = processLanguageConcept(line[0], "en") #insere artigo ->  id
        counter +=1

        logger.info("Storing Concept in database")    
        ai.database.insertConcept(article_en_id, datestr) #insere concept

        print("DELAYYY")
        time.sleep(1)


elif ilang == "pt":

    processDataset("../dataset/dataset_pt.txt")

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "fr":

    processDataset("../dataset/dataset_fr.txt")

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)

elif ilang == "de":

    processDataset("../dataset/dataset_de.txt")

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)

elif ilang == "ca":

    processDataset("../dataset/dataset_ca.txt")

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)

elif ilang == "it":

    processDataset("../dataset/dataset_it.txt")

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)

elif ilang == "ru":

    processDataset("../dataset/dataset_ru.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "ar":

    processDataset("../dataset/dataset_ar.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "id":

    processDataset("../dataset/dataset_id.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "tr":

    processDataset("../dataset/dataset_tr.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "el":

    processDataset("../dataset/dataset_el.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "hi":

    processDataset("../dataset/dataset_hi.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "bn":

    processDataset("../dataset/dataset_bn.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "fa":

    processDataset("../dataset/dataset_fa.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "zh":

    processDataset("../dataset/dataset_zh.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "ja":

    processDataset("../dataset/dataset_ja.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "he":

    processDataset("../dataset/dataset_he.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "ur":

    processDataset("../dataset/dataset_ur.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

elif ilang == "ko":

    processDataset("../dataset/dataset_ko.txt")  

    for line in datasetList:
        logger.info("Concept En: %s" % (line[0],))
        logger.info("Concept " + ilang + ": %s" % (line[1],))

        if(line[1] != "Not Found"):
            logger.info("New " +ilang+ " term")
            lang_id = processLanguageConcept(line[1], ilang)    
            counter +=1
        else:
            lang_id = None
        
        concept_lang = str("concept_" + ilang)

        en_id = ai.database.getEnId(line[0])  
       
        if not lang_id is None:
            logger.info("Updating Concept in database")
            ai.database.updateConcept(en_id, concept_lang, lang_id)  

else:
    print("Invalid language")

logger.info("Starting section hierarchy processing")

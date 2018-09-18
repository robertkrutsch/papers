"""
This is the an ieee xplore parsing. Be aware that one needs an account and each account has just 200 queries.
"""

import sys
from astor.file_util import fopen
sys.path.append('/home/robert/work/papers/3rdparty/xplore/xploreapi.py')
import xplore
from xml.etree.ElementTree import XML, fromstring, tostring


def write_articles(data):
    #parse the xml and write the abstracts into files
    myxml = fromstring(data)
    totalfound = 0 #how many articles we found
    nr_articles = 0 #used to parse the articles

    article_number = []
    publication_number = []
    title = []
    abstract = []

    for item in myxml:
        if (item.tag=="totalfound"):
            print (item.tag, item.text)
            totalfound = int(item.text)
        if (item.tag=="article"):
            for article_item in item:
                if (article_item.tag=="article_number"):
                    article_number.append(article_item.text)
                if (article_item.tag=="publication_number"):
                    publication_number.append(article_item.text)
                if (article_item.tag=="title"):
                    title.append(article_item.text)
                if (article_item.tag=="abstract"):
                    abstract.append(article_item.text)
            nr_articles += 1
        
    #write the lists to files
    for i in range(nr_articles):
        f = open(save_dir + publication_number[i] + "." + article_number[i]+".txt",'wt')
        f.write(abstract[i]) 
        f.close()
    
    return totalfound,nr_articles


save_dir = "/home/robert/work/papers/dataset_ieee/" #here we save all the papers 

"""
parse ieee and search for a certain keyword
"""
query = xplore.xploreapi.XPLORE('jxbje7zvg66y37t96cydaq6v')
query.authorText('precup')
query.dataType('xml')
data = query.callAPI()

totalfound,nr_articles = write_articles(data)

while (totalfound > nr_articles):
    query = xplore.xploreapi.XPLORE('jxbje7zvg66y37t96cydaq6v')
    query.authorText('precup')
    query.startingResult(nr_articles+1)
    query.dataType('xml')    
    data = query.callAPI()
    
             
    totalfound_tmp,nr_articles_tmp = write_articles(data)
    nr_articles += nr_articles_tmp
    
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import codecs
from glob import glob
import os

def checkExists(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def returnQuotedUrl(query,startPageNum):
    url = 'http://jglobal.jst.go.jp/search.php#{"keyword":"%s","synonym":null,"category":1,"order":"score","limit":100,"page":%d,"words":[]}' % (query,startPageNum)
    
    return urllib2.quote(url,':/#')


def returnIsNotLastPage(pagerElem):
    soup = BeautifulSoup(pagerElem.get_attribute('innerHTML'))
    pageButtons = soup.find('ul',{'class':'pageNumBtnsHolder'})
    if len(pageButtons.findAll('li')) ==0:
        return False
    elif pageButtons.findAll('li')[-1].find('strong') is not None:
        return False
    else:
        return True

def readKeywords(fileName='keywords.txt'):
    array=[]
    with codecs.open(fileName,'rb','utf-8') as f:
        for line in f.readlines():
            array.append(line.replace('\r\n',''))
    return array

def returnFilteredURLS():
    group_id_lkp = {'university':'CS',
                    'job':'JT',
                    'field':'RSB',
                    'affiliations':'SO',
                    'regions': 'RG',
                    'prefectures':'PF'
            

    }
    baseURL = 'http://jglobal.jst.go.jp/search.php#{"keyword":"京大","synonym":null,"category":1,"order":"score","limit":100,"page":1,"words":[{"count":10000,"title":"%s","code":"","category":1,"groupId":"%s","val":"%s"}]}'
    array = []

    files= glob('./filters/*.txt')
    for oneFile in files:
        fileType = os.path.basename(oneFile).split('_')[0]
        groupId = group_id_lkp[fileType] 
        with open(oneFile,'rb') as f:
            for filter in f.readlines():
                key = filter.replace('\n','').decode('utf-8')
                array.append(baseURL.decode('utf-8') % (key,groupId,key))
    return array

# URL = 'http://jglobal.jst.go.jp/search.php#{"keyword":"%s","synonym":null,"category":1,"order":"score","limit":100,"page":1,"words":[]}'
# keywords = readKeywords()
# scrapedKeywords = readKeywords(fileName='scrapedKeywords.txt')




# linkArray=readKeywords(fileName='AllKeyWordsLinks.txt')
# for keyword in keywords:
#     if keyword in scrapedKeywords:
#         print keyword.encode('utf-8')
#         continue
#     conditionFlag = True
#     count = 0
#     scrapeURL = URL % keyword
#     driver = webdriver.Chrome('chromedriver.exe')
#     driver.set_window_size(1920, 1000)
#     driver.get(scrapeURL)    
#     while conditionFlag:

#         button_xpath = "//a[contains(@class,'nextPageBtn')]/img"
#         table_xpath = "//table[contains(@class,'type1')]"

        
#         WebDriverWait(driver,60).until(EC.invisibility_of_element_located((By.ID, 'loading')))
                
#         table_contents_html = driver.find_element_by_xpath(table_xpath).get_attribute('innerHTML')
#         if len(table_contents_html)!=0:
#             soup = BeautifulSoup(table_contents_html)
#             with open('AllKeyWordsLinks.txt','a+') as f:
#                 for tr in soup.findAll('tr'):
#                     if tr.a is not None:
#                         if tr.a['href'] not in linkArray:
#                             linkArray.append(tr.a['href'])
#                             f.write(tr.a['href']+'\n')

#         nextButton = driver.find_element_by_xpath(button_xpath)
#         pagerElem = driver.find_element_by_xpath("//ul[contains(@class,'pager')]")

#         if nextButton.is_displayed() and returnIsNotLastPage(pagerElem):
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             count+=1
#             nextButton.click()
#         else:
#             conditionFlag=False
#         with open('allKeywordsLog.txt',"a+") as logFile:
#             logFile.write('%s keyword, %d pages scraped\n' %(keyword.encode('utf-8'),count))
#             logFile.write("%d pages scraped\n" % count)
#             print "%d pages scraped" % count
#             print "%d profiles scraped" % len(linkArray)
#             logFile.write("%d profiles scraped\n" % len(linkArray))
#     driver.quit()
#     with codecs.open('scrapedKeywords.txt','a+','utf-8') as a:
#         a.write(keyword+'\n')


urls = returnFilteredURLS()
linkArray=[]
for oneURL in urls:
    conditionFlag = True
    count = 0
  
    driver = webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1920, 1000)
    driver.get(oneURL)    
    while conditionFlag:

        button_xpath = "//a[contains(@class,'nextPageBtn')]/img"
        table_xpath = "//table[contains(@class,'type1')]"

        
        WebDriverWait(driver,60).until(EC.invisibility_of_element_located((By.ID, 'loading')))
                
        table_contents_html = driver.find_element_by_xpath(table_xpath).get_attribute('innerHTML')
        if len(table_contents_html)!=0:
            soup = BeautifulSoup(table_contents_html)
            with open('filteredKyotoLinks.txt','a+') as f:
                for tr in soup.findAll('tr'):
                    if tr.a is not None:
                        if tr.a['href'] not in linkArray:
                            linkArray.append(tr.a['href'])
                            f.write(tr.a['href']+'\n')

        nextButton = driver.find_element_by_xpath(button_xpath)
        pagerElem = driver.find_element_by_xpath("//ul[contains(@class,'pager')]")

        if nextButton.is_displayed() and returnIsNotLastPage(pagerElem):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            count+=1
            nextButton.click()
        else:
            conditionFlag=False
        with open('filteredKyotolog.txt',"a+") as logFile:
            logFile.write('%s url, %d pages scraped\n' %(oneURL.encode('utf-8'),count))
            logFile.write("%d pages scraped\n" % count)
            print "%d pages scraped" % count
            print "%d profiles scraped" % len(linkArray)
            logFile.write("%d profiles scraped\n" % len(linkArray))
    driver.quit()

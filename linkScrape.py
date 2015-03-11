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

# <codecell>

def loadLinks():
    linkArray=[]
    with open('profileLinksCollection.txt','rb') as f:
        for line in f:
            linkArray.append(line)
    return linkArray

links = loadLinks()
linkDict = {}
for line in links[580:]:
    driver = webdriver.Chrome("chromedriver.exe")
    driver.set_window_size(1920, 1000)
    driver.get(line)
    try:
        print "looking for content"
        def find(driver):
            e = driver.find_element_by_xpath("//a[contains(@title,'researchmap')]")
            if (e.value_of_css_property('display')=='block'):
                return False
            return e
        e = WebDriverWait(driver,600).until(find)
    finally: print "done loading" 
    uniqueID = (line.split('='))[1][:-2] #get id 
    englishSPAN = driver.find_element_by_xpath("//a[contains(@title,'researchmap')]")
    # soup = BeautifulSoup(englishSPAN.get_attribute('innerHTML'))
    try:
        link = englishSPAN.get_attribute('href')
        # link = soup.find('a')['href']
    except TypeError:
        link = 'NO LINK'
    
    linkDict[uniqueID] =link
    with open('researchMapLinks2.txt','a+') as f:
        f.write(uniqueID+','+link+'\n')
        
    driver.close()
    
print linkDict
        

# <codecell>

# for line in links:
print (line.split('='))[1][:-2] #get id 




from time import sleep
from attr import attributes
from pendulum import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("/Users/srulyrosenblat/Developer/CunySearch/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
classCollection =  db.collection('classes')
college = ''

PATH = '/Users/srulyrosenblat/Developer/selenium test/chromedriver'
driver = webdriver.Chrome(PATH)
driver.get(url ='https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController')

def crawlSite():
    # select = Select(driver.find_element(By.ID, 't_pd'))
    # dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
    # next = driver.find_element(By.NAME, 'next_btn')
    # select.select_by_index(2)
    # dropdownElems[1].click()
    # next.click()
    # loopThroughClasses()
    # driver.back()

    # sleep(1)
    for option in range(3):
        select = Select(driver.find_element(By.ID, 't_pd'))
        next = driver.find_element(By.NAME, 'next_btn')
        select.select_by_index(option +1)
        dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
        # half = (len(dropdownElems) +1) // 2
        # dropdownElems[5].click()
        dropdownElems[10].click()
        # dropdownElems[13].click()
        # for i in range(half, len(dropdownElems)):
        #     dropdownElems[i].click()
        #     sleep(.1)
        next.click()
        loopThroughClasses()
        driver.back()
    
def loopThroughClasses():
    i = 2
    select = Select(driver.find_element(By.ID, 'subject_ld'))
    length = len(select.options)
    if(length):
        for i in range(1, length):
            select = Select(driver.find_element(By.ID, 'subject_ld'))
            search = driver.find_element(By.ID, 'btnGetAjax')
            dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
            select.select_by_index(i)
            for check in dropdownElems:
                check.click()
            # select.select_by_index(0)
            search.click()
            readClasses()
            driver.back()

def handleDetailsScreen(classData):
    html_file = driver.page_source
    content = html_file
    soup = BeautifulSoup(content, 'html.parser')
    isOpen = soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_DESCRSHORT'}).get_text() == 'Open'
    description = soup.find(name='span',attrs={'id': 'DERIVED_CLSRCH_DESCRLONG'}).get_text()
    campus = soup.find(name='span',attrs={'id': 'CAMPUS_TBL_DESCR'}).get_text()
    # classType = soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG'}).get_text()
    preReq=  soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG'}).get_text()
    courseCode =  soup.find(name='span',attrs={'id': 'DERIVED_CLSRCH_DESCR200'}).get_text()
    college =  soup.find(name='span',attrs={'class': 'SSSKEYTEXT'}).get_text()
    college = college.strip().split(' | ')
    courseCode = courseCode.strip().split(' ')

    classData['collegeName'] = college[0]
    classData['term'] = college[1]
    classData['type'] = college[2]

    classData['courseCode']  = courseCode[0] + ' ' +  courseCode[1]

    classData['campus'] = campus
    classData['description'] = description
    classData['isOpen'] = isOpen
    classData['preReq']= preReq
    return

def handleMainScreen():
   pass

def readClasses():
    # with open('/Users/srulyrosenblat/Developer/CunySearch/home.html','r') as html_file:
    content =  driver.page_source
    # print(content)
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all(name="table", attrs={'border': '0'})
    c = 0
    classes = []
    for table in tables:
        if 'Days &amp; Times' in  str(table):
            c+=1
            # print()
           
            headers = table.find_all(name='td', attrs={'class': 'cunylitegridcollum'})
            atrs= table.find_all(name='td', attrs={'class': 'cunylite_LEVEL3GRIDROW'})
            classData = {}
            for i in range(1,len(headers)):
                category = str(headers[i].getText().replace(" ", "").replace('&',"And"))
                data = str(atrs[i].getText()).strip()
                classData[category] = data
                
                classes.append(classData)
            try: 
                driver.get('https://globalsearch.cuny.edu/CFGlobalSearchTool/' + table.a['href'])
                handleDetailsScreen(classData)
                sleep(.1)
                print(classData)
                classCollection.add(classData)
                driver.back()
            except Exception as e:
                driver.back()
                print(e)
    return classes




# handleSearchScreen()
crawlSite()

# print(f'{}')


from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
cred = credentials.Certificate('put firebase credentials here')
firebase_admin.initialize_app(cred)
db = firestore.client()
classCollection =  db.collection('classes')
college = ''

PATH = 'put path to chrome driver here'
driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get(url ='https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController')

def crawlSite():
    for option in range(3):
        select = Select(driver.find_element(By.ID, 't_pd'))
        next = driver.find_element(By.NAME, 'next_btn')
        select.select_by_index(option +1)
        dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
        amount = len(dropdownElems)
        for i in range(1,amount):
            if(i == 1):
                dropdownElems[0].click()
                dropdownElems[0].click()
            else:
                dropdownElems[i-1].click()
                sleep(getWait())
            dropdownElems[i].click()
            print(dropdownElems[i].text)
            sleep(getWait())      
            next.click()
            loopThroughClasses()
            driver.back()
    
def loopThroughClasses():
    select = Select(driver.find_element(By.ID, 'subject_ld'))
    length = len(select.options)
    dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
    for check in dropdownElems:
        check.click()
    if(length):
        for i in range(1, length):
            select = Select(driver.find_element(By.ID, 'subject_ld'))
            search = driver.find_element(By.ID, 'btnGetAjax')
            openCheckBox = driver.find_element(By.ID,'open_classId')
            if openCheckBox.is_selected():
                openCheckBox.click()
            print("     - "+ select.options[i].text)
            select.select_by_index(i)
            
            # select.select_by_index(0)
            search.click()
            readClasses()
            driver.back()

def handleDetailsScreen():
    delay = 3 # seconds
    try:
        html_file = driver.page_source
        content = html_file
        soup = BeautifulSoup(content, 'html.parser')
        description = soup.find(name='table',attrs={'id': 'ACE_SSR_CLS_DTL_WRK_GROUP6'}).text.replace("\\xa0",'').replace('\n','')
        requirements=  soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG'}).text.replace("\\xa0",'').replace('\n','')
        return (description,requirements)
    except TimeoutException:
        print("Loading took too much time!")
        return ('','')

def handleMainScreen():
   pass
def getWait():
    return randint(1,100) * .001


def readClasses():
    content =  driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all(name="table", attrs={'border': '0'})
    schoolInfo = soup.find(name='span', attrs={'class':'SSSKEYTEXT'}).text.replace("\xa0", '').split(' | ')
    schoolName = schoolInfo[0].strip()
    termInfo = schoolInfo[1].strip()
    subject = soup.find(name='strong').text.strip()

    c = 0
    uploadData =[]
    for table in tables:
        tableStr = str(table)
        description = ''
        requirements = ''
        if('cunylite_LABEL' in tableStr):
            classHeaders = table.find(name="span", attrs={'class': 'cunylite_LABEL'}).text
            classHeaders = classHeaders.replace("\xa0", '').split('-')
            classCode = classHeaders[0]
            topicName = classHeaders[1]
        if 'Days &amp; Times' in  tableStr:
            c+=1
            headers = table.find_all(name='td', attrs={'class': 'cunylitegridcollum'})
            classes = table.find_all(name='tr', attrs={})
            classData = {}
            
            l = 0
            for classInfo in classes:
                l+=1
                allClasses = []
                atrs= classInfo.find_all(name='td', attrs={'class': 'cunylite_LEVEL3GRIDROW'})
                if(len(atrs)):        
                    classData['link'] = 'https://globalsearch.cuny.edu/CFGlobalSearchTool/' + re.sub("&session_searched=\w*","&session_searched=NA" , classInfo.a['href']   )
                    if not description:
                        try: 
                            sleep(getWait())
                            
                            driver.get('https://globalsearch.cuny.edu/CFGlobalSearchTool/' + table.a['href'])
                            details = handleDetailsScreen()
                            description = details[0]
                            requirements = details[1]
                            classCollection.add(classData)
                            sleep(getWait() * 10)
                            driver.back()
                        except Exception as e:
                            driver.back()
                            print(e)
                    # print(classData['link'])
                    for i in range(1,len(headers)):
                        category = str(headers[i].getText().replace(" ", "").replace('&',"And"))
                        data = str(atrs[i].getText()).strip()
                        if(category == "Instructor"):
                            instructers =  re.findall('(?<=\>)(.*?)(?=\<)',str(atrs[i]))
                            addedTeachers = []
                            for teacher in instructers:
                                teacher = teacher.replace("\\xa0",'').strip()
                                teacher = teacher.split(',')
                                teacher.reverse()
                                teacher = ' '.join(teacher)
                                if(teacher not in addedTeachers):
                                    addedTeachers.append(teacher)
                                    # print(teacher)
                            classData[category] = teacher
                        else:

                            classData[category] = data
                        
                        allClasses.append(classData)
                    try: 
                        classCollection.add({'className': topicName, "classes":allClasses,"classCode":classCode,"schoolName": schoolName,"termInfo": termInfo,"subject": subject,'requirements':requirements,'description':description})
                    except Exception as e:
                        print(e)

    return classes

crawlSite()

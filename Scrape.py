
from time import sleep
from pendulum import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os

def crawlSite():
    PATH = '/Users/srulyrosenblat/Developer/selenium test/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get(url ='https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController')
    dropdownElems = driver.find_elements(By.CLASS_NAME, 'cunylite_DROPDOWNLIST')
    half = (len(dropdownElems) +1) // 2
    for  i in range(1,half):
        dropdownElems[i].click()
    sleep(1)
    # driver.back()
    for i in range(half, len(dropdownElems)):
        dropdownElems[i].click()
    select = Select(driver.find_element(By.ID, 't_pd'))
    print(select.options)
    for option in range(len(select.options)):
        select.select_by_index(option)
        # select.select_by_value(option)
        sleep(1)
    sleep(10)
   

def handleSearchScreen():
    with open('/Users/srulyrosenblat/Developer/CunySearch/home.html','r') as html_file:
        content = html_file.read() 
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        isOpen = soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_DESCRSHORT'}).get_text() == 'Open'
        description = soup.find(name='span',attrs={'id': 'DERIVED_CLSRCH_DESCRLONG'}).get_text()
        print(description, isOpen)

def handleMainScreen():
   pass

def readMainPage():
    with open('/Users/srulyrosenblat/Developer/CunySearch/home.html','r') as html_file:
        content = html_file.read() 
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.find_all(name="table", attrs={'border': '0'})
        c = 0
        classes = []
        for table in tables:
            if 'Days &amp; Times' in  str(table):
                c+=1
                # print(table)
                links = table.find_all(name='a')
                print(links)
                print(table.a)
                # headers = table.find_all(name='td', attrs={'class': 'cunylitegridcollum'})
                # atrs= table.find_all(name='td', attrs={'class': 'cunylite_LEVEL3GRIDROW'})
                # classData = {}
                # for i in range(1,len(headers)):
                #     category = str(headers[i].getText().replace(" ", "").replace('&',"And"))
                #     data = str(atrs[i].getText()).strip()
                #     classData[category] = data
                    
                #     classes.append(classData)
    return classes




# handleSearchScreen()
crawlSite()

# print(f'{}')
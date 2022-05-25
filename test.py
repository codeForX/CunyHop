

from pydoc import classname
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
import re
def handleDetailsScreen():
    with open('/Users/srulyrosenblat/Developer/CunySearch/home.html','r') as content:
        # html_file = driver.page_source
        # content = html_file
        content = content.read()

        soup = BeautifulSoup(content, 'html.parser')
        description = soup.find(name='table',attrs={'id': 'ACE_SSR_CLS_DTL_WRK_GROUP6'}).get_text().replace("\\xa0",'').replace('\n','')
        requirements=  soup.find(name='span',attrs={'id': 'SSR_CLS_DTL_WRK_SSR_REQUISITE_LONG'}).text.replace("\\xa0",'').replace('\n','')
        print((description,requirements))
        return (description,requirements)
print(handleDetailsScreen())
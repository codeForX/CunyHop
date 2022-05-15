

from bs4 import BeautifulSoup
import os
def websiteCrawler():
    pass
def readHtml():
    with open('/Users/srulyrosenblat/Developer/CunySearch/home.html','r') as html_file:
        content = html_file.read() 
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.find_all(name="table", attrs={'border': '0'})
        c = 0
        for table in tables:
            if 'Days &amp; Times' in  str(table):
                c+=1
                # print(table)
                headers = table.find_all(name='td', attrs={'class': 'cunylitegridcollum'})
                atrs= table.find_all(name='td', attrs={'class': 'cunylite_LEVEL3GRIDROW'})
                classData = {}
                for i in range(1,len(headers)):
                    category = str(headers[i].getText().replace(" ", "").replace('&',"And"))
                    data = str(atrs[i].getText()).strip()
                    classData[category] = data
                    print(classData) 
    return c




c = readHtml()


print(f'done {c}')
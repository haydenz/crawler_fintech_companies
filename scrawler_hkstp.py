from bs4 import BeautifulSoup
import requests
import urllib.request
import csv
import socket

def getData():
    url = 'https://www.hkstp.org/en/reach-us/company-directory/?i=&t=All&c=-1&s=-1&page='
    get_url = 'https://www.hkstp.org'

    for i in range(38,45): #page number
        try:
            request = urllib.request.Request(url + str(i))
            response = urllib.request.urlopen(request,timeout=10)
            soup = BeautifulSoup(response,'html.parser')
            tags = soup.find_all('div', class_="contentWrapper")
            for tag in tags: #for each company
                #print(get_url + tag.a['href'])
                name = tag.a.get_text()
                request1 = urllib.request.Request(get_url + tag.a['href'])
                response1 = urllib.request.urlopen(request1)
                soup1 = BeautifulSoup(response1,'html.parser')
                tags1 = soup1.find_all('div', class_="info-list")
                tel = None
                email = None
                web = None
                addr = None
                intro = None
                product = None
                person = None
                country = 'Hong Kong'
                city = 'Hong Kong'
                fintech_flag = False
                for tag1 in tags1: #for each info
                    if tag1.span != None:
                        info_class = str(tag1.span)[str(tag1.span).find('>')+1:str(tag1.span).find('<',1)]
                        #print(info_class  + str(len(info_class)))
                        if info_class == 'Tel':
                            tel = tag1.find('p').text
                        
                        elif info_class == 'Email':
                            email = tag1.p.a.get_text()
                        
                        elif info_class == 'Website':
                            web = tag1.p.a['href']
                            #print(web)
                        elif info_class == 'Address':
                            addr = tag1.find('p').text
                            addr = addr[11:len(addr)-10].replace(',\n',', ')
                            addr = addr.replace('\n',', ')
                            #print(addr.find('Hong Kong Science Park'))
                        
                            if addr.find('Hong Kong Science Park') != -1:
                                city = 'Hong Kong Science Park'
                            else:
                                addr1 = addr.split(', ')
                                try:
                                    city = addr1[addr1.index('Hong Kong')-1]
                                except Exception as e1:
                                    try:
                                        city = addr1[addr1.index('HK')-1]
                                    except Exception as e2:
                                        city = 'Hong Kong'

                            #print(city)
                        
                        elif info_class == 'Introduction':
                            intro = tag1.find('p').text
                            intro = intro[11:len(intro)-10].replace('\n\n', '\n')
                            fintech_flag = fintech(intro.lower())
                        
                        elif info_class == 'Product':
                            product = tag1.find('p').text
                            product = product[11:len(product)-10].replace('\n\n', '\n')
                            fintech_flag = fintech(product.lower())
                        
                        elif info_class == 'Contact Person':
                            person = tag1.find('p').text
                if fintech_flag:       
                    row = (3,1,name,country,city,web,'',product,intro,person,tel,email,addr)
                    with open('results38-44.csv', 'a', encoding='gb18030', newline='') as  f:
                        # obtain writer object
                        writer = csv.writer(f)
                        # write into one row
                        writer.writerow(row)
                        print(row)
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.timeout):
                pass
            else:
                print('[ERROR]: ' + str(error))
                
def fintech(MyString): #check whether it is a fintech company
    if MyString.find('financial') != -1 or MyString.find('finance') != -1 or MyString.find('fintech') != -1 or MyString.find('bank') != -1 or MyString.find('account') != -1 or MyString.find('asset') != -1 or MyString.find('insurance') != -1 or MyString.find('payment') != -1 or MyString.find('lend') != -1or MyString.find('loan')!= -1 or MyString.find('currency') != -1 or MyString.find('derivatives') != -1 or MyString.find('quantitative research') != -1 or MyString.find('robo-advisor') != -1 or MyString.find('roboadvisor') != -1:
        return True
    else:
        return False
    
 
if __name__ == '__main__':
    getData()

import bs4 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#url1 = 'https://www.lacelab.com/collections/luxury-leather-laces/products/black-luxury-leather-laces-gold-plated'
url1 = 'https://www.lacelab.com/collections/ultra-boost-shoe-laces/products/black-japanese-katakana-shoe-laces'
url2 = 'https://www.ropelacesupply.com/collections/all-shoe-laces/products/flat-red-shoe-laces'

#connecting,downloading,closing webpage
uClient = uReq(url1)
page_html = uClient.read()
uClient.close()

#html parse
pageSoup = soup(page_html, "html.parser")
laceDetails = pageSoup.findAll("script",{"type":"text/javascript"})
stringLace = str(laceDetails[10])
meat = stringLace.splitlines()[4]

sampleString = "inventory_quantity"

meat = meat[meat.find(':[{"id"'):]
#print(meat)
rawList = []
nameList = []
priceList =[]
quantList = []

for x in range(0,meat.count(sampleString)):
    rawList.append(meat[meat.find('{"id"') + 2 : meat.find('}') + 1]) 
    meat = meat[meat.find('}')+1:]
    #print(itemList[x])
    #print()
    if rawList[x].find("\"name\""):
        nameList.append(rawList[x][rawList[x].find("\"name\"") + 8 : rawList[x].find('public_title') - 5 ])

    if rawList[x].find("\"price\""):
        temp = rawList[x][rawList[x].find("\"price\"") + 8 : rawList[x].find('weight') - 2 ]
        priceList.append(temp[0:2] + '.' + temp[2:])

    if rawList[x].find("\"inventory_quantity\""):
        quantList.append(rawList[x][rawList[x].find("\"inventory_quantity\"") + 21 : rawList[x].find('inventory_management') - 2 ]) 
    print(nameList[x])
    print(priceList[x]) 
    print(quantList[x])
    print()



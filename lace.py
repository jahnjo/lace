import bs4 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys
import random
import string

urls = ['https://www.lacelab.com/collections/luxury-leather-laces/products/black-luxury-leather-laces-gold-plated',
'https://www.ropelacesupply.com/collections/premium-leather-shoe-laces/products/black-chrome-leather-laces',
'https://www.ropelacesupply.com/collections/all-shoe-laces/products/g-o-a-t-flat-shoe-laces']

#Containers
laceData = ''
#Used in order to find out how many different sizes/types of laces are on the page
sampleString = "inventory_quantity"
#Containers to hold all the information
rawList = []
nameList = []
priceList =[]
quantList = []

def randWorksheet():
    rand = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(5))
    return rand

def urlRequest(currentURL):
    #Connecting, Downloading, Closing webpage
    uClient = uReq(currentURL)
    pageHTML = uClient.read()
    uClient.close()
    return pageHTML

def parseHTML(page):
    #pageSoup holds all the HTML within bs4 object
    pageSoup = soup(page, "html.parser")
    return pageSoup

def getTag(rawHTML):
    #Holds all the HTML within <script type="text/javascript"> tags
    scriptTags = rawHTML.findAll("script",{"type":"text/javascript"})
    return scriptTags

def getLaceData(rawScript):
    currentTag = []
    global laceData
    #Going through each <script> tag and finding the right one with the lace data
    for x in range(0,len(rawScript)):
        #Casting bs4 object to string to use find() function
        currentTag.append(str(rawScript[x]))
        #print(currentTag[x])

        #lacelab.com algorithm
        if currentTag[x].find("new Shopify") != -1:
            #print("found 1")
            laceData = currentTag[x]

        #ropelacesupply.com algorithm    
        elif currentTag[x].find("var json_product") != -1:
            #print("found 2")
            laceData = currentTag[x]

def getBeginning():
    global laceData
    #Aligning the parse to accurately iterate through each item
    laceData = laceData[laceData.find(':[{"id"'):]

def getOutOfStock():
    global laceData
    #Checking if the item is sold out
    if laceData.count(sampleString) == 0:
        print("Item sold out")
        sys.exit(0)

def getData():
    global laceData
    global sampleString
    global rawList
    global nameList
    global priceList
    global quantList
    #Parsing through each item and putting name, price, quantity into their respective container.
    for x in range(0,laceData.count(sampleString)):
        rawList.append(laceData[laceData.find('{"id"') + 2 : laceData.find("</script>")]) 
        laceData = laceData[laceData.find('}')+1:]

        if rawList[x].find("\"name\""):
            nameList.append(rawList[x][rawList[x].find("\"name\"") + 8 : rawList[x].find('public_title') - 5 ])

        if rawList[x].find("\"price\""):
            temp = rawList[x][rawList[x].find("\"price\"") + 8 : rawList[x].find('weight') - 2 ]
            #print(temp)
            #priceList.append(temp[0:2] + '.' + temp[2:])
            priceList.append(str(format(int(temp)/100, '.02f')))

        if rawList[x].find("\"inventory_quantity\""):
            quantList.append(rawList[x][rawList[x].find("\"inventory_quantity\"") + 21 : rawList[x].find('inventory_management') - 2 ]) 
        print(nameList[x])
        print(priceList[x]) 
        print(quantList[x])
        print()

def clearData():
    global laceData
    global rawList
    global nameList
    global priceList
    global quantList
    laceData = ''
    rawList = []
    nameList = []
    priceList = []
    quantList = []


#Main
for x in range(0,len(urls)):
    dlContent = urlRequest(urls[x])
    HTMLsoup = parseHTML(dlContent)
    rawScriptData = getTag(HTMLsoup)
    getLaceData(rawScriptData)
    getBeginning()
    getOutOfStock()
    getData()
    clearData()

















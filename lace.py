import bs4 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sys

#url1 = 'https://www.lacelab.com/collections/luxury-leather-laces/products/black-luxury-leather-laces-gold-plated'
#url1 = 'https://www.ropelacesupply.com/collections/premium-leather-shoe-laces/products/black-chrome-leather-laces'
url1 = 'https://www.ropelacesupply.com/collections/all-shoe-laces/products/g-o-a-t-flat-shoe-laces'

#Connecting, Downloading, Closing webpage
uClient = uReq(url1)
page_html = uClient.read()
uClient.close()

#pageSoup holds all the HTML within bs4 object
pageSoup = soup(page_html, "html.parser")

#Holds all the HTML within <script type="text/javascript"> tags
laceDetails = pageSoup.findAll("script",{"type":"text/javascript"})

#Pre-initializing container variables
meat = ''
currentTag = []

#Going through each <script> tag and finding the right one with the lace data
for x in range(0,len(laceDetails)):
    #Casting bs4 object to string to use find() function
    currentTag.append(str(laceDetails[x])

    #lacelab.com algorithm
    if currentTag[x].find("new Shopify") != -1:
        meat = currentTag[x]

    #ropelacesupply.com algorithm    
    elif currentTag[x].find("var json_product") != -1:
        meat = currentTag[x]

#Used in order to find out how many different sizes/types of laces are on the page
sampleString = "inventory_quantity"

#Aligning the parse to accurately iterate through each item
meat = meat[meat.find(':[{"id"'):]

#Containers to hold all the information
rawList = []
nameList = []
priceList =[]
quantList = []

#Checking if the item is sold out
if meat.count(sampleString) == 0:
    print("Item sold out")
    sys.exit(0)

#Parsing through each item and putting name, price, quantity into their respective container.
for x in range(0,meat.count(sampleString)):
    rawList.append(meat[meat.find('{"id"') + 2 : meat.find("</script>")]) 
    meat = meat[meat.find('}')+1:]

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



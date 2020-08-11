import requests
from bs4 import BeautifulSoup
import pandas as pd

# This number checks if an expression is a number
# if it is number returns true else returns false
# requires input of the number
def isNumber(Str):
    try:
        float(Str)
        return True
    except ValueError:
        return False

# This function extracts data using the
# beautiful soup library. requires the url,
# the name of the tag and the attribute
def extractSoup(url,name,attrs):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find(name, attrs=attrs)
    return table

############# functions to remove after ###############
#test function
def headingTest(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html5lib')
    headingList = []
    for heading in soup.find_all(["h2"]):
        headingList.append([url,heading.name,heading.text.strip()])

    return headingList

# This function returns information from the community info page of an MLS
# Listing requires the url of the listing and returns a 2d array of the info
# table
def CommunityInfo(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('div', attrs={"class":'si-ld-details__item clearfix js-masonary-item js-collapsible'})
    infoData = {}
    for elem in table.findChildren("div"):
        infoData.update({elem.find("strong").text:[elem.find("span").text.strip()]})
    return infoData

# This function returns the table info of an MLS listing into an array
# requires the url of the page and table name
def MlsInfo(URL, Table_Name):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    tables = soup.findAll('div', {'class':'si-ld-details__item js-masonary-item js-collapsible'})
    infoData = {}
    for table in tables:
        if table.h2.text == Table_Name:
            for elem in table.findAll("div"):
                infoData.update({elem.strong.text:elem.span.text.strip()})
    return infoData


# This function extracts the data for price change history
# returns an array of data requires the Url of the MLS page
def MlsPriceChange(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    priceChange = soup.find('section', {'class': 'si-ld-price-history is-collapse js-collapsible'})
    table = []
    if hasattr(priceChange, 'table') == True:
        allrows = priceChange.table.findAll('tr')
        for row in range(1,len(allrows)):
            col = allrows[row].findAll('td')
            table.append([col[0].text,col[1].text,col[2].text,col[3].text])
    else:
        table.append([None, None, None, None])
    return table

# This function extracts the data for room info of an MLS listing
# returns an array of data extracted requires the Url of the mls listing
# site
def MlsRoomInfo(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    roomTable = soup.find('table', {'id': 'tblRooms'})
    table = []
    if roomTable != None:
        allrows = roomTable.findAll('tr')
        for row in allrows:
            col = row.findAll('td')
            table.append([col[0].text, col[1].text, col[2].text, col[3].text])
    else:
        table.append([None, None, None, None])
    return table
#
# URL = "https://www.livrealestate.ca/idx/4012-crestview-rd-sw-calgary-ab-t2t-2l4/10940161_spid/"
# output = MlsRoomInfo(URL)
# print(output)

# This function extracts the primary info regarding the MLS listing
# requires the URL and returns an array of data
def MlsMainInfo(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    mainInfo = soup.find('div', {'class': 'si-ld-primary__info clearfix'})
    table = {}
    for elem in mainInfo.findAll('div'):
        table.update({elem.strong.text:[elem.span.text.strip()]})
        #table.append([elem.strong.text, elem.span.text])
    return table

# This function returns the price of an MLS listing requires the URL
# and returns the price
# covert into private functions in the object
def MlsPrice(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    price = soup.find('span', {'class': 'si-ld-top__price'})
    return price.text.strip()

# This function returns the description of an MLS listing requires the URL
# and return the description
def MlsDescription(URL):
    assert type(URL) == str, "URL must be expressed as a string"
    assert len(URL) > 0, "URL length must be greater then 0"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    description = soup.find('div', {'class': 'si-ld-description js-listing-description'})
    return description.text.strip()

# this function coverts a dictionary to a panda data frame requires
# the dictionary as input
def dictToDataFrame(Dict):
    assert isinstance(Dict, dict), "variable must be a dictionary"

    df = pd.DataFrame(Dict)
    return df

# this function coverts an array into a proper panda data frame with
# rows and columns requires the array as input
def ArrayToDataFrame(Arr):
    assert isinstance(Arr, list), "variable must be a List"

    df = pd.DataFrame(Arr, columns=Arr[0])
    df = df[1:]
    return df

#
# URL = "https://www.livrealestate.ca/idx/443-mahogany-blvd-se-calgary-ab-t3m-1z5/13032683_spid/"
# infoArray = ["Architecture","Features / Amenities","Property Features","Tax and Financial Info","Price Change History"]
# data = MlsInfo(URL,infoArray[0])
# print(data)

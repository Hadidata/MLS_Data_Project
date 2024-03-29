
#This module runs the main data extraction functions for MLS lisitngs
from msilib.schema import Property

import requests
from bs4 import BeautifulSoup
import pandas as pd
import Functions as fun
import csv

#Declare static values that can be changed here

def priceChangeHistory():
    colNames = ['Link','Date','Old Price','New Price','Percent Change']
    return colNames

def roomInfo():
    colNames = ['Link', 'Rooms', 'Level', 'Size', 'Description']
    return colNames



# This Class extracts data from the website Live Real Estate
# The property of this class includes the URL for the city quadrant
# number of pages to extract (if left blank then the peoperty will be
# assigned based on an internal function

class liveMls:
    def __init__(self,Url,Pages=None):

        assert type(Url) == str, "URL must be expressed as a string"
        assert len(Url) > 0, "URL length must be greater then 0"

        self.Url = Url
        if Pages == None:
            Pages = self.__getlastPage(Url)
            self.Pages = Pages
        else:
            assert type(Pages) == int, "Number of pages must be expressed as an integer"
            assert Pages > 0, "Number of pages requested must be greater then 0"
            self.Pages = Pages

    ### Public classes go here ###

    # This method returns the URL of the Mls listing pages that
    # must be extracted
    @property
    def getPageUrl(self):
        PageLinks = []
        for page in range(1,self.Pages+1):
            NewUrl = self.Url + "?pg=" + str(page)
            PageLinks.append(NewUrl)
        return PageLinks

    # This method returns the Url of the individual Mls Listing
    # intalize this before using any other methods
    def getMlsUrl(self, progress=False):

        linkList = []
        frontUrl = "https://www.livrealestate.ca"
        numPage = self.getPageUrl
        indPage = 1
        MaxPage = len(numPage)
        for page in numPage:
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'html5lib')
            links = soup.findAll('a', attrs={'class': 'js-listing-detail'})
            # Extract the links in the page
            for link in links:
                if link['href'] != 'javascript:void(0);':
                    linkList.append(frontUrl + link['href'])
            if progress == True:
                print("Page " + str(indPage) + " of " + str(MaxPage) + " extracted")
                indPage = indPage + 1
        return linkList

    # this method is used to extract the top level info of an MLS listing that
    def getTopLevelInfo(self,links):
        assert links != None, "Links cannot be empty, Did you forgot to call the getMlsUrl Method?"

        #extract price, square feet, year
        #everyting for the section class si-ld-primary
        data = []
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            #extract the price of the MLS listing
            price = soup.find('span',{'class':'si-ld-top__price'})
            data.append([link, "Price", price.text.strip()])
            details = soup.find('div',{'class':'si-ld-primary__info clearfix'})
            #get description associated with the property
            desc = soup.find('div',{'class':'si-ld-description js-listing-description'})
            data.append([link,"Description",desc.text.strip()])
            #to extract bottom level info that is tied to a table
            for det in details:
                if det.find('div') != -1:
                    col = det.find('strong').text
                    val = det.find('span').text.strip()
                    data.append([link, col, val])
        # pivoting logic to show data as a column
        col = ('url', 'col', 'values')
        pddata = pd.DataFrame(data, columns=col)
        pivotData = pddata.pivot(index=col[0], columns=col[1], values=col[2])
        return (pivotData)


    # This method returns the price change history (if avaliable) of all
    # returns a dataframe
    def getPriceChangeHistory(self,links,progress=False):
        #links = self.getMlsUrl(progress=progress)
        assert links != None, "Links cannot be empty, Did you forgot to call the getMlsUrl Method?"

        colNames = priceChangeHistory()
        data = []
        indPage = 1
        MaxPage = len(links)
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            priceChange = soup.find('section', {'class': 'si-ld-price-history is-collapse js-collapsible'})
            if hasattr(priceChange, 'table') == True:
                allrows = priceChange.table.findAll('tr')
                for row in range(1,len(allrows)):
                    col = allrows[row].findAll('td')
                    data.append([link,col[0].text, col[1].text, col[2].text, col[3].text])
            else:
                data.append([link,None,None,None,None])
            if progress == True:
                print("Page " + str(indPage) + " of " + str(MaxPage) + " extracted -- Price History")
                indPage = indPage + 1
        dataFrame = pd.DataFrame(data, columns=colNames)
        return dataFrame

    # The method returns Roominfo of a specific MLS listing as a dataframe
    def getRoomInfo(self, links,progress=False):
        #links = self.getMlsUrl(progress=progress)
        assert links != None, "Links cannot be empty, Did you forgot to call the getMlsUrl Method?"

        colNames = roomInfo()
        data = []
        indPage = 1
        MaxPage = len(links)
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            roomTable = soup.find('table', {'id': 'tblRooms'})
            if roomTable != None:
                allrows = roomTable.findAll('tr')
                for row in range(1,len(allrows)):
                    col = allrows[row].findAll('td')
                    data.append([link,col[0].text, col[1].text, col[2].text, col[3].text])
            else:
                data.append([link,None, None, None, None])
            if progress == True:
                print("Page " + str(indPage) + " of " + str(MaxPage) + " extracted -- Room Info")
                indPage = indPage + 1
        dataFrame = pd.DataFrame(data, columns=colNames)
        return dataFrame

    #This method returns information about an MLS listing based on the header
    #requires the mls listing URl, header name under info type to check against
    #outputs a dataframe table with the URL it pulled data from and the columns extracted from it
    def getHeaderInfo(self,links,infoType, progress=False):
        #links = self.getMlsUrl(progress=progress)
        assert links != None, "Links cannot be empty, Did you forgot to call the getMlsUrl Method?"
        assert len(infoType) > 0, "infoType must have a valid header value"

        data = []
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            propertyDetails = soup.find('section',{'id':'propertyDetails'})
            for header in propertyDetails:
                #print(header.find('h2'))
                if header.find('h2') != -1:
                    if infoType == header.find('h2').text:
                        table = header.findAll('div')
                        for elem in table:
                            col = elem.find('strong').text
                            val = elem.find('span').text.strip()
                            data.append([link,col,[val]])

        #pivoting logic to show data as a column
        col = ('url', 'col', 'values')
        pddata = pd.DataFrame(data, columns=col)
        pivotData = pddata.pivot(index=col[0], columns=col[1], values=col[2])
        return(pivotData)

    ### Private classes go here ###

    # This method returns the last page of a city sector
    # expressed an an integer
    # requires the city sector URL as an input
    def __getlastPage(self,Link):
        r = requests.get(Link)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs={'class': 'si-container si-pager js-lw-pager'})
        pageList = []
        for item in table.findAll('li'):
            if fun.isNumber(item.text) == True:
                pageList.append(int(item.text))
        return max(pageList)


def test():
    URL = "https://www.livrealestate.ca/calgary-city-centre/"
    mls = liveMls(Url=URL,Pages=1)
    mlslinks = mls.getMlsUrl(progress=False)
    data = mls.getTopLevelInfo(mlslinks)
    data.to_csv("C:\\Users\\Hadi-PC\\Desktop\\Projects\\MLS_Test\\toplevelinfo.csv")

if __name__ == '__main__':
    test()


# Dump to csv for comprehensive logic testing (price history)
#
# URL = "https://www.livrealestate.ca/calgary-city-centre/"
# URL = "https://www.livrealestate.ca/calgary-west/"
# URL = "https://www.livrealestate.ca/calgary-east/"
# URL = "https://www.livrealestate.ca/calgary-northeast/"
# URL = "https://www.livrealestate.ca/calgary-northwest/"
# URL = "https://www.livrealestate.ca/calgary-south/"
# URL = "https://www.livrealestate.ca/calgary-southeast/"
# MlsData = liveMls(URL).getRoomInfo(progress=True)
# #print(MlsData)
# csvString = "C://Users//Hadi-PC//PycharmProjects//Extracts//Rooms_CityCenter.csv"
# MlsData.to_csv(csvString,index=False)


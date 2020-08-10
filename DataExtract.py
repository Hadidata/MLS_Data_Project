
#This module runs the main data extraction functions for MLS lisitngs
from msilib.schema import Property

import requests
from bs4 import BeautifulSoup
import pandas as pd
import Functions as fun
import csv

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

    # This property returns the price change history (if avaliable) of all
    # returns a dataframe
    def getPriceChangeHistory(self, progress=False):
        links = self.getMlsUrl(progress=progress)
        colNames = ['Link','Date','Old Price','New Price','Percent Change']
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
    def getRoomInfo(self, progress=False):
        links = self.getMlsUrl(progress=progress)
        colNames = ['Link', 'Rooms', 'Level', 'Size', 'Description']
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

    #This method returns the properties of an Mls listing returns a dataframe
    def getMaininfo(self, infoType, progress=False):
        pass

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


# This class communicates with the MLS data website
# requires the input url

import requests
import Functions as fun
from bs4 import BeautifulSoup



class WebConnector():
    def __init__(self, mainUrl):
        assert type(mainUrl) == str, "URL must be expressed as a string"
        assert len(mainUrl) > 0, "URL length must be greater then 0"
        self.mainUrl = mainUrl

    # this method pull all the url of a city quadrant based on the
    # city, region and the number of pages requested if pagefirst or
    # pagelast is 0 then max page is used.
    def PullRegionalLinks(self, city, region, page_first=0, page_last=0, progress=False):

        assert type(city) == str, "city must be expressed as a string"
        assert len(city) > 0, "city length must be greater then 0"
        assert type(region) == str, "region must be expressed as a string"
        assert len(region) > 0, "region length must be greater then 0"

        if page_first==0 or page_last==0:
            page_last = self.GetLastQuadrantPage(city=city,region=region)
            page_first = 1

        linkList = []
        frontUrl = "https://www.livrealestate.ca"
        for page in range(page_first,page_last+1):
            pageLink = self.mainUrl + "/" + city + "-" + region + "/?pg=" + str(page)
            r = requests.get(pageLink)
            soup = BeautifulSoup(r.content, 'html5lib')
            links = soup.findAll('a', attrs={'class': 'js-listing-detail'})
            for link in links:
                if link['href'] != "javascript:void(0);":
                    linkList.append(frontUrl + link['href'])
            if progress == True:
                print("Page " + str(page) + " of " + str(page_last) + " extracted")
        return linkList


    # this method
    def PullListingData(self, mls_url):

        assert type(mls_url) == str, "mls_url must be expressed as a string"
        assert len(mls_url) > 0, "mls_url length must be greater then 0"

        r = requests.get(mls_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        priceChange = soup.find('section', {'class': 'si-ld-price-history is-collapse js-collapsible'})
        roomInfo = soup.find('table', {'id': 'tblRooms'})
        mainInfo = soup.find('div', {'class': 'si-ld-primary__info clearfix'})
        price = soup.find('span', {'class': 'si-ld-top__price'})
        description = soup.find('div', {'class': 'si-ld-description js-listing-description'})
        communityInfo = soup.find('div', {'class': 'si-ld-details__item clearfix js-masonary-item js-collapsible'})
        output_dict = {'priceChange':priceChange,
                       'roomInfo':roomInfo,
                       'mainInfo':mainInfo,
                       'price': price,
                       'description': description,
                       'Community Information': communityInfo}

        tables = ["Architecture", "Features / Amenities", "Property Features", "Tax and Financial Info"]
        for table in tables:
            output_dict[table] = self.__MlsInfo(mls_url,table)

        return output_dict

    # this property extracts the last page of a quadrant requires
    # city and region be popuilated in the PullRegionalLinks Method
    def GetLastQuadrantPage(self,city,region):

        assert type(city) == str, "city must be expressed as a string"
        assert len(city) > 0, "city length must be greater then 0"
        assert type(region) == str, "region must be expressed as a string"
        assert len(region) > 0, "region length must be greater then 0"

        firstPageUrl = self.mainUrl + "/" + city + "-" + region + "/"
        name = 'div'
        attribute = {'class': 'si-container si-pager js-lw-pager'}
        r = requests.get(firstPageUrl)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find(name, attrs=attribute)
        pageList = []
        for item in table.findAll('li'):
            if fun.isNumber(item.text) == True:
                pageList.append(int(item.text))
        return max(pageList)

    def __MlsInfo(self,url, table_name):

        assert type(url) == str, "url must be expressed as a string"
        assert len(url) > 0, "url length must be greater then 0"

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        tables = soup.findAll('div', {'class': 'si-ld-details__item js-masonary-item js-collapsible'})
        output = None
        for table in tables:
            if table.h2.text == table_name:
                output = table
        return output
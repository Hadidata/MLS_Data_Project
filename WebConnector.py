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
    def PullRegionalLinks(self, city, region, page_first=0, page_last=0):

        assert type(city) == str, "city must be expressed as a string"
        assert len(city) > 0, "city length must be greater then 0"
        assert type(region) == str, "region must be expressed as a string"
        assert len(region) > 0, "region length must be greater then 0"

        if page_first==0 or page_last==0:
            page_last = self.GetLastQuadrantPage(city=city,region=region)
            page_first = 1

        for page in range(page_first,page_last):
            pass


    # this method
    def PullListingData(self, mls_url):
        pass

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
        table = fun.extractSoup(firstPageUrl,name,attribute)
        pageList = []
        for item in table.findAll('li'):
            if fun.isNumber(item.text) == True:
                pageList.append(int(item.text))
        return max(pageList)


"https://www.livrealestate.ca/calgary-south/"

frontUrl = "https://www.livrealestate.ca"
testClass = WebConnector(frontUrl)
print(testClass.GetLastQuadrantPage("edmonton","central"))

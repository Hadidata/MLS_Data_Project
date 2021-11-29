#This module is the Main python file that calls all other python files/classes that interact with the SQL Database

from DataExtract import liveMls
from pandas import DataFrame as df
from datetime import datetime

# transfer these to a database table where they can be logged
# and updated as needed

#list of city quadrant URLs from the liverealestate website
def mainUrls():
    return (

           {'center':"https://www.livrealestate.ca/calgary-city-centre/",
           'west':"https://www.livrealestate.ca/calgary-west/",
           'east':"https://www.livrealestate.ca/calgary-east/",
           'northeast':"https://www.livrealestate.ca/calgary-northeast/",
           'northwest':"https://www.livrealestate.ca/calgary-northwest/",
           'south':"https://www.livrealestate.ca/calgary-south/",
           'southeast':"https://www.livrealestate.ca/calgary-southeast/"}
           )


#list of property details that need to be extracted from the website
#the first value is the header name that needs to be supplied to the
#website the second is the output file name
def propertyDetails():
    return(
                  {'community_information':'Community Information',
                   'architecture':'Architecture',
                   'property_features':'Property Features',
                   'tax_financial_info':'Tax and Financial Info',
                   'features_amenities':'Features / Amenities'}
    )


#this method is used to extract the data for MLS listings within a
# city quadrant specify a path and the quadrant name
def getQuandrantMls(path,quadrant):

    timeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    URL = mainUrls()[quadrant]
    mls = liveMls(Url=URL, Pages=1)
    mlslinks = mls.getMlsUrl(progress=False)
    for detail in propertyDetails():
        data = mls.getHeaderInfo(infoType=propertyDetails()[detail],links=mlslinks)
        data.to_csv(path + '\\' + detail + '_' + quadrant + timeStamp + '_' + ".csv")

    roomInfo = mls.getRoomInfo(mlslinks,progress=False)
    roomInfo.to_csv(path + '\\' + 'room_info' + '_' + quadrant + timeStamp + '_' + ".csv",index=False)

    priceHistory = mls.getPriceChangeHistory(mlslinks,progress=False)
    priceHistory.to_csv(path + '\\' + 'price_history' + '_' + quadrant + '_' + timeStamp + ".csv", index=False)

    #topLevelInfo = mls.get


def main():
    path = 'C:\\Users\\Hadi-PC\\Desktop\\Projects\\MLS_Test'
    print(getQuandrantMls(path,'west'))
    #URL = "https://www.livrealestate.ca/calgary-city-centre/"

    #initalize the mls class
    #mls = liveMls(Url=URL,Pages=1)

    #get the urls of each listing
    #listing_url = mls.getMlsUrl(progress=True)
    #mlsPriceHistory = mls.getPriceChangeHistory(listing_url,progress=True)
    #listing_url.to_csv("C:/Users/Hadi-PC/Downloads/room_data_test.csv",index=False)


if __name__== "__main__":
    main()
#This module is the Main python file that calls all other python files/classes that interact with the SQL Database

from DataExtract import liveMls
from pandas import DataFrame as df

test_array = ["https://www.livrealestate.ca/idx/1020-9-ave-se-calgary-ab-t2g-0s7/13050739_spid/",
              "https://www.livrealestate.ca/idx/2429-25-st-sw-calgary-ab-t3e-1x5/10948220_spid/",
              "https://www.livrealestate.ca/idx/230-39-ave-sw-calgary-ab-t2s-0w5/12106898_spid/"]


def main():
    URL = "https://www.livrealestate.ca/calgary-city-centre/"

    #initalize the mls class
    mls = liveMls(Url=URL,Pages=1)

    #get the urls of each listing
    listing_url = mls.getMlsUrl(progress=True)
    mlsPriceHistory = mls.getPriceChangeHistory(listing_url,progress=True)
    #listing_url.to_csv("C:/Users/Hadi-PC/Downloads/room_data_test.csv",index=False)


if __name__== "__main__":
    main()

#This module is for unit testing

import unittest as ut
from DataExtract import liveMls
import pandas as pd

class TestliveMls(ut.TestCase):

    #Testing Properties
    #this test is to check if the URL is being passed correctly
    def test_URL(self):
        Url = "xxxx"
        mlsData = liveMls(Url,2)
        self.assertEqual(mlsData.Url, Url, "Propery Url Should be " + mlsData.Url)
        Url1 = 12  # capture integer error
        with self.assertRaises(AssertionError) as cm:
            liveMls(Url1,2)
            exception = cm.exception
            self.assertEqual(exception.error_code,6)
        Url2 = "" # capture blank error
        with self.assertRaises(AssertionError) as ct:
            liveMls(Url2,2)
            exception = ct.exception
            self.assertEqual(exception.error_code, 6)

    #test the pages property
    def test_pages(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        mlsData = liveMls(Url)
        self.assertNotEqual(mlsData.Pages,None,"Property pages should be a number")
        page = "12" #yeild an assertion error
        with self.assertRaises(AssertionError) as ct:
            liveMls(Url,page)
            exception = ct.exception
            self.assertEqual(exception.error_code, 6)
        page = 0  # yeild an assertion error
        with self.assertRaises(AssertionError) as ct:
            liveMls(Url, page)
            exception = ct.exception
            self.assertEqual(exception.error_code, 6)

    # Test the method getPageUrl to see if an array is returned
    def test_getPageUrl(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        mlsData = liveMls(Url)
        self.assertIsInstance(mlsData.getPageUrl,list,"getPageUrl must return an array")
    # Test the method getPageUrl to see if the number of pages equals the lenght of array
        pages = 3
        mlsData = liveMls(Url,pages)
        self.assertEqual(len(mlsData.getPageUrl), pages, "Array size must be " + str(pages))

    # Test the method getMlsUrl to see if an array is returned
    def test_getMlsUrl(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        pages = 2
        mlsData = liveMls(Url,pages)
        self.assertIsInstance(mlsData.getMlsUrl(), list, "getMlsUrl must return an array")
        mlsData = liveMls(Url,pages)
        data = mlsData.getMlsUrl()
        #print(data)
        self.assertEqual(len(data),(pages*12), "Output Array length " +
            str(len(data)) + " is not " + str((pages*12)-1))

    # Test the method getPriceChangeHistory to see if a data is returned
    def test_getPriceChangeHistory(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        pages = 2
        numbOfColumns = 5
        mlsData = liveMls(Url, pages)
        history = mlsData.getPriceChangeHistory()
        self.assertEqual(isinstance(history,pd.DataFrame),True,"Price Change History Output is Not a Dataframe")
        #check dimmensions
        self.assertEqual(len(history.columns),numbOfColumns, "Number of Columns should be " + str(numbOfColumns))

    def test_getRoomInfo(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        pages = 2
        numbOfColumns = 5
        mlsData = liveMls(Url, pages)
        rooms = mlsData.getRoomInfo()
        self.assertEqual(isinstance(rooms, pd.DataFrame), True, "Room Info Output is Not a dataframe")
        # check dimmensions
        self.assertEqual(len(rooms.columns), numbOfColumns, "Number of Columns should be " + str(numbOfColumns))

    #test if the assertion error for infoarray is working when a blank list is given
    def test_getMaininfoAssertion(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        pages = 1
        numbOfColumns = 5
        mlsData = liveMls(Url, pages)
        with self.assertRaises(AssertionError) as ct:
            mainInfo = mlsData.getMaininfo([], progress=False)
            exception = ct.exception
            self.assertEqual(exception.error_code, 6)


    #test if a dataframe is returned
    def test_getMaininfoDataFrame(self):
        Url = "https://www.livrealestate.ca/calgary-city-centre/"
        pages = 1
        numbOfColumns = 5
        infoArray = ["Architecture", "Features / Amenities", "Property Features", "Tax and Financial Info",
                     "Price Change History"]
        mlsData = liveMls(Url, pages)
        mainInfo = mlsData.getMaininfo(infoArray[0],progress=False)
        self.assertEqual(isinstance(mainInfo, pd.DataFrame), True, "Main Info output is not a dataframe")

    #test if having more then one infoArray defined yields a dataframe with more columns
    def test_getMaininfoMutiData(self):
        pass

if __name__ == "__main___":
    ut.main()


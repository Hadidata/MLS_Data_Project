import Functions as fun
import csv

# this script extracts the headings for a listing in python


def listingHeading(url,csvString):
    last = fun.lastPage(url)

    ListingHeading = []
    for page in range(1,last):
        propertyUrl = fun.getPageUrl(url + "?pg=" + str(page))
        print("Page " + str(page) + " of " + str(last) + " data extracted")
        for link in range(0,len(propertyUrl)):
            ListingHeading.append(fun.headingTest(propertyUrl[link]))

    with open(csvString, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for row in ListingHeading:
            for col in row:
                writer.writerow(col)

listingHeading("https://www.livrealestate.ca/calgary-west/", "Calgary_West.csv")
listingHeading("https://www.livrealestate.ca/calgary-east/", "Calgary_East.csv")
listingHeading("https://www.livrealestate.ca/calgary-city-centre/", "Calgary_Center.csv")
listingHeading("https://www.livrealestate.ca/calgary-northeast/", "Calgary_Northeast.csv")
listingHeading("https://www.livrealestate.ca/calgary-northwest/", "Calgary_Northwest.csv")
listingHeading("https://www.livrealestate.ca/calgary-south/", "Calgary_South.csv")
listingHeading("https://www.livrealestate.ca/calgary-southeast/", "Calgary_Southeast.csv")





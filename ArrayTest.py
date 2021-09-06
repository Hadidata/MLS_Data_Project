from WebConnector import WebConnector
import pandas as pd

# this function is a test to extract all data that is not room or
# price change history,
def getAllData(cityQuad):
    # extract all the url for the city quadrant

    con = WebConnector("https://www.livrealestate.ca")
    urlList = con.PullRegionalLinks("calgary", cityQuad,progress=True)
    # extract data for the following dictionary objects
    # main info, price, description
    # "Architecture", "Features / Amenities", "Property Features", "Tax and Financial Info"
    # Community Info

    mlslist = []
    ind = 0
    maxInd = len(urlList)
    for url in urlList:
        mlsobj = con.PullListingData(url)
        # main info
        mlsData = {}
        maininfo = mlsobj['mainInfo']
        if maininfo != None:
            for elem in maininfo.findAll('div'):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        # price
        price = mlsobj['price'].text.strip()
        mlsData.update({"Price": price})

        # description
        description = mlsobj['description'].text.strip()
        mlsData.update({"Description": description})

        # Architecture
        arch = mlsobj['Architecture']
        if arch != None:
            for elem in arch.findAll("div"):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        # "Features / Amenities"
        feat = mlsobj["Features / Amenities"]
        if feat != None:
            for elem in feat.findAll("div"):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        # Property Features
        prop = mlsobj["Property Features"]
        if prop != None:
            for elem in prop.findAll("div"):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        # Tax and Financial Info
        fin = mlsobj["Tax and Financial Info"]
        if fin != None:
            for elem in fin.findAll("div"):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        # Community Info
        com = mlsobj["Community Information"]
        if com != None:
            for elem in com.findAll("div"):
                mlsData.update({elem.strong.text: elem.span.text.strip()})

        mlslist.append(mlsData)
        ind = ind + 1
        print("Listing " + str(ind) + " of " + str(maxInd) + " extracted")
    return mlslist

if __name__ == '__main__':
    data = pd.DataFrame(getAllData("city-centre"))
    csvString = "C://Users//Hadi-PC//PycharmProjects//Extracts//DataOutput//AllDataCityCenter.csv"
    data.to_csv(csvString,index=False)



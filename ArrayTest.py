import numpy as np
import pandas as pd
import Functions as fun


URL = "https://www.livrealestate.ca/idx/408-33-ave-nw-calgary-ab-t2a-7s4/13043246_spid/"
URL1 = "https://www.livrealestate.ca/idx/443-mahogany-blvd-se-calgary-ab-t3m-1z5/13032683_spid/"

#print(fun.MlsInfo(URL,"Property Features"))
#print(fun.MlsInfo(URL1,"Property Features"))

dict1 = {'Lot Size:': '0.07 Acres', 'Lot Dimensions:': '7.6 x 37', 'Lot Features:': 'Back Lane, Back Yard, Front Yard, Low Maintenance Landscape, Level, Near Public Transit', 'Front Exposure:': 'South', 'Community Features:': 'Sidewalks', 'Zoning:': 'R-C2'}
dict2 = {'Lot Size:': ['0.08 Acres'], 'Lot Dimensions:': ['8.27 x 35.02'], 'Lot Features:': ['Back Lane, Back Yard, Near Shopping Center, Near Public Transit, Private'], 'Front Exposure:': ['South'], 'Community Features:': ['Lake, Playground, Sidewalks, Street Lights'], 'Sewer Septic:': ['Public Sewer'], 'Zoning:': ['R-2M']}

dictList = [dict1,dict2]

dt = pd.DataFrame(dictList)

print(dt)


# df1 = pd.DataFrame(data=Array1)
# df2 = pd.DataFrame(data=Array2)
#
# app = df1.append(df2)

# URL = "https://www.livrealestate.ca/idx/408-33-ave-nw-calgary-ab-t2a-7s4/13043246_spid/"
# array = fun.MlsRoomInfo(URL)
# df1 = pd.DataFrame(array, columns=array[0])
# df1 = df1[1:]
# print(df1)



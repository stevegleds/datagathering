# ************ Districts ************
# PIVOT_DISTRICT_FILE = data_output+'\\pivot_district.csv'  # contains summary results
# PIVOT_MUNICIPALITY_FILE = data_output+'\\pivot_municipality.csv'  # contains summary results
#  MYDSP_LOG_FILE = data_sources+'\\12-12.log"  # needed to get correct country codes (3 letters)

#  dfdistricts = pd.read_csv(DISTRICTS_FILE)

dfresults = pd.merge(left=dfresults, right=dfdistricts, how='left', on='Latitude')
dfresults.rename(index=str, columns={"Longitude_x": "Longitude", "Longitude_y": "District Longitude"}, inplace=True)
print("df results datatypes with added district columns: \n", dfresults.dtypes)
dfresults = dfresults.apply(checkdistrict, axis=1)
# use following line if districts needed
# def addextradata(dfresults, dfcountry, dfdistricts):
def checkdistrict(df):
    #  If longitude is equal to longitude of district file then we are sure we have the correct district.
    #  Return unchanged if it is equal or change to 'unknown' otherwise
    try:
        int(df['Longitude'])
        if int(df['Longitude'] * 10000) == int(df['District Longitude'] * 10000):
            pass
        else:
            df['District'] = 'Unknown'
            df['Municipality'] = 'Unknown'
    except:
        pass
    return df


"1 Parse log file to get country codes from mydsp (obsolete)"
if ans == 1:
    response = input("Are you sure? This is no longer required. Type YES to continue \n")
    if not response.lower() == 'YES':
        pass
    else:
        dfcountrycodes = get3lettercountrycodes(countrycodeset)
        print('Raw country codes are: ', dfcountrycodes)
        print('First few results before country codes', dfresults.head())
        dfcountrycodes.to_csv(COUNTRY_CODE_FILE)
        dfresults = addcountrycodedata(dfresults, dfcountrycodes)

#  print('Main df datatypes: /n', dfresults.dtypes)

# comment out next 2 lines if needed for districts
# pivotmunicipality = pd.pivot_table(dfresults, index=["Municipality"],
#                           values=["Download", "Upload"],
#                           aggfunc=['count', 'sum', 'mean', 'median'])
# pivotdistrict = pd.pivot_table(dfresults, index=["District"],
#                           values=["Download", "Upload"],
#                           aggfunc=['count', 'sum', 'mean', 'median'])

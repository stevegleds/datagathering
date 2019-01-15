from math import sqrt
#  import datetime
import pandas as pd


def addextradata(dfresults, dfcountry, dfdistricts):
    dfresults['Date Time'] = pd.to_datetime(dfresults['Timestamp'], unit='ms')
    print("dfresults head:\n", dfresults.head())
    print("dfcountry head:\n", dfcountry.head())
    print("Adding Country information: City information, Peak / Off peak times")
    dfresults = pd.merge(left=dfresults, right=dfcountry, how='left', left_on='Country',
                         right_on='Country Code 2')
    print("Calculating if each result is in the city or not")
    dfresults['Distance'] = dfresults.apply(getdistance, axis=1)
    print("Calculating if each result is peak or offpeak")
    dfresults['City'] = dfresults['Distance'] <= dfresults['Radius']
    dfresults['Hour'] = dfresults['Date Time'].dt.hour
    #  print(dfresults[['Date Time', 'Hour']])
    dfresults['Peak End'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['Peak-End-GMT'])
    dfresults['Peak Start'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['Peak-Start-GMT'])
    dfresults['Peak'] = dfresults.apply(getpeak, axis=1)
    dfresults.rename(index=str, columns={"Latitude_x": "Latitude", "Longitude_x": "Longitude", "Latitude_y": "CityLat",
                                         "Longitude_y": "CityLong", "Country_x": "CountryCode",
                                         "Country_y": "Country Name"}, inplace=True)
    dfresults = pd.merge(left=dfresults, right=dfdistricts, how='left', on='Latitude')
    dfresults.rename(index=str, columns={"Longitude_x": "Longitude", "Longitude_y": "District Longitude"}, inplace=True)
    #  print("df results datatypes with added district columns: \n", dfresults.dtypes)
    dfresults = dfresults.apply(checkdistrict, axis=1)
    return dfresults


def addcountrycodedata(dfresults, dfcountrycodes):
    dfresults = pd.merge(left=dfresults, right=dfcountrycodes, how='left', left_on='Timestamp', right_on='Raw Timestamp')
    return dfresults


def getdistance(df):
    lat_distance = (df['Latitude_x'] - df['Latitude_y']) * df['Latitude-Length']
    long_distance = (df['Longitude_x'] - df['Longitude_y']) * df['Longitude-Length']
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def getpeak(df):
    return df['Peak-End-GMT'] >= df['Hour'] >= df["Peak-Start-GMT"]


def filterbycountry(df, countrycodeset):
    df = df[df['CountryCode'].isin(countrycodeset)]
    return df


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

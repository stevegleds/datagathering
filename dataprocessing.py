from math import sqrt
#  import datetime
import pandas as pd


def addextradata(dfresults, dfcountry):
    dfresults['Date Time'] = pd.to_datetime(dfresults['Timestamp'], unit='ms')
    print("dfresults head:\n", dfresults.head())
    print("dfcounty head:\n", dfcountry.head())
    print("dfresults datatypes\n", dfresults.dtypes)
    print("dfcountry datatypes\n", dfcountry.dtypes)
    dfresults = pd.merge(left=dfresults, right=dfcountry, how='left', left_on='Raw Country Code',
                         right_on='Country Code 3')
    #  todo find a way to rename columns to more meaningful
    # dfresults.rename(index=str, columns={"Latitude_x": "Latitude", "Longitude_x": "Longitude", "Latitude_y": "CityLat", "Longitude_y": "CityLong"})
    print("df results datatypes with added columns: \n", dfresults.dtypes)
    dfresults['Distance'] = dfresults.apply(getdistance, axis=1)
    dfresults['City'] = dfresults['Distance'] <= dfresults['Radius']
    dfresults['Hour'] = dfresults['Date Time'].dt.hour
    dfresults['Peak End'] = dfresults['Country Code 3'].map(dfcountry.set_index('Country Code 3')['Peak-End-GMT'])
    dfresults['Peak Start'] = dfresults['Country Code 3'].map(dfcountry.set_index('Country Code 3')['Peak-Start-GMT'])
    dfresults['Peak'] = dfresults.apply(getpeak, axis=1)
    return dfresults


def addcountrycodedata(dfresults, dfcountrycodes):
    dfresults = pd.merge(left=dfresults, right=dfcountrycodes, how='left', left_on='Timestamp', right_on='Raw Timestamp')
    # dfresults['Raw Country Code'] = dfresults['Timestamp'].map(dfcountrycodes.set_index('Raw Timestamp')['Raw countrycode'])
    # print("new country info is:", dfresults['Timestamp', 'Raw Country Code'])
    return dfresults


def getdistance(df):
    lat_distance = (df['Latitude_x'] - df['Latitude_y']) * df['Latitude-Length']
    long_distance = (df['Longitude_x'] - df['Longitude_y']) * df['Longitude-Length']
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def getpeak(df):
    #  print('gettingpeak', df['Peak Start'], df['Hour'], df['Peak End'])
    return df['Peak End'] >= df['Hour'] >= df["Peak Start"]



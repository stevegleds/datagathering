from math import sqrt
#  import datetime
import pandas as pd


def addextradata(dfresults, dfcountry):
    dfresults['Date Time'] = pd.to_datetime(dfresults['Timestamp'], unit='ms')
    print(dfresults.head())
    dfresults['Radius'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Radius'])
    dfresults['CityLat'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Latitude'])
    dfresults['CityLong'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Longitude'])
    dfresults['LatLength'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Latitude-Length'])
    dfresults['LongLength'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Longitude-Length'])
    dfresults['Distance'] = dfresults.apply(getdistance, axis=1)
    dfresults['City'] = dfresults['Distance'] <= dfresults['Radius']
    dfresults['Hour'] = dfresults['Date Time'].dt.hour
    dfresults['Peak End'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Peak-End-GMT'])
    dfresults['Peak Start'] = dfresults['Country'].map(dfcountry.set_index('Country Code 2')['Peak-Start-GMT'])
    dfresults['Peak'] = dfresults.apply(getpeak, axis=1)
    return dfresults


def addcountrycodedata(dfresults, dfcountrycodes):
    dfresults = pd.merge(left=dfresults, right=dfcountrycodes, how='left', left_on='Timestamp', right_on='Raw Timestamp')
    # dfresults['Raw Country Code'] = dfresults['Timestamp'].map(dfcountrycodes.set_index('Raw Timestamp')['Raw countrycode'])
    # print("new country info is:", dfresults['Timestamp', 'Raw Country Code'])
    return dfresults


def getdistance(df):
    lat_distance = (df['Latitude'] - df['CityLat']) * df['LatLength']
    long_distance = (df['Longitude'] - df['CityLong']) * df['LongLength']
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def getpeak(df):
    #  print('gettingpeak', df['Peak Start'], df['Hour'], df['Peak End'])
    return df['Peak End'] >= df['Hour'] >= df["Peak Start"]



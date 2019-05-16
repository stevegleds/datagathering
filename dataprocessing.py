from math import sqrt
#  import datetime
import pandas as pd


def addextradata(dfresults, dfcountry, dfpopserver, dfproviders):
    dfresults['Date Time'] = pd.to_datetime(dfresults['Timestamp'], unit='ms')
    print("dfresults head:\n", dfresults.head())
    print("dfcountry head:\n", dfcountry.head())
    print("Adding Country information: City information, Peak / Off peak times")
    dfresults = pd.merge(left=dfresults, right=dfcountry, how='left', left_on='Country',
                         right_on='Country Code 2')
    print("        ... Done")
    print("Adding POP Server information: City, Country and Continent of POP Servers")
    dfresults = pd.merge(left=dfresults, right=dfpopserver, how='left', left_on='POP Unique',
                         right_on='POP')
    print("        ... Done")
    print("Adding Providers information: Country, Owner, Group etc.")
    dfresults = pd.merge(left=dfresults, right=dfproviders, how='left', left_on='ISP2',
                         right_on='Providers')
    print("        ... Done")
    print("Calculating distance of each result from the capital")
    dfresults['Distance'] = dfresults.apply(getdistance, axis=1)
    print("        ... Done")
    print("Calculating if each result is within the City radius")
    dfresults['City'] = dfresults['Distance'] <= dfresults['Radius']
    print("        ... Done")
    print("Calculating the hour of the day of each result")
    dfresults['Hour'] = dfresults['Date Time'].dt.hour
    print("        ... Done")
    print("Adding Peak Start and End times from country data")
    dfresults['Peak End'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['Peak-End-GMT'])
    dfresults['Peak Start'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['Peak-Start-GMT'])
    print("        ... Done")
    print("Adding AM Start and End times from country data")
    dfresults['AM End'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['AM-End-GMT'])
    dfresults['AM Start'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['AM-Start-GMT'])
    print("        ... Done")
    print("Adding PM Start and End times from country data")
    dfresults['PM End'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['PM-End-GMT'])
    dfresults['PM Start'] = dfresults['Country Code 2'].map(dfcountry.set_index('Country Code 2')['PM-Start-GMT'])
    print("        ... Done")
    print("Calculating if each result is during peak time or not")
    dfresults['Peak'] = dfresults.apply(getpeak, axis=1)
    print("        ... Done")
    print("Calculating if each result is during AM or not")
    dfresults['AM'] = dfresults.apply(get_am, axis=1)
    print("        ... Done")
    print("Calculating if each result is during PM or not")
    dfresults['PM'] = dfresults.apply(get_pm, axis=1)
    print("        ... Done")
    print("Adding time of day column")
    dfresults['TOD'] = dfresults.apply(get_time_of_day, axis=1)
    print("        ... Done")
    print("Renaming column names")
    dfresults.rename(index=str, columns={"Latitude_x": "Latitude", "Longitude_x": "Longitude", "Latitude_y": "CityLat",
                                         "Longitude_y": "CityLong", "Country_x": "CountryCode",
                                         "Country_y": "Country Name", "POP_y": "POP Lookup", "POP_x": "POP"}, inplace=True)
    return dfresults


def getdistance(df) -> float:
    lat_distance = (df['Latitude_x'] - df['Latitude_y']) * df['Latitude-Length']
    long_distance = (df['Longitude_x'] - df['Longitude_y']) * df['Longitude-Length']
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def getpeak(df) -> bool:
    return df['Peak-End-GMT'] >= df['Hour'] >= df["Peak-Start-GMT"]


def get_pm(df) -> bool:
    return df['PM-End-GMT'] >= df['Hour'] >= df["PM-Start-GMT"]


def get_am(df) -> bool:
    return df['AM-End-GMT'] >= df['Hour'] >= df["AM-Start-GMT"]


def get_time_of_day(df) -> str:
    if df['AM']:
        return 'AM'
    elif df['PM']:
        return 'PM'
    return 'NA'


def filterbycountry(df, countrycodeset: list):
    df = df[df['CountryCode'].isin(countrycodeset)]
    return df



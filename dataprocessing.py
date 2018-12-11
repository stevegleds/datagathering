from math import sqrt
import datetime
import pandas as pd

def findGeoDistance(lat: float, long: float, centrelat: float, centrelong: float, lengthlat: float, lengthlong: float):
    """

    :return:
    """
    #   =SQRT(((H2-centre_lat)*lengthlat)^2 + ((I2-centre_long)*lengthlong)^2)
    lat_distance = (lat - centrelat) * lengthlat
    long_distance = (long - centrelong) * lengthlong
    print(lat_distance, long_distance)
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def incity(distance: float, radius: float):
    return distance <= radius


def addcitypeaktimedata(countries: dict, speed_data: dict):
    for country in countries:
        for result in speed_data:
            if result['Country'] == country['IP']:
                print(country['IP'], country['Radius'], float(result['City Distance']) <= float(country['Radius']), result['City Distance'])
                #   city_results += 1
                lat, long, cityLat, cityLong, latLength, longLength = float(result['Latitude']), float(result['Longitude']),\
                                                                      float(country['Latitude']), float(country['Longitude']),\
                                                                      float(country['Latitude-Length']), float(country['Longitude-Length'])
                result['newDistance'] = findGeoDistance(lat, long, cityLat, cityLong, latLength, longLength)
                result['newCity'] = result['newDistance'] <= float(country['Radius'])
                result['newHour'] = int(result['Date Time'][-5:-3])
                result['newPeak'] = int(country['Peak-End']) >= result['newHour'] >= int(country['Peak-Start'])
                result['newDate'] = datetime.datetime
                # todo remove int() if not needed
                # TODO add 'peak' calculation
                # print(newDistance, 'True distance is:', result['City Distance'])
                # print(newCity, 'In City is: ', result['City?'])
                # print('City results total: ', city_results)
    return speed_data


def getdistance(df):
    #   =SQRT(((H2-centre_lat)*lengthlat)^2 + ((I2-centre_long)*lengthlong)^2)
    lat_distance = (df['Latitude'] - df['CityLat']) * df['LatLength']
    long_distance = (df['Longitude'] - df['CityLong']) * df['LongLength']
    #  print(lat_distance, long_distance)
    return sqrt((lat_distance ** 2) + (long_distance ** 2))


def getpeak(df):
    #  print('gettingpeak', df['Peak Start'], df['Hour'], df['Peak End'])
    return df['Peak End'] >= df['Hour'] >= df["Peak Start"]


def addextradata(dfresults, dfcountry):
    dfresults['Date Time'] = pd.to_datetime(dfresults['Timestamp'], unit='ms')
    print(dfresults.head())
    dfresults['Radius'] = dfresults['Country'].map(dfcountry.set_index('Country')['Radius'])
    dfresults['CityLat'] = dfresults['Country'].map(dfcountry.set_index('Country')['Latitude'])
    dfresults['CityLong'] = dfresults['Country'].map(dfcountry.set_index('Country')['Longitude'])
    dfresults['LatLength'] = dfresults['Country'].map(dfcountry.set_index('Country')['Latitude-Length'])
    dfresults['LongLength'] = dfresults['Country'].map(dfcountry.set_index('Country')['Longitude-Length'])
    dfresults['Distance'] = dfresults.apply(getdistance, axis=1)
    dfresults['City'] = dfresults['Distance'] <= dfresults['Radius']
    dfresults['Hour'] = dfresults['Date Time'].dt.hour
    #  int(country['Peak-End']) >= result['newHour'] >= int(country['Peak-Start'])
    dfresults['Peak End'] = dfresults['Country'].map(dfcountry.set_index('Country')['Peak-End'])
    dfresults['Peak Start'] = dfresults['Country'].map(dfcountry.set_index('Country')['Peak-Start'])
    dfresults['Peak'] = dfresults.apply(getpeak, axis=1)
    return dfresults
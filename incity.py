from math import sqrt


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
                # TODO add 'peak' calculation
                # print(newDistance, 'True distance is:', result['City Distance'])
                # print(newCity, 'In City is: ', result['City?'])
                # print('City results total: ', city_results)
    return speed_data

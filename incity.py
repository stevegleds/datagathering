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

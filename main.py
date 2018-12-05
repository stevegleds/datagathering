from parse import parse, save_results
from incity import findGeoDistance, incity

DATA_FILE = 'mesample.csv'  # this is the raw data
OUTPUT_FILE = 'output.csv'  # this is the raw data with fields for city and peak time info
CONSTANTS_FILE = 'meconstants.csv'  # contains data about city radiius etc.

print('Data file used is: ', DATA_FILE)
print('Output file used is:', OUTPUT_FILE)


def main():
    speed_data = parse(DATA_FILE, ',')
    print('Speed data is:', speed_data)
    countries = parse(CONSTANTS_FILE, ',')
    for country in countries:
        print(country['Radius'])
    print('The countries are:', countries)
    print('The countries are: ', countries)
    city_results = 0
    for country in countries:
        for result in speed_data:
            if result['Country'] == country['IP']:
                print(country['IP'], country['Radius'], float(result['City Distance']) <= float(country['Radius']), result['City Distance'])
                if float(result['City Distance']) <= float(country['Radius']):
                    city_results += 1
                lat, long, cityLat, cityLong, latLength, longLength = float(result['Latitude']), float(result['Longitude']),\
                                                                      float(country['Latitude']), float(country['Longitude']),\
                                                                      float(country['Latitude-Length']), float(country['Longitude-Length'])
                result['newDistance'] = findGeoDistance(lat, long, cityLat, cityLong, latLength, longLength)
                result['newCity'] = result['newDistance'] <= float(country['Radius'])
                # print(newDistance, 'True distance is:', result['City Distance'])
                # print(newCity, 'In City is: ', result['City?'])
                # print('City results total: ', city_results)
    results = speed_data  # results is same as input for testing only
    test = findGeoDistance(31.983977, 35.924226, 31.9289, 35.9154, 110885.5465, 94565.95484)
    print(test)
    radius = 15000
    city = incity(test, radius)
    print('City ? ', city)
    save_results(OUTPUT_FILE, results)


if __name__ == "__main__":
    main()

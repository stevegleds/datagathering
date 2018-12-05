from parse import parse, save_results
from incity import findGeoDistance, incity, addcitypeaktimedata

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
    #  city_results = 0
    results = addcitypeaktimedata(countries, speed_data)
    #  results = speed_data  # results is same as input for testing only
    save_results(OUTPUT_FILE, results)


if __name__ == "__main__":
    main()

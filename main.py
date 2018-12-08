from parse import parse, save_results
from dataprocessing import findGeoDistance, incity, addcitypeaktimedata
import pandas as pd

DATA_FILE = 'mesample.csv'  # this is the raw data
OUTPUT_FILE = 'output.csv'  # this is the raw data with fields for city and peak time info
CONSTANTS_FILE = 'meconstants.csv'  # contains data about city radiius etc.
PIVOT_FILE = 'pivotresults.csv'  # contains summary results

print('Data file used is: ', DATA_FILE)
print('Output file used is:', OUTPUT_FILE)


def main():
    ans = True
    while ans:
        print('''
        Process new data file:
        1 Parse source file to internal dict
        2 Parse constants file to internal countries dict
        3 Add City and Peak time columns to results and create output file
        
        Analyse output file:
        4 Create Pivot table Country > City > Peak > Type
        5 Send Pivot to pivot file
        6 Testing options
        ''')
        ans = int(input('What do you want?'))
        if ans == 1:
            speed_data = parse(DATA_FILE, ',')
        if ans == 2:
            countries = parse(CONSTANTS_FILE, ',')
        if ans == 3:
            results = addcitypeaktimedata(countries, speed_data)
            save_results(OUTPUT_FILE, results)
        if ans == 4:
            df = pd.read_csv(OUTPUT_FILE)
            print(df.head())
            pivot = pd.pivot_table(df, index=["Country", "New City", "New Peak", "ConnectionType"], values=["Download"],
                           aggfunc=['count', 'sum', 'mean', 'median'])
            print(pivot)
        if ans == 5:
            with open(PIVOT_FILE, "w", newline='') as f:
                pivot.to_csv(f)
            f.close()
        if ans == 6:
            print(df['Country'])
            pass

    # speed_data = parse(DATA_FILE, ',')
    # print('Speed data is:', speed_data)
    # countries = parse(CONSTANTS_FILE, ',')
    # for country in countries:
    #     print(country['Radius'])
    # print('The countries are:', countries)
    # print('The countries are: ', countries)
    # #  city_results = 0
    # results = addcitypeaktimedata(countries, speed_data)
    # #  results = speed_data  # results is same as input for testing only
    # save_results(OUTPUT_FILE, results)
    # df = pd.read_csv(OUTPUT_FILE)
    # print(df.head())
    # pivot = pd.pivot_table(df, index=["Country", "New City", "New Peak", "ConnectionType"], values=["Download"],
    #                        aggfunc=['count', 'sum', 'mean', 'median'])
    # print(pivot)
    # with open(PIVOT_FILE, "w", newline='') as f:
    #     pivot.to_csv(f)
    # f.close()

if __name__ == "__main__":
    main()

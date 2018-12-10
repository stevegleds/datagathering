from parse import parse, save_results
from dataprocessing import findGeoDistance, incity, addcitypeaktimedata, getdistance, getpeak
import pandas as pd


DATA_FILE = 'mesample.csv'  # this is the raw data
EXCEL_FILE = 'mesample.xlsx'
#  EXCEL_FILE = 'me20181127-01.xlsx'
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
        
        7 Do it all in pandas
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
        if ans == 7:  # do it all in pandas
            countryfile = pd.read_csv(CONSTANTS_FILE)
            df = pd.read_excel(EXCEL_FILE)
            df['Date Time'] = pd.to_datetime(df['Timestamp'], unit='ms')
            print(df.head())
            df['Radius'] = df['Country'].map(countryfile.set_index('Country')['Radius'])
            df['CityLat'] = df['Country'].map(countryfile.set_index('Country')['Latitude'])
            df['CityLong'] = df['Country'].map(countryfile.set_index('Country')['Longitude'])
            df['LatLength'] = df['Country'].map(countryfile.set_index('Country')['Latitude-Length'])
            df['LongLength'] = df['Country'].map(countryfile.set_index('Country')['Longitude-Length'])
            df['Distance'] = df.apply(getdistance, axis=1)
            df['City'] = df['Distance'] <= df['Radius']
            df['Hour'] = df['Date Time'].dt.hour
            #  int(country['Peak-End']) >= result['newHour'] >= int(country['Peak-Start'])
            df['Peak End'] = df['Country'].map(countryfile.set_index('Country')['Peak-End'])
            df['Peak Start'] = df['Country'].map(countryfile.set_index('Country')['Peak-Start'])
            df['Peak'] = df.apply(getpeak, axis=1)
            print(df[['Date Time', 'Country', 'Hour', 'City', 'Peak']])
            df.to_csv("df.csv")


if __name__ == "__main__":
    main()

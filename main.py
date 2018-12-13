from parse import parse, save_results
from dataprocessing import findGeoDistance, incity, addcitypeaktimedata, getdistance, getpeak, addextradata
import pandas as pd


CSV_FILE = '13mydsp2.csv'  # this is the raw data
EXCEL_FILE = 'mesample.xlsx'
#  EXCEL_FILE = 'me20181127-01.xlsx'
OUTPUT_FILE = 'output.csv'  # this is the raw data with fields for city and peak time info
CONSTANTS_FILE = 'meconstants.csv'  # contains data about city radiius etc.
PIVOT_FILE = 'pivotresults.csv'  # contains summary results

print('Data file used is: ', CSV_FILE)
print('Output file used is:', OUTPUT_FILE)


def main():
    outputfilecreated = False
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
        8 Create pivot table(s)
        ''')
        ans = int(input('What do you want?'))
        if ans == 1:
            speed_data = parse(CSV_FILE, ',')
        if ans == 2:
            countries = parse(CONSTANTS_FILE, ',')
        if ans == 3:
            results = addcitypeaktimedata(countries, speed_data)
            save_results(OUTPUT_FILE, results)
        if ans == 4:
            dfresults = pd.read_csv(OUTPUT_FILE)
            print(dfresults.head())
            pivot = pd.pivot_table(dfresults, index=["Country", "New City", "New Peak", "ConnectionType"], values=["Download"],
                           aggfunc=['count', 'sum', 'mean', 'median'])
            print(pivot)
        if ans == 5:
            with open(PIVOT_FILE, "w", newline='') as f:
                pivot.to_csv(f)
            f.close()
        if ans == 6:
            print(dfresults['Country'])
            pass
        if ans == 7:  # do it all in pandas:
            dfcountry = pd.read_csv(CONSTANTS_FILE)
            dfresults = pd.read_csv(CSV_FILE)
            dfresults = addextradata(dfresults, dfcountry)
            print(dfresults[['Date Time', 'Country', 'Hour', 'City', 'Peak']])
            try:
                dfresults.to_csv(OUTPUT_FILE)
            except:
                print(OUTPUT_FILE, "is open")
            outputfilecreated = True
        if ans == 8:
            if not outputfilecreated:
                print("Please process raw data file before analysing. Option 7.")
            else:
                print(dfresults.head())
                pivot = pd.pivot_table(dfresults, index=["Country", "City", "Peak", "ConnectionType"],
                                       values=["Download"],
                                       aggfunc=['count', 'sum', 'mean', 'median'])
                print(pivot)
                pivot.to_csv(PIVOT_FILE)


if __name__ == "__main__":
    main()

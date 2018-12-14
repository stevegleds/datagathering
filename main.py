from dataprocessing import addextradata
import pandas as pd


CSV_FILE = 'mesample.csv'  # this is the raw data
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
        1 Parse Source File
        2 Create Pivot table Country > City > Peak > Type
        ''')
        ans = int(input('What do you want?'))
        if ans == 1:  # do it all in pandas:
            print("Use the following files?")
            print('Data file used is: ', CSV_FILE)
            print('Output file used is:', OUTPUT_FILE)
            response = input("Y to continue; any other key to abort /n" )
            if not response.lower():
                pass
            dfcountry = pd.read_csv(CONSTANTS_FILE)
            dfresults = pd.read_csv(CSV_FILE)
            dfresults = addextradata(dfresults, dfcountry)
            print(dfresults[['Date Time', 'Country', 'Hour', 'City', 'Peak']])
            try:
                dfresults.to_csv(OUTPUT_FILE)
            except:
                print(OUTPUT_FILE, "is open")
            outputfilecreated = True
        if ans == 2:
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

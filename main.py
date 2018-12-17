from dataprocessing import addextradata, addcountrycodedata
from parserawdata import get3lettercountrycodes
import pandas as pd


CSV_FILE = 'logdata.csv'  # this is the raw data
EXCEL_FILE = 'mesample.xlsx'
#  EXCEL_FILE = 'me20181127-01.xlsx'
OUTPUT_FILE = 'output.csv'  # this is the raw data with fields for city and peak time info
CONSTANTS_FILE = 'meconstants.csv'  # contains data about city radiius etc.
PIVOT_FILE = 'pivotresults.csv'  # contains summary results
MYDSP_LOG_FILE = "html5test.2018-12-13-21.log"  # needed to get correct country codes (3 letters)
COUNTRY_CODE_FILE = "countrycode.csv"

print('Data file used is: ', CSV_FILE)
print('Output file used is:', OUTPUT_FILE)


def main():
    outputfilecreated = False
    dfcountry = pd.read_csv(CONSTANTS_FILE)
    dfresults = pd.read_csv(CSV_FILE)
    dfresults["Timestamp"] = pd.to_numeric(dfresults["Timestamp"])
    ans = True
    while ans:
        print('''
        1 Parse log file to get country codes from mydsp
        2 Parse Source File
        3 Create Pivot table Country > City > Peak > Type
        
        ''')
        ans = int(input('What do you want?'))
        if ans == 1:
                dfcountrycodes = get3lettercountrycodes(MYDSP_LOG_FILE)
                print('Raw country codes are: ', dfcountrycodes)
                print('First few results before country codes', dfresults.head())
                dfcountrycodes.to_csv(COUNTRY_CODE_FILE)

                dfresults = addcountrycodedata(dfresults, dfcountrycodes)

        if ans == 2:  # do it all in pandas:
            print("Use the following files?")
            print('Data file used is: ', CSV_FILE)
            print('Output file used is:', OUTPUT_FILE)
            response = input("Y to continue; any other key to abort /n" )
            if not response.lower():
                pass
            dfresults = addextradata(dfresults, dfcountry)
            print(dfresults[['Date Time', 'Country', 'Hour', 'City', 'Peak']])
            try:
                dfresults.to_csv(OUTPUT_FILE)
            except:
                print(OUTPUT_FILE, "is open")
            outputfilecreated = True
        if ans == 3:
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

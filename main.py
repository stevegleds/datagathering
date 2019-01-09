from dataprocessing import addextradata, addcountrycodedata, filterbycountry
from parserawdata import get3lettercountrycodes, getageoffile
import pandas as pd


CSV_FILE = '12-31copy.csv'  # this is the raw data
EXCEL_FILE = 'bahrain20190109.xlsx'
#  EXCEL_FILE = 'me20181127-01.xlsx'
OUTPUT_FILE = 'outputnew.csv'  # this is the raw data with fields for city and peak time info
CONSTANTS_FILE = 'meconstants.csv'  # contains data about city radii etc.
DISTRICTS_FILE = 'districts.csv'  # lookup table of latitude to Bahrain districts
PIVOT_FILE = 'pivotresults.csv'  # contains summary results
MYDSP_LOG_FILE = "12-12.log"  # needed to get correct country codes (3 letters)
COUNTRY_CODE_FILE = "countrycode.csv"
#  countrycodeset is used to filter out unneeded countries
countrycodeset = {"SAU", "ARE", "JOR", "ISR", "KWT", "OMN", "TUR", "QAT", "EGY", "BHR"}


def main():
    outputfilecreated = False
    print("Creating dataframes from local files")
    dfcountry = pd.read_csv(CONSTANTS_FILE)
    dfresults = pd.read_excel(EXCEL_FILE, encoding="ISO-8859-1")
    dfdistricts = pd.read_csv(DISTRICTS_FILE)
    print("Dataframes Created")
    print("dfresults datatypes\n", dfresults.dtypes)
    dfresults['Timestamp'] = dfresults['Timestamp'][1:]
    # dfresults['Timestamp'].astype(str).astype(int)
    dfresults['Timestamp'] = pd.to_numeric(dfresults['Timestamp'], errors='coerce')
    #  print('Main df datatypes: /n', dfresults.dtypes)
    print('Data file used is: ', EXCEL_FILE, 'modified on :', getageoffile(EXCEL_FILE))
    print('Output file used is:', OUTPUT_FILE)
    ans = True
    while ans:
        print('''
        1 Parse log file to get country codes from mydsp (obsolete)
        2 Parse Source File 
        3 Create Pivot table Country > City > Peak > Type
        
        ''')
        try:
            ans = int(input('What do you want? \n'))
        except:
            print('Please choose a number')
        if ans == 1:
            response = input("Are you sure? This is no longer required. Type YES to continue \n")
            if not response.lower() == 'YES':
                pass
            else:
                dfcountrycodes = get3lettercountrycodes(countrycodeset)
                print('Raw country codes are: ', dfcountrycodes)
                print('First few results before country codes', dfresults.head())
                dfcountrycodes.to_csv(COUNTRY_CODE_FILE)
                dfresults = addcountrycodedata(dfresults, dfcountrycodes)

        if ans == 2:  # do it all in pandas:
            print("Use the following files?")
            print('Data file used is: ', EXCEL_FILE)
            print('Output file used is:', OUTPUT_FILE)
            response = input("Y to continue; any other key to abort \n")
            if not response.lower() == 'y':
                pass
            print('Adding new data to data file - Country, City, Peak and District information.')
            dfresults = addextradata(dfresults, dfcountry, dfdistricts)
            print("Countries to filter by: \n")
            print("1 All Countries")
            print("2 ME Countries: ", countrycodeset)
            print("3 Bahrain")
            print("4 Enter Three Letter Country Code")
            filterresponse = ""
            allowedresponses = ["1", "2", "3", "4"]
            while filterresponse not in allowedresponses:
                filterresponse = input("Choose one of these options \n")
                if filterresponse.lower() == '1':
                    print("Producing results for all countries")
                if filterresponse.lower() == '2':
                    dfresults = filterbycountry(dfresults, countrycodeset)
                if filterresponse.lower() == '3':
                    dfresults = filterbycountry(dfresults, ["BHR", "BH"])
                if filterresponse.lower() == '4':
                    print("This option not available yet. You should see all results.")  # todo write code to allow choice
            try:
                dfresults.to_csv(OUTPUT_FILE)
            except:
                print(OUTPUT_FILE, "************ The output file is open. Close it and start again.  ************")
            outputfilecreated = True
        if ans == 3:
            if not outputfilecreated:
                print("Please process raw data file before analysing. Option 7.")
            else:
                print(dfresults.head())
                pivot = pd.pivot_table(dfresults, index=["CountryCode", "City", "Peak", "ConnectionType", "ISP"],
                                       values=["Download"],
                                       aggfunc=['count', 'sum', 'mean', 'median'])
                pivotisp = pd.pivot_table(dfresults, index=["ISP"],
                                       values=["Download", "Upload"],
                                       aggfunc=['count', 'sum', 'mean', 'median'])
                pivotlatitude = pd.pivot_table(dfresults, index=["Latitude"],
                                          values=["Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])
                pivotmunicipality = pd.pivot_table(dfresults, index=["Municipality"],
                                          values=["Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])
                pivotdistrict = pd.pivot_table(dfresults, index=["District"],
                                          values=["Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])
                pivotpeak = pd.pivot_table(dfresults, index=["Peak"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                pivotcity = pd.pivot_table(dfresults, index=["City"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                pivot.to_csv(PIVOT_FILE)
                pivotisp.to_csv("pivotisp.csv")
                pivotlatitude.to_csv('pivotlatitude.csv')
                pivotdistrict.to_csv('pivotdistrict.csv')
                pivotmunicipality.to_csv('pivotmunicipality.csv')
                pivotpeak.to_csv('pivotpeak.csv')
                pivotcity.to_csv('pivotcity.csv')


if __name__ == "__main__":
    main()

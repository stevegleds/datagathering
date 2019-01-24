from dataprocessing import addextradata, addcountrycodedata, filterbycountry
from parserawdata import get3lettercountrycodes, getageoffile
import pandas as pd
import os

#  Data Folders and Files
data_dir = os.getcwd()+'\\data'
data_sources = data_dir+'\\datasources'
data_input = data_dir+'\\input'
data_output = data_dir+'\\output'
#  Data Sources
CSV_FILE = data_input+'\\12-31copy.csv'  # this is the raw data
EXCEL_FILE = data_input+'\\20190115.xlsx'
CONSTANTS_FILE = data_sources+'\\meconstants.csv'  # contains data about city radii etc.
DISTRICTS_FILE = data_sources+'\\districts.csv'  # lookup table of latitude to Bahrain districts
#  MYDSP_LOG_FILE = data_sources+'\\12-12.log"  # needed to get correct country codes (3 letters)
COUNTRY_CODE_FILE = data_sources+'\\countrycode.csv'
#  countrycodeset is used to filter out unneeded countries. Comment out 2 or 3 letter version as needed
#  countrycodeset = {"SAU", "ARE", "JOR", "ISR", "KWT", "OMN", "TUR", "QAT", "EGY", "BHR"}
countrycodeset = {"AE", "BH", "EG", "IL", "IR", "JO", "KW", "LB", "OM", "QA", "SA", "TR"}

#  Data Output
PIVOT_FILE = data_output+'\\pivot_results.csv'  # contains summary results
PIVOT_ISP_FILE = data_output+'\\pivot_isp.csv'  # contains summary results
PIVOT_GEO_FILE = data_output+'\\pivot_geo.csv'  # contains summary results
PIVOT_PEAK_FILE = data_output+'\\pivot_peak.csv'  # contains summary results
PIVOT_CITY_FILE = data_output+'\\pivot_city.csv'  # contains summary results
# PIVOT_DISTRICT_FILE = data_output+'\\pivot_district.csv'  # contains summary results
# PIVOT_MUNICIPALITY_FILE = data_output+'\\pivot_municipality.csv'  # contains summary results


def main():
    outputfilecreated = False
    output_file = data_output + '\\output.csv'  # this is the raw data with fields for city and peak time info
    print(output_file)
    print("Creating dataframes from local files")
    dfcountry = pd.read_csv(CONSTANTS_FILE)
    dfresults = pd.read_excel(EXCEL_FILE, encoding="ISO-8859-1")
    #  dfdistricts = pd.read_csv(DISTRICTS_FILE)
    print("Dataframes Created")
    print("dfresults datatypes\n", dfresults.dtypes)
    dfresults['Timestamp'] = pd.to_numeric(dfresults['Timestamp'], errors='coerce')
    #  print('Main df datatypes: /n', dfresults.dtypes)
    print('Data file used is: ', EXCEL_FILE, 'modified on :', getageoffile(EXCEL_FILE))
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
            response = input("Y to continue; any other key to abort \n")
            if not response.lower() == 'y':
                pass
            print('Adding new data to data file - Country, City, Peak and District information.')
            # use this instead of next if dfdistricts needed
            # dfresults = addextradata(dfresults, dfcountry, dfdistricts)
            dfresults = addextradata(dfresults, dfcountry)  # dfdistricts not needed
            print("Countries to filter by: \n")
            print("1 All Countries")
            print("2 ME Countries: ", countrycodeset)
            print("3 Bahrain")
            print("4 Enter Two Letter Country Code")
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
            file_suffix = input("Enter text to add to end of output file name")
            output_file = output_file[:-4] + "_" + file_suffix + ".csv"
            print("Output file is going to be: ", output_file)
            try:
                dfresults.to_csv(output_file)
                print("Your results have been saved in:", output_file)
            except:
                print(output_file, "************ The output file is open. Close it and start again.  ************")
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
                pivotgeo = pd.pivot_table(dfresults, index=["Latitude"],
                                          values=["Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])

                pivotpeak = pd.pivot_table(dfresults, index=["CountryCode", "Peak"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                pivotcity = pd.pivot_table(dfresults, index=["City"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                # comment out next 2 lines if needed for districts
                # pivotmunicipality = pd.pivot_table(dfresults, index=["Municipality"],
                #                           values=["Download", "Upload"],
                #                           aggfunc=['count', 'sum', 'mean', 'median'])
                # pivotdistrict = pd.pivot_table(dfresults, index=["District"],
                #                           values=["Download", "Upload"],
                #                           aggfunc=['count', 'sum', 'mean', 'median'])
                file_suffix = input("Enter text to add to end of pivot file names")
                pivot.to_csv(PIVOT_FILE[:-4] + "_" + file_suffix + ".csv")
                print("Pivot results file is going to be: ", PIVOT_FILE[:-4] + "_" + file_suffix + ".csv")
                pivotisp.to_csv(PIVOT_ISP_FILE[:-4] + "_" + file_suffix + ".csv")
                pivotgeo.to_csv(PIVOT_GEO_FILE[:-4] + "_" + file_suffix + ".csv")
                pivotpeak.to_csv(PIVOT_PEAK_FILE[:-4] + "_" + file_suffix + ".csv")
                pivotcity.to_csv(PIVOT_CITY_FILE[:-4] + "_" + file_suffix + ".csv")
                print("Your Pivot files are created and stored in the Data/Output folder.")


if __name__ == "__main__":
    main()

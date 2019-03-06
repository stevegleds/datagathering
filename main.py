from dataprocessing import addextradata, filterbycountry
from parserawdata import getageoffile
import pandas as pd
import os

"""
This script takes raw speed test data from .xlsx files and adds information about the country (peak times, 
geographical information about its capital). It uses this to create a csv file that contains the added information.
Optionally it creates pivot tables that include median values (something that isn't one of the options in Excel pivots).
An option is available to merge the source data with historic myDSP data if needed. 
Finally there is an option to filter by country or countries.
"""

#  Data Folders and Files
data_dir = os.getcwd()+'\\data'
data_sources = data_dir+'\\datasources'
data_input = data_dir+'\\input'
data_output = data_dir+'\\output'

#  Data Sources

CSV_FILE = data_input+'\\dailymail.csv'  # this is the raw data
EXCEL_FILE = data_input+'\\dailymail.xlsx'
CONSTANTS_FILE = data_sources+'\\constants.csv'  # contains data about city radii etc.
DISTRICTS_FILE = data_sources+'\\districts.csv'  # lookup table of latitude to Bahrain districts
MYDSP_FILE = data_input+'\\mydsp_nov2018_jan2019.xlsx'
COUNTRY_CODE_FILE = data_sources+'\\countrycode.csv'
POPSERVER_FILE = data_sources+'\\popservers.csv'
#  countrycodeset is used to filter out unneeded countries. Comment out 2 or 3 letter version as needed
#  There are 2 and 3 letter codes needed for processing mydsp data. Mediasmart only used 2 letter codes
mecountrycodeset = ["AE", "BH", "EG", "IL", "IR", "JO", "KW", "LB", "OM", "QA", "SA", "TR",
                    "ARE", "BHR", "EGY", "ISR", "IRN", "JOR", "KWT", "LBN", "OMN", "QAT", "SAU", "TUR"]
choicesmade = []
#  Data Output
PIVOT_FILE = data_output+'\\pivot_results.csv'  # contains summary results
PIVOT_ISP_FILE = data_output+'\\pivot_isp.csv'  # contains isp results
PIVOT_GEO_FILE = data_output+'\\pivot_geo.csv'  # contains geo results
PIVOT_PEAK_FILE = data_output+'\\pivot_peak.csv'  # contains peak time results
PIVOT_CITY_FILE = data_output+'\\pivot_city.csv'  # contains city results
print('file names and constants have been defined')


def main():
    outputfilecreated = False
    ans = True
    while ans:
        menu = (
            f"1 Use An Existing Data File That I Will Specify \n"
            f"2 Create New Data file including Country Info file from constants file \n and Parse Raw File {EXCEL_FILE}\n" 
            f"3 Create Pivot table Country > City > Peak > Type\n"
        )
        print(menu)
        print("Previous actions: ", choicesmade)
        try:
            ans = int(input('What do you want? \n'))
        except:
            print('Please choose a number')
        if ans == 1:
            outputfilecreated = True
            outputfilenameok = False
            while not outputfilenameok:
                try:
                    output_file = data_output + '\\' + input("Existing csv file name e.g. 'output_20190129' with no ext: ") + ".csv"
                    dfresults = pd.read_csv(output_file, encoding="ISO-8859-1")
                    print(dfresults.head())
                    outputfilenameok = True
                except:
                    pass
        if ans == 2:
            output_file = data_output + '\\output.csv'  # this is the raw data with fields for city and peak time info
            dailymail = input('If this is for DailyMail enter street code or else enter nothing \n '
                              'choices are KPG, IPL, CGD, MRD, TBS, CRT, CMP, FWY, GCC, AST\n')
            if dailymail:
                print("Producing results for street code", dailymail, ". Results going to : ", output_file)
                output_file = data_output + '\\dailymail\\' + dailymail + '_output.csv'
                print(output_file)
                CONSTANTS_FILE = data_sources+'\\' + dailymail + 'constants.csv'
            else:
                CONSTANTS_FILE = data_sources + '\\meconstants.csv'
            print("Creating new data file: ", output_file, "from the raw input file ", EXCEL_FILE)
            print("Creating dataframes from local files")
            print("        Creating country information dataframe")
            dfcountry = pd.read_csv(CONSTANTS_FILE)
            print("        ... Done")
            print("Creating POP Server dataframe")
            dfpopserver = pd.read_csv(POPSERVER_FILE)
            print("        ... Done")
            print("        Creating results dataframe")
            dfresults = pd.read_excel(EXCEL_FILE, encoding="ISO-8859-1")
            print("        ... Done")
            print("Dataframes Created")
            print("Converting timestamp field to numeric to ensure good date time data")
            dfresults['Timestamp'] = pd.to_numeric(dfresults['Timestamp'], errors='coerce')
            print("        ... Done")
            print("Creating POP3 column that contains only one POP server id to allow lookup to work ")
            dfresults['POP Unique'] = [x[:3] for x in dfresults['POP']]
            print("        ... Done")
            print('Data file used is: ', EXCEL_FILE, 'modified on :', getageoffile(EXCEL_FILE))

            print("Use the following files?")
            print('Data file used is: ', EXCEL_FILE)
            response = input("Y to continue; any other key to abort \n")
            if not response.lower() == 'y':
                pass  #TODO this is pointless because the next section is still completed
            print('Adding new data to data file - Country, City, Peak, POP and District information.')
            dfresults = addextradata(dfresults, dfcountry, dfpopserver)
            print("Countries to filter by: \n")
            print("1 All Countries")
            print("2 ME Countries: ", mecountrycodeset)
            print("3 Bahrain")
            print("4 Enter Two Letter Country Code {not available yet")
            filterresponse = ""
            allowedresponses = ["1", "2", "3", "4"]
            while filterresponse not in allowedresponses:
                filterresponse = input("Choose one of these options \n")
                if filterresponse.lower() == '1':
                    print("Producing results for all countries")
                    choicesmade.append("Data File created for all countries")
                if filterresponse.lower() == '2':
                    dfresults = filterbycountry(dfresults, mecountrycodeset)
                    choicesmade.append("Data File created for Middle East Countries")
                if filterresponse.lower() == '3':
                    dfresults = filterbycountry(dfresults, ["BHR", "BH"])
                    choicesmade.append("Data File created for Bahrain only")
                if filterresponse.lower() == '4':
                    print("This option not available yet. You should see all results.")  # todo write code to allow choice
                    choicesmade.append("Data File created for all countries")
            if dailymail:
                file_suffix = dailymail
                dfresults['Street Code'] = [dailymail if x is True else 'Ignore' for x in dfresults['City']]
            else:
                file_suffix = input("Enter text to add to end of output file name")
            output_file = output_file[:-4] + "_" + file_suffix + ".csv"
            print("Output file is going to be: ", output_file)
            try:
                print("Saving output csv file")
                dfresults.to_csv(output_file)
                print("Your results have been saved in:", output_file)
            except:
                print("************ The output file is open. Close it and start again.  ************")
            outputfilecreated = True
        if ans == 3:
            if not outputfilecreated:
                print("Please process raw data file before analysing. "
                      "Option 1 to use existing output csv file or 2 to process again.")
            else:
                print(dfresults.head())
                pivot = pd.pivot_table(dfresults, index=["Country Name", "City", "Peak", "ConnectionType", "ISP"],
                                       values=["Download", "Upload"],
                                       aggfunc=['count', 'sum', 'mean', 'median'],)
                pivotisp = pd.pivot_table(dfresults, index=["Country Name", "ISP"],
                                          values=["Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])
                pivotgeo = pd.pivot_table(dfresults, index=["Country Name", "Latitude"],
                                          values=["Longitude", "Download", "Upload"],
                                          aggfunc=['count', 'sum', 'mean', 'median'])
                pivotpeak = pd.pivot_table(dfresults, index=["Country Name", "Peak"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                pivotcity = pd.pivot_table(dfresults, index=["Country Name", "City"],
                                               values=["Download", "Upload"],
                                               aggfunc=['count', 'sum', 'mean', 'median'])
                print(file_suffix)
                samesuffix = input("Use previous suffix? Y/y")
                if samesuffix.lower() == "y":
                    pass
                else:
                    file_suffix = input("Enter text to add to end of pivot file names\n")
                print("Pivot results csv file is going to be: ", PIVOT_FILE[:-4] + "_" + file_suffix + ".csv")
                pivot.to_csv(PIVOT_FILE[:-4] + "_" + file_suffix + ".csv", index=True)
                pivotisp.to_csv(PIVOT_ISP_FILE[:-4] + "_" + file_suffix + ".csv", index=True)
                pivotgeo.to_csv(PIVOT_GEO_FILE[:-4] + "_" + file_suffix + ".csv", index=True)
                pivotpeak.to_csv(PIVOT_PEAK_FILE[:-4] + "_" + file_suffix + ".csv", index=True)
                pivotcity.to_csv(PIVOT_CITY_FILE[:-4] + "_" + file_suffix + ".csv", index=True)
                print("Your Pivot csv files are created and stored in the Data/Output folder.")
                print("Pivot results excel file is going to be: ", PIVOT_FILE[:-4] + "_" + file_suffix + ".csv")
                choicesmade.append("Pivot csv files created with a suffix of " + file_suffix)


if __name__ == "__main__":
    main()

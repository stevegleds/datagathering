import pandas as pd
import os
"""A test file to work on linking results to cities based on lat/long of result and lat/long and radius of city 
"""

#  Data Folders and Files
data_dir = os.getcwd()+'\\data'
data_sources = data_dir+'\\datasources'
data_input = data_dir+'\\input'
data_output = data_dir+'\\output'

#  Data Sources

# CSV_FILE = data_input+'\\dailymail.csv'  # this is the raw data
EXCEL_FILE = data_input+'\\dailymail.xlsx'
CONSTANTS_FILE = data_sources+'\\meconstants.csv'  # contains data about city radii etc.
DISTRICTS_FILE = data_sources+'\\districts.csv'  # lookup table of latitude to Bahrain districts
MYDSP_FILE = data_input+'\\mydsp_nov2018_jan2019.xlsx'
COUNTRY_CODE_FILE = data_sources+'\\countrycode.csv'
POPSERVER_FILE = data_sources+'\\popservers.csv'
PROVIDERS_FILE = data_sources+'\\providers.xlsx'

columns_list = ['POP Unique', 'Download', 'Upload', 'Latency', 'ISP',  'ISP2', 'Providers', 'Country Name',
                'MNO Country', 'MNO', 'Owner', 'Group?', 'Rank', 'Timestamp', 'Date Time', 'Latitude', 'Longitude',
                'ConnectionType', 'DeviceID',
                'AppID', 'ExchangeName', 'CountryCode', 'IP', 'IPAddress', 'AppBundle', 'AppName', 'ModelName',
                'ModelName2', 'Count', 'DownloadCount', 'UploadCount', 'POP', 'Capital',
                'Country Code 2', 'Country Code 3', 'CityLat', 'CityLong', 'Latitude-Length', 'Longitude-Length',
                'Radius', 'Peak-Start-GMT', 'Peak-End-GMT', 'POP Lookup', 'POP City', 'POP Country', 'POP Continent',
                'Distance', 'City', 'TOD', 'AM', 'PM', 'Peak', 'Hour', 'Peak End', 'Peak Start', 'ServerIP',
                'ServerCountry']

def addextradata(dfresults, dfcountry):
    """for each result in dfresults finds closest city in dfcountry
    
    Arguments:
        dfresults {dataframe} -- source results
        dfcountry {dataframe} -- lookup table of cities with lat/long radius
    return: dfresults with added column showing name and country of nearest city
    """
    pass

def main():
    dailymail = "KPG"
    output_file = data_output + '\\output.csv'  # this is the raw data with fields for city and peak time info
    print("Producing results for street code", dailymail, ". Results going to : ", output_file)
    output_file = data_output + '\\dailymail\\' + dailymail + '_output.csv'
    print(output_file)
    CONSTANTS_FILE = data_sources+'\\' + dailymail + 'constants.csv'
    print("Creating new data file: ...", output_file[-20:], "from the raw input file ... ", EXCEL_FILE[-20:])
    print("Creating dataframes from local files")
    print("        Creating country information dataframe")
    dfcountry = pd.read_csv(CONSTANTS_FILE)
    print("        ... Done")
    print("Creating results dataframe")
    dfresults = pd.read_excel(EXCEL_FILE, encoding="ISO-8859-1")
    print("        ... Done")
    print("Dataframes Created")
    print('Data file used is: ', EXCEL_FILE)
    print('Adding new data to data file - ')
    dfresults = addextradata(dfresults, dfcountry)
    file_suffix = dailymail
    dfresults['Street Code'] = [dailymail if x is True else 'Ignore' for x in dfresults['City']]
    file_suffix = input("Enter text to add to end of output file name \n")
    output_file = output_file[:-4] + "_" + file_suffix + ".csv"
    print("Output file is going to be: ", output_file)
    dfresults = dfresults[columns_list]
    dfresults.index.name = "ID"
    try:
        print("Saving output csv file")
        dfresults.to_csv(output_file)
        print("Your results have been saved in:", output_file)
    except:
        print("************ The output file is open. Close it and start again.  ************")
    

if __name__ == "__main__":
    main()

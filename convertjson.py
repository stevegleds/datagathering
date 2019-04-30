import pandas as pd
import os
import glob
from pathlib import Path
'''
Usage
Converts json to csv
This is done with unpack() which takes a dataframe and a column to unpack
Need to change subpath for each folder. Can't work in one folder because filenames are same and data needs to be merged.
Individual csv files are created for each json file
Finally, all csv files are combined to one csv with the name of the folder (as given in subpath)
'''
# Check we are in the correct directory
print(os.getcwd())
subpath = "/testresults-20190430000000"  # To be used so we only need to change directory in one place
csvfilename = subpath[1:] + ".csv"
path = "S:/pythoncode/myprojects/work/datagathering/data/json/20190430/source" + subpath
os.chdir(path)
print(os.getcwd())
cf_hit_text = "CF-Cache-Status: HIT"
cf_ray_text = "CF-RAY"


#  Unpack dictionary elements and add one column for each dictionary field.
def unpack(df, column, fillna=None):
    ret = None
    if fillna is None:
        tmp = pd.DataFrame((d for idx, d in df[column].iteritems()))
        ret = pd.concat([df.drop(column, axis=1), tmp], axis=1)
    else:
        tmp = pd.DataFrame((d for idx, d in df[column].iteritems())).fillna(fillna)
        ret = pd.concat([df.drop(column, axis=1), tmp], axis=1)
    return ret


# filename is the json file and this process converts json to dataframe and then exports to csv
# We need to 'unpack' some fields that contain dictionaries of data to produce column data
def jsontocsv(filename):
    df = pd.read_json(filename, lines=True)
    df = unpack(df, 'HttpTestResults', 0)
    df = unpack(df, 0, 0)
    df = unpack(df, 'ResponseStatus', 0)
    df = unpack(df, 'ProbeInfo', 0)
    # df = unpack(df, 'TestStatus', 0)
    cols = df.columns.tolist()
    # create list of extra data columns that will store additional data
    new_cols = ['JobID', 'Datacentre', 'Throughput', 'CF_HIT', 'CF_RAY']
    cols = new_cols + cols
    print(cols)
    # convert DownloadBytes to our usual measure of Mb/s
    df['Throughput'] = (df['DownloadedBytes'] * 8) / (df['TotalTime'] / 1000) / 1000000
    # JobID column stores the name of the Job so that we know which job the data came from
    df['JobID'] = jobID
    #  Creates user-friendly title for Data Centre e.g. CloudFlare instead of the long url
    df = df.apply(add_datacentre, axis=1)
    #  Parse information from the header for CF_RAY and CF_HIT to help with quality of analysis
    df = df.apply(add_cf_header_info, axis=1)
    print(df.columns.tolist())
    df = df[cols]  # Creates df with only those columns in 'cols'. In this case we use all columns but change the order.
    df.to_csv(csvfile)
    return df


#  Simple function to lookup destination data nad replace with user-friendly data
def add_datacentre(df):
    if df['Destination'] == "https://kong.speedcheckerapi.com:8443/download/100mb.zip?apikey=1a2b3c4d-1975-1978-9876-9f8e7d6c5b4a":
        df['Datacentre'] = 'Cloudflare'
    elif df['Destination'] == 'http://196.251.248.78/100mb':
        df['Datacentre'] = 'Heficed'
    else:
        df['Datacentre'] = 'Other'
    return df


def add_cf_header_info(df):
    #  Note the use of str() to work with Headers object.
    #  It would be better to convert this to string - perhaps during reading the csv
    if cf_hit_text in str(df['Headers']):
        df['CF_HIT'] = "Hit"
    else:
        df['CF_HIT'] = 'Miss'
    if cf_ray_text in str(df['Headers']):
        cf_ray_location = str(df["Headers"]).find(cf_ray_text)  # where does CF_RAY start
        df['CF_RAY'] = str(df['Headers'])[cf_ray_location+25:cf_ray_location+28]
        # only need last 3 chars of CF_RAY data
    else:
        df['CF_RAY'] = 'Null'
    return df


# Go through all json files and create csv files
for filename in glob.glob(os.path.join(path, '*.json')):  # Uses glob to only use .json files
    print('Filename is: ', filename)
    jobID = Path(filename).stem  # returns the filename with no path or extension info
    print('JobID is: ', jobID)
    csvfile = jobID + '.csv'
    jsontocsv(filename)

# go through all csv files and create single csv file
all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=False)
# export to csv
combined_csv.to_csv(csvfilename, index=False, encoding='utf-8-sig')




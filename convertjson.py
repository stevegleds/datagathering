import pandas as pd
import os
import glob
from pathlib import Path

# Check we are in the correct directory
print(os.getcwd())
subpath = "/badjson"  # To be used so we only need to change directory in one place
csvfilename = subpath[1:] + ".csv"
path = "S:/pythoncode/myprojects/work/datagathering/data/json/source" + subpath
os.chdir(path)
print(os.getcwd())


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
def jsontocsv(filename):
    df = pd.read_json(filename, lines=True)
    df = unpack(df, 'HttpTestResults', 0)
    df = unpack(df, 0, 0)
    df = unpack(df, 'ResponseStatus', 0)
    df = unpack(df, 'ProbeInfo', 0)
    # df = unpack(df, 'TestStatus', 0)
    cols = df.columns.tolist()
    new_cols = ['JobID', 'Datacentre', 'Throughput']
    cols = new_cols + cols
    print(cols)
    df['Throughput'] = (df['DownloadedBytes'] * 8) / (df['TotalTime'] / 1000) / 1000000
    df['JobID'] = jobID
    df = df.apply(add_datacentre, axis=1)
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




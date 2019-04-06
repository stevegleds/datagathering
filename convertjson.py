import pandas as pd
import os

# Check we are in the correct directory
print(os.getcwd())
#  os.chdir("data/json")
os.chdir("C:/Users/steve/Desktop/work_temp/androidconfig/TestResultsJobs/testresults-20190403160000")
print(os.getcwd())
# Change json_file csvfile as required for source and destination
jobID = "08b3c438-a675-4c74-9da4-e4f604b5e934"
json_file = jobID + ".json"
csvfile = json_file + '.csv'
print('csvfile is: ', csvfile)
print('json file is: ', json_file)


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


#  Simple function to lookup destination data nad replace with user-friendly data
def add_datacentre(df):
    if df['Destination'] == "https://kong.speedcheckerapi.com:8443/download/100mb.zip?apikey=1a2b3c4d-1975-1978-9876-9f8e7d6c5b4a":
        df['Datacentre'] = 'Cloudflare'
    elif df['Destination'] == 'http://196.251.248.78/100mb':
        df['Datacentre'] = 'Heficed'
    else:
        df['Datacentre'] = 'Other'
    return df


df = pd.read_json(json_file, lines=True)
df = unpack(df, 'HttpTestResults', 0)
df = unpack(df, 0, 0)
df = unpack(df, 'ResponseStatus', 0)
df = unpack(df, 'ProbeInfo', 0)
df = unpack(df, 'TestStatus', 0)
cols = df.columns.tolist()
new_cols = ['JobID', 'Datacentre', 'Throughput']
cols = new_cols + cols
print(cols)
df['Throughput'] = (df['DownloadedBytes']*8)/(df['TotalTime']/1000)/1000000
df['JobID'] = jobID
df = df.apply(add_datacentre, axis=1)
print(df.columns.tolist())
df = df[cols]  # Creates df with only those columns in 'cols'. In this case we use all columns but change the order.
df.to_csv(csvfile)




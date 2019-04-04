import pandas as pd
import os

# Check we are in the correct directory
print(os.getcwd())
os.chdir("data/json")
print(os.getcwd())
# Change json_file csvfile as required for source and destination
jobID = "fa1ead52-6615-40f8-b157-c1bb8af3ed29"
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
df['Throughput'] = (df['DownloadedBytes']*8)/(df['TotalTime']/1000)/1000000
df['JobID'] = jobID
df = df.apply(add_datacentre, axis=1)
#  cols contains list of column headers in order required for final csv. Use df.columns.tolist() to get latest list
cols = ['JobID', 'Datacentre', 'Throughput', 'CityName', 'ConnectionType', 'CountryCode', 'CountryName', 'TestDateTime',
        'DownloadedBytes', 'TotalTime', 'ContentLength', 'Destination', 'Status', 'TimeToFirstByte', 'StatusCode',
        'StatusText', 'ASN', 'AdvertisedSpeed', 'DNSResolver', 'GeolocationAccuracy', 'IPAddress', 'Latitude',
        'Longitude', 'Network', 'NetworkID', 'Platform', 'ProbeID', 'Screensize', 'Version', 'StatusCode', 'StatusText']
df = df[cols]  # Creates df with only those columns in 'cols'. In this case we use all columns but change the order.
df.to_csv(csvfile)




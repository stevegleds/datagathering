import pandas as pd


def get3lettercountrycodes(filename):
    values = []
    with open(filename, "r") as read_file:
        for line in read_file:
            timestamploc = line.find("timestamp")
            time = line[timestamploc + 10: timestamploc + 23]
            countryloc = line.find("&country=")
            country = line[countryloc + 9: countryloc + 12]
            # print(time, country)
            if time.isdigit():
                values.append([time, country])
    df = pd.DataFrame.from_records(values, columns=['Raw Timestamp', "Raw countrycode"])
    print(df)
    print('Timestamps only: \n', df[['Raw Timestamp']])
    print('duplicates:', df.columns.get_duplicates())
    df['Raw Timestamp'] = pd.to_numeric(df['Raw Timestamp'])
    return df

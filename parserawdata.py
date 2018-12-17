import pandas as pd


def get3lettercountrycodes(filename):
    values = []
    with open(filename, "r") as read_file:
        for line in read_file:
            timestamploc = line.find('ts')
            time = int(line[timestamploc + 5: timestamploc + 15] + line[timestamploc + 16: timestamploc + 19])
            countryloc = line.find("&country=")
            country = line[countryloc + 9: countryloc + 12]
            # print(time, country)
            # if time.isdigit():
            values.append([time, country])
    df = pd.DataFrame.from_records(values, columns=['Raw Timestamp', "Raw Country Code"])
    print(df)
    print('Timestamps only: \n', df['Raw Timestamp'].dtype)
    print(df.dtypes)
    df['Raw Timestamp'] = pd.to_numeric(df["Raw Timestamp"])
    print(df.dtypes)
    # print('duplicates:', df.columns.idx.duplicated())
    return df
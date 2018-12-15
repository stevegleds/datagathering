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
            values.append([time, country])

    df = pd.DataFrame.from_records(values, columns=['Timestamp', "countrycode"])
    print(df)
    return df

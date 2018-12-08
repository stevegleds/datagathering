import csv


def parse(raw_file, delimiter=','):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    #  open csv file
    opened_file = open(raw_file)
    #  read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    #  csv_data object is now an iterator meaning we can get each element one at a time
    #  build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    print('fields in input file are: ', fields)
    fields[0] = 'IP'
    print('fixed fields in input file are: ', fields)

    for row in csv_data:
        if row[1] == "":  # there is no text in the field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))
            # Creates a new dict item for each row with col header as key and stores in a list
        #  city_count += 1
    # close csv file
    opened_file.close()
    return parsed_data


def save_results(raw_file, results):
    """
    :param raw_file: file to be created or updated with results
    :param results: the data to be saved to raw_file
    :return: nothing. File is saved and closed within the function
    """
    with open(raw_file, "w", newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['IP',	'Country',	'Download',	'Upload',	'Latency',	'ISP',	'Timestamp',	'Latitude',	'Longitude',
                         'ConnectionType', 'DeviceID',	'POP',	'AppID',	'ExchangeName',	'Date Time',
                         'City Distance',	'City?',	'New Distance', 'New City', 'Hour', 'New Hour', 'Peak?', 'New Peak'])
        for item in results:
            writer.writerow([item['IP'], item['Country'], item['Download'], item['Upload'], item['Latency'], item['ISP'],
                             item['Timestamp'], item['Latitude'], item['Longitude'], item['ConnectionType'],
                             item['DeviceID'], item['POP'], item['AppID'], item['ExchangeName'], item['Date Time'],
                             item['City Distance'], item['City?'], item['newDistance'],
                             item['newCity'], item['Hour'], item['newHour'], item['Peak?'], item['newPeak']])
    f.close()
    return


def main():
    # Get postcode sector data from the postcode sector csv file:
    sector_data = parse(DATA_FILE, ',')
    # Get speedtest results data from the speedtest results file:
    speedtest_results_data = parse(OUTPUT_FILE, ',')
    print('Speedtest data prepared after ', time.time() - start, 'seconds')
    sector_coordinates = get_coordinates(sector_data)
    sector_coordinates_array = np.asarray(sector_coordinates)
    constituency_coordinates = get_coordinates(constituency_data)
    constituency_coordinates_array = np.asarray(constituency_coordinates)
    print('Sector array prepared after ', time.time() - start, 'seconds')
    sectors, constituencies, results = get_closest_points(speedtest_results_data, sector_coordinates_array,
                                          sector_data, constituency_coordinates_array, constituency_data)
    save_results(UPDATED_RESULTS_FILE, results)


if __name__ == "__main__":
    main()

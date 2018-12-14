values = []
with open('html5test.2018-12-13-21.log', "r") as read_file:
    for line in read_file:
        timestamploc = line.find("timestamp")
        time = line[timestamploc + 10: timestamploc + 23]
        countryloc = line.find("&country=")
        country = line[countryloc + 9: countryloc + 12]
        print(time, country)
        values.append([time, country])
with open("lookup.csv", "w") as write_file:
    for value in values:
        read_file.write(value)
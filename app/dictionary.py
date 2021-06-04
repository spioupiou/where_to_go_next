import csv

jp_cities = {}
with open('app/database.csv', 'r') as database:
    reader = csv.reader(database)
    next(reader)
    for row in reader:
        jp_cities[row[0]] = {'lat':float(row[1]), 'lon':float(row[2]), 'pref':row[3], 'picture':row[6], 'comments':row[7]}

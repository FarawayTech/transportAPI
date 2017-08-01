import csv
import logging
from pymongo import MongoClient
import pymongo


def main_import():
    logging.info("Converting to json")
    f = open('data/line_colors.csv')
    reader = csv.reader(f)

    headers = reader.next()
    locations = {}

    for row in reader:
        line = {}
        for key, value in zip(headers, row):
            line[key] = value
        if not line:
            continue
        location_name = line['location']
        if location_name in locations:
            location = locations[location_name]
        else:
            location = line
            location['location'] = {'type': 'Point', 'coordinates': [float(location.pop('location_lon')),
                                                                     float(location.pop('location_lat'))]}
            location['lines'] = {}
            locations[location_name] = location
        location['lines'][line.pop('line_num')] = line.pop('color')

    logging.info("Importing into local MongoDB")

    client = MongoClient()
    db = client['test']
    if 'line_colors' in db.collection_names():
        db.drop_collection('line_colors')

    db.line_colors.insert(locations.values())
    logging.info("Creating indexes")
    db.line_colors.create_index([("location", pymongo.GEOSPHERE)])
    client.close()

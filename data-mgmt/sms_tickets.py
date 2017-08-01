import csv
import logging
from pymongo import MongoClient


def main_import():
    logging.info("Converting to json")
    f = open('data-mgmt/data/sms_tickets.csv', 'r')
    reader = csv.reader(f)

    headers = next(reader)
    sms_locations = {}

    for row in reader:
        location = {}
        for key, value in zip(headers, row):
            location[key] = value
        if not location:
            continue
        main_code = location['main_code']
        if main_code in sms_locations:
            sms_location = sms_locations[main_code]
        else:
            location['localities'] = []
            sms_location = location
            sms_locations[main_code] = sms_location
        sms_location['localities'].append({'name': location.pop('locality'), 'zone': location.pop('zone')})

    logging.info("Importing into local MongoDB")
    client = MongoClient()
    db = client['test']
    if 'sms_tickets' in db.collection_names():
        db.drop_collection('sms_tickets')

    db.sms_tickets.insert(sms_locations.values())
    logging.info("Creating indexes")
    db.sms_tickets.create_index('localities.name')
    client.close()

import csv
import os
import subprocess
import re
import unicodedata
import logging

import itertools
from metaphone import doublemetaphone
from pymongo import MongoClient
import pymongo


def strip_accents(s):
    s = s.decode('utf-8')
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


REPLACE_PUNCT = re.compile(r'[.()/,\-&]')
STATION_NAMES = ['stop_name', 'ch_station_long_name', 'ch_station_synonym1', 'ch_station_synonym2',
                 'ch_station_synonym3', 'ch_station_synonym4']
STATION_COL_NAME = 'stations'


def main_import():
    client = MongoClient()
    db = client['temp']
    prev_count = db[STATION_COL_NAME].count()

    print("Downloading stops file...", end="\t")
    subprocess.call(["curl http://gtfs.geops.ch/dl/complete/stops.txt > stops.csv"], shell=True)
    print("[OK]")
    current_count = sum(1 for _ in open("stops.csv"))
    if current_count + 10 < prev_count:
        logging.error("New file contains %d stations less than the old one, aborting\t[FAIL]" % (prev_count - current_count))
    subprocess.call(["cat stops.csv | sort -r -k1,1 -t',' > stops_sorted.csv"], shell=True)

    logging.info("Converting to json")
    f = open('stops_sorted.csv')
    reader = csv.reader(f)

    headers = reader.next()
    stations = []
    station_ids = set()

    for row in reader:
        station = {'weight': 0}
        for key, value in zip(headers, row):
            if key == 'stop_id':
                value = value.split(':')[0]
            station[key] = value
        if station['stop_id'] in station_ids:
            stations[-1]['weight'] += 1
            continue
        station_ids.add(station['stop_id'])
        station['location'] = {'type': 'Point',
                               'coordinates': [float(station.pop('stop_lon')), float(station.pop('stop_lat'))]}

        # synonyms, used in weighted matching
        station['synonyms'] = [station[syn_attr_name] for syn_attr_name in STATION_NAMES if station[syn_attr_name]]
        station['metaphones'] = [s for s in set(itertools.chain(*(doublemetaphone(s) for s in station['synonyms'])))
                                 if s != '']

        def recursive_prefixes(prefix_set, sequence):
            for i in range(1, len(sequence)):
                # if space - recurse
                if sequence[i] == ' ':
                    recursive_prefixes(prefix_set, sequence[i + 1:])
                else:
                    prefix_set.add(sequence[:i].strip())
            prefix_set.add(sequence)

        # create text field for station names
        normal_names = set()
        for station_attr in STATION_NAMES:
            normal_name = ' '.join(REPLACE_PUNCT.sub(' ', strip_accents(station.pop(station_attr))).split()).lower()
            if normal_name:
                normal_names.add(normal_name)

        station['first_names'] = list(set([name[:i + 1].strip() for name in normal_names for i in range(len(name))]))

        # create text field for station name prefixes
        second_names = set()
        for normal_name in list(normal_names):
            second_name = ' '.join(normal_name.split()[1:]) or normal_name
            recursive_prefixes(second_names, second_name)

        station['second_names'] = list(second_names)

        # all name prefixes
        prefix_names = set()
        for normal_name in list(normal_names):
            for name in normal_name.split():
                for i in range(len(name)):
                    prefix_names.add(name[:i + 1])
        station['prefix_names'] = list(prefix_names)

        stations.append(station)

    logging.info("Importing into local MongoDB temp collection")
    temp_col = db['temp_stations']
    temp_col.insert(stations)
    logging.info("Creating indexes")
    temp_col.create_index([("location", pymongo.GEOSPHERE)])
    temp_col.create_index('stop_id')
    temp_col.create_index('first_names')
    temp_col.create_index('second_names')
    temp_col.create_index('prefix_names')
    temp_col.create_index('weight')
    temp_col.create_index([('metaphones', pymongo.TEXT)], default_language='none')

    logging.info('Dropping old collection and renaming')
    if STATION_COL_NAME in db.collection_names():
        db.drop_collection(STATION_COL_NAME)
    temp_col.rename(STATION_COL_NAME)
    client.close()
    os.remove("stops_sorted.csv")
    os.remove("stops.csv")

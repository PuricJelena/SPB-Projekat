import pymongo
import csv
from decimal import Decimal


class Artist:
    def __init__(self, file):
        self._file = file

    def add_artist_to_db(self, url, db_name):
        client = pymongo.MongoClient(url)
        db = client[db_name]
        artists = []
        self._artists = {}
        with open(self._file, 'r', encoding='cp850') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                artist = get_artist(row)
                artists.append(artist)
                self._artists[artist['id']] = get_artist(artist)

        db['artists'].insert_many(artists)

    def get_artists(self):
        return self._artists


def get_artist(row) -> dict:

    strin2 = str(row['genres']).strip('[]')
    if strin2 == '':
        strin3 = []
    else:
        strin3 = str(strin2).split(',')
    return {
        'id': row['id'],
        'followers': conv(row['followers']),
        'genres': strin3,
        'name': row['name'],
        'popularity': int(row['popularity'])
    }


def get_mini_artist(artist) -> dict:
    return {
        'id': artist['id'],
        'name': artist['name']
    }


def conv(s):
    try:
        s = float(s)
    except ValueError:
        pass
    return s

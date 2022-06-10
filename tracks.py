import pymongo
import csv
from collections import ChainMap
from dateutil import parser


class TrackParser:
    def __init__(self, file):
        self._file = file

    def add_track_to_db(self, url, db_name, artists):
        client = pymongo.MongoClient(url)
        db = client[db_name]
        tracks = []
        listOfArtists = []

        with open(self._file, 'r', encoding='cp850') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                listOfArtists.clear()
                listOfArtId = row['id_artists'].split(',')
                lengthIdArt = len(listOfArtId)
                a_list = []
                if lengthIdArt == 1:
                    if (row['id_artists'] in artist['id'] for artist in artists):
                        name = eval(row['id_artists'].strip('[]'))
                        try:
                            tracks.append(get_track(row, artists[name]))
                            a_list.clear()
                        except:
                            print(
                                "Error artist_id: {} not found in csv (single artists)"
                                    .format(row['id_artists'])
                            )
                if lengthIdArt > 1:
                    for oneId in listOfArtId:
                        try:
                            listOfArtists.append(artists[eval(oneId.strip('[]'))])
                        except:
                            print(
                                "Error artist_id: {} not found in csv (multiple artists)"
                                    .format(oneId)
                            )

                    tracks.append(get_track(row, listOfArtists[:]))

        if len(tracks) > 0:
            print(len(tracks))
            db['tracks'].insert_many(tracks)


def get_track(row, artist) -> dict:
    elementsOfSong = {
        'energy': float(row['energy']),
        'danceability': float(row['danceability']),
        'key': float(row['key']),
        'loudness': float(row['loudness']),
        'mode': float(row['mode']),
        'speechiness': float(row['speechiness']),
        'acousticness': float(row['acousticness']),
        'instrumentalness': float(row['instrumentalness']),
        'liveness': float(row['liveness']),
        'valence': float(row['valence']),
        'tempo': float(row['tempo']),
        'time_signature': float(row['time_signature'])
    }

    return {
        'name': row['name'],
        'popularity': float(row['popularity']),
        'duration_ms': float(row['duration_ms']),
        'explicit': float(row['explicit']),
        'release_date': parser.parse(row['release_date']),
        'elementOfSong' : elementsOfSong,
        'artists': artist
    }

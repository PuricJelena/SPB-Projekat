import pymongo
import csv
from collections import ChainMap


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
                listOfArtId = row['id_artists'].split(',')
                lengthIdArt = len(listOfArtId)
                if lengthIdArt == 1:
                    if (row['id_artists'] in artist['id'] for artist in artists):
                        name = eval(row['id_artists'].strip('[]'))
                        try:
                            listofOneArtist = artists[name].items()
                            tracks.append(get_track(row,listofOneArtist))
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
                    case_list = {}
                    for entry in listOfArtists:
                        case = {}
                        case_list[''] = case
                        
                    tracks.append(get_track(row, listOfArtists))
                    listOfArtists.clear()


        if len(tracks) > 0:
            print(len(tracks))
            db['tracks'].insert_many(tracks)


def get_track(row, artist):
    return {
        'name': row['name'],
        'artist': artist

    }

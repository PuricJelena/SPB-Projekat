from tracks import TrackParser
from artist import Artist
import os
import csv

if __name__ == '__main__':

    print("Artists!")
    artist_parser = Artist('artists.csv')
    artist_parser.add_artist_to_db(url = 'mongodb://localhost:27017/', db_name='sbp-v1')
    print("Tracks!")
    track_parser = TrackParser('tracks.csv')
    track_parser.add_track_to_db(url = 'mongodb://localhost:27017/', db_name='sbp-v1',
                                 artists = artist_parser.get_artists())

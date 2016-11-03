"""
Module for mapping lastfm xml to objects.
"""
from xml.etree import ElementTree as ET

class Session(object):
    """
    Lastfm Session
    """
    def __init__(self, name, key):
        self.name = name
        self.key = key

class Track(object):
    """
    Lastfm Tracks
    """
    def __init__(self, name, artist, url):
        self.name = name
        self.artist = artist
        self.url = url

class LastFmMapper(object):

    def __init__(self, logger):
        self.logger = logger

    def lastfm_session(self, content):
        root = ET.fromstring(content)
        status = root.get('status')
        if status == 'ok':
            session = root.find('session')
            name_elem = session.find('name')
            key_elem = session.find('key')
            return Session(name_elem.text, key_elem.text)

        return None

    def lastfm_recenttracks(self, content):
        root = ET.fromstring(content)
        recent_tracks = root.find('recenttracks')
        raw_tracks = recent_tracks.findall('track')[0:5]
        tracks = []
        for raw_track in raw_tracks:
            self.logger.info('Parsing track')
            self.logger.info(raw_track)
            name_elem = raw_track.find('name')
            artist_elem = raw_track.find('artist')
            url_elem = raw_track.find('url')
            track = Track(name_elem.text, artist_elem.text, url_elem.text)
            tracks.append(track)

        return tracks

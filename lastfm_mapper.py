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
    def __init__(self, name):
        self.name = name

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

    def lastfm_recenttracks(self, json):
        tracks = []
        self.logger.info('Raw tracks json')
        self.logger.info(json)
        for raw_track in json['track']:
            name = raw_track['name']
            track = Track(name)
            tracks.append(track)

        return tracks

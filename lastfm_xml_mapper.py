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

def lastfm_session(content):
    root = ET.fromstring(content)
    status = root.get('status')
    if status == 'ok':
        session = root.find('session')
        name_elem = session.find('name')
        key_elem = session.find('key')
        return Session(name_elem.text, key_elem.text)

    return None

def lastfm_recenttracks(content):
    root = ET.fromstring(content)
    tracks = []
    for raw_track in root.iter('track'):
        name_elem = raw_track.find('name')
        track = Track(name_elem.text)
        tracks.append(track)

    return tracks

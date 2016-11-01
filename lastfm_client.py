import requests, hashlib
import lastfm_xml_mapper as mapper
from datetime import timedelta, datetime
"""
Client methods for Last.fm API
"""

class LastFMClient(object):
    LASTFM_API_ROOT = 'http://www.last.fm/api'
    LASTFM_SCROBBLER_ROOT = 'http://ws.audioscrobbler.com/2.0/'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret


    def get_auth_url(self, callback_url):
        base_url = "{lastfm_root}/auth/?api_key={api_key}" \
            .format(lastfm_root=self.LASTFM_API_ROOT, api_key=self.api_key)

        if callback_url != None and callback_url != '':
            return "{base_url}&cb={cb}".format(base_url=base_url, cb=callback_url)

        return base_url

    def get_session(self, token):
        method = 'auth.getSession'
        payload = self.create_params(method, token)
        response = requests.get("{root}".format(root=self.LASTFM_SCROBBLER_ROOT), params=payload)
        lastfm_session = mapper.lastfm_session(response.content)
        return lastfm_session

    def get_recent_tracks(self, user):
        now = datetime.now()
        from_time = (now + timedelta(days=-5)).time()
        params = self.create_nonauth_params('user.getRecentTracks')
        params['user'] = user
        params['from'] = from_time
        response = requests.get("{root}".format(root=self.LASTFM_SCROBBLER_ROOT), params=params)
        return mapper.lastfm_recenttracks(response.content)


    def create_nonauth_params(self, method):
        return {'method': method, 'api_key': self.api_key}

    def create_params(self, method, token):
        signature = self.create_signature(method, token)
        return {'method': method, 'token': token, 'api_key': self.api_key, 'api_sig': signature}

    def create_signature(self, method, token):
        sig = "api_key{api_key}method{method}token{token}{secret}".format(api_key=self.api_key, method=method, token=token, secret=self.api_secret)
        m = hashlib.md5()
        m.update(sig)
        d = m.hexdigest()
        print d.encode('utf-8')
        return d

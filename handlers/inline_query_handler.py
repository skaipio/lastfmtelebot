import applogger, re

class InlineQueryHandler(object):

    def __init__(self, lastfm_client, telegram_botapi_client):
        self.__lastfm_client = lastfm_client
        self.__telegram_botapi_client = telegram_botapi_client

    def handle_inline_query(self, inline_query):
        m = re.search(r'what is (\S+) listening to?', inline_query.query)
        if m != None:
            username = m.group(1)
            tracks = self.__lastfm_client.get_recent_tracks(username)
            if len(tracks) > 0:
                first_track = tracks[0]
                applogger.info('Found track ' + first_track.name + ' for user ' + username)
                self.__telegram_botapi_client.answer_inline_query(inline_query.query_id, [first_track.name])

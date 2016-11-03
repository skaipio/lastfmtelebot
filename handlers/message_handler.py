import applogger, re

class MessageHandler:

    def __init__(self, lastfm_client, telegram_botapi_client):
        self.__lastfm_client = lastfm_client
        self.__telegram_botapi_client = telegram_botapi_client

    def handle_message(self, message):
        applogger.info('Handling message ' + message.id)
        if message.text == None:
            return
        m = re.search(r'/recent_tracks (\S+)', message.text) or re.search(r'^What is (\S+) listening to?', message.text)
        if m != None:
            username = m.group(1)
            tracks = self.__lastfm_client.get_recent_tracks(username)
            if len(tracks) > 0:
                first_track = tracks[0]
                applogger.info('Found track ' + first_track.name + ' for user ' + username)
                chat_id = message.chat.id
                self.__telegram_botapi_client.send_message(chat_id, \
                    username + ' is listening to ' + \
                    first_track.name + ' of artist ' + \
                    first_track.artist)

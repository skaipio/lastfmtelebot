import re

class MessageHandler:

    __track_template = "<b>{username}</b> is listening to <a href={track_url}>{track}</a> of artist <i>{artist}</i>"

    def __init__(self, logger, lastfm_client, telegram_botapi_client):
        self.__logger = logger
        self.__lastfm_client = lastfm_client
        self.__telegram_botapi_client = telegram_botapi_client

    def handle_message(self, message):
        self.__logger.info('Handling message ' + str(message.message_id))
        if message.text == None:
            self.__logger.info('No text in message ' + str(message.message_id))
            return
        m = re.search(r'/recent_tracks (\S+)', message.text) or re.search(r'^What is (\S+) listening to?', message.text)
        if m != None:
            username = m.group(1)
            tracks = self.__lastfm_client.get_recent_tracks(username)
            if len(tracks) > 0:
                first_track = tracks[0]
                self.__logger.info('Found track ' + first_track.name + ' for user ' + username)
                chat_id = message.chat.chat_id
                formatted_msg = self.__track_template.format(username=username, \
                                                             track_url=first_track.url, \
                                                             track=first_track.name, \
                                                             artist=first_track.artist)
                self.__telegram_botapi_client.send_message(chat_id, formatted_msg, 'HTML')
        else:
            self.__logger.info('Message did not match any known command')

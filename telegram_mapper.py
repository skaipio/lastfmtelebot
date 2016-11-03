class Chat(object):
    def __init__(self, chat_id, title, chat_type):
        self.chat_id = chat_id
        self.title = title
        self.chat_type = chat_type

class Message(object):
    def __init__(self, chat, text):
        self.chat = chat
        self.text = text

class InlineQuery(object):
    def __init__(self, query_id, query):
        self.query_id = query_id
        self.query = query

class TelegramMapper:

    def __init__(self, logger):
        self.logger = logger

    def __is_message(self, json):
        return json.get('message', None) != None

    def __is_inline_query(self, json):
        return json.get('inline_query', None) != None

    def __to_message(self, json):
        raw_message = json['message']
        text = raw_message.get('text', None)
        raw_chat = raw_message.get('chat', None)
        self.logger.info(raw_chat)
        chat = Chat(raw_chat['id'], raw_chat['title'], raw_chat['type']) if raw_chat != None else None
        return Message(chat, text)

    def __to_inline_query(self, json):
        inline_query = json['inline_query']
        query = inline_query['query']
        query_id = inline_query['id']
        return InlineQuery(query_id, query)

    def parse_telegram_object(self, json):
        if self.__is_message(json):
            return self.__to_message(json)
        elif self.__is_inline_query(json):
            return self.__to_inline_query(json)

        return None
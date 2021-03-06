import requests, json

class TelegramBotAPIClient(object):
    BOT_API_ROOT='https://api.telegram.org'

    def __init__(self, bot_key, bot_token, logger=None):
        self.bot_key = bot_key
        self.bot_token = bot_token
        self.logger = logger
        if self.__get_bot != None:
            webhook = self.__get_webhook_info()
            if webhook['url'] == '':
                result = self.__set_webhook()
                self.logger.info(result)

    def send_message(self, chat_id, message, parse_mode=''):
        response = self.__do_post_request('sendMessage', {'chat_id': chat_id, 'text': message, 'parse_mode': parse_mode})
        self.logger.info('Sent message. Response:')
        self.logger.info(response.status_code)
        self.logger.info(response.text)

    def answer_inline_query(self, query_id, results):
        self.logger.info('Answering query ' + str(query_id))
        response = self.__do_post_json_request('answerInlineQuery', {}, {'inline_query_id': str(query_id), 'results': results})
        self.logger.info('Response to "answer inline query"')
        self.logger.info(response.status_code)
        self.logger.info(response.text)


    def __get_bot(self):
        response = self.__do_get_request('getMe')
        json = response.json()
        if json['ok']==True:
            return json['result']
        return None

    def __get_webhook_info(self):
        response = self.__do_get_request('getWebhookInfo')
        json = response.json()
        self.logger.info('webhook info\n' + str(json))
        if json['ok']==True:
            return json['result']
        return None

    def __set_webhook(self):
        cb_url="https://lastfmtelebot.tk/{bot_token}".format(bot_token=self.bot_token)
        params ={'url': cb_url}
        webhook_url='setWebhook'
        json = self.__do_get_request(webhook_url, params).json()
        return json

    def __do_get_request(self, method, params={}):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.get(url, params)

    def __do_post_request(self, method, params):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.post(url,params=params)

    def __do_post_json_request(self, method, params, data):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.post(url,params=params, data=json.dumps(data))

    def __do_post_file_request(self, method, params, files):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.post(url,params=params,files=files)

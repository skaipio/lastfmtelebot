import requests

class TelegramBotAPIClient(object):
    BOT_API_ROOT='https://api.telegram.org'

    def __init__(self, bot_key, bot_token, logger=None):
        self.bot_key = bot_key
        self.bot_token = bot_token
        self.logger = logger
        if self.__get_bot != None:
            webhook = self.__get_webhook_info()
            if webhook['url'] == '':
                self.__set_webhook()

    def __get_bot(self):
        response = self.__do_get_request('getMe')
        json = response.json()
        if json['ok']==True:
            return json['result']
        return None

    def __get_webhook_info(self):
        response = self.__do_get_request('getWebhookInfo')
        json = response.json()
        self.logger('webhook info\n' + json)
        if json['ok']==True:
            return json['result']
        return None

    def __set_webhook(self):
        webhook_url="https://lastfmtelebot.tk/{bot_token}".format(bot_token=self.bot_token)
        json = self.__do_get_request('setWebhook', {'url': webhook_url}).json()
        if json['ok']==True:
            return json['result']
        return None

    def __do_get_request(self, method, params={}):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.get(url, params)

    def __do_post_request(self, method, params):
        url = "{root}/bot{bot_key}/{method}".format(root=self.BOT_API_ROOT, bot_key=self.bot_key, method=method)
        return requests.post(url,params=params)

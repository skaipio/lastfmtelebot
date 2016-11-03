from flask import Flask, redirect, request, session
from lastfm_client import LastFMClient
from telegram_botapi_client import TelegramBotAPIClient
from handlers import message_handler, inline_query_handler
from telegram_mapper import TelegramMapper, Message, InlineQuery
import logging

app = Flask(__name__)
app.config.from_envvar('LASTFMBOTAPI_CONFIG')

# Set up logging
logfile_path = app.config['LOGFILE']
file_handler = logging.FileHandler(logfile_path)
file_handler.setLevel(logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

session_map = {}

TELEGRAM_BOT_KEY=app.config['TELEGRAM_BOT_KEY']
TELEGRAM_BOT_TOKEN=app.config['TELEGRAM_BOT_TOKEN']
TELEGRAM_BOTAPI_CLIENT = TelegramBotAPIClient(TELEGRAM_BOT_KEY, TELEGRAM_BOT_TOKEN, app.logger)
LASTFM_CLIENT = LastFMClient(app.logger, app.config['LASTFM_API_KEY'], app.config['LASTFM_SECRET'])
__telegram_mapper = TelegramMapper(app.logger)
__message_handler = message_handler.MessageHandler(app.logger, LASTFM_CLIENT, TELEGRAM_BOTAPI_CLIENT)
__inline_query_handler = inline_query_handler.InlineQueryHandler(LASTFM_CLIENT, TELEGRAM_BOTAPI_CLIENT)

@app.route("/" + TELEGRAM_BOT_TOKEN, methods=['POST'])
def bot_query():
    json = request.json
    app.logger.info("Received a query from bot\n{}".format(json))

    telegram_obj = __telegram_mapper.parse_telegram_object(json)
    if isinstance(telegram_obj, Message):
        __message_handler.handle_message(telegram_obj)
    elif isinstance(telegram_obj, InlineQuery):
        __inline_query_handler.handle_inline_query(telegram_obj)

    return ''

@app.route("/session")
def new_session():
    token = get_token(request)
    lastfm_session = LASTFM_CLIENT.get_session(token)
    session_map[token] = lastfm_session
    session['token'] = token
    return "<h1 style='color:blue'>You're in a session {}!</h1>".format(lastfm_session.name)

@app.route("/recent_tracks")
def recent_tracks():
    user = request.args.get('lastfm_user', '')
    tracks = LASTFM_CLIENT.get_recent_tracks(user)
    track_names = '<br/>'.join([track.name for track in tracks])
    return track_names

@app.route("/lastfm")
def lastfm():
    cb = app.debug and 'http://127.0.0.1:5000/session' or None
    return redirect(LASTFM_CLIENT.get_auth_url(cb), code=302)

def get_token(req):
    return req.args.get('token', '')


if __name__ == "__main__":
    app.run(host='0.0.0.0')

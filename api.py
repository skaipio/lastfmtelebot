from flask import Flask, redirect, request, session
from lastfm_client import LastFMClient
from telegram_botapi_client import TelegramBotAPIClient
import logging

app = Flask(__name__)
app.config.from_envvar('LASTFMBOTAPI_CONFIG')

logfile_path = app.config['LOGFILE']
applogger = app.logger
file_handler = logging.FileHandler(logfile_path)
file_handler.setLevel(logging.DEBUG)
applogger.setLevel(logging.DEBUG)
applogger.addHandler(file_handler)

session_map = {}

TELEGRAM_BOT_KEY=app.config['TELEGRAM_BOT_KEY']
TELEGRAM_BOT_TOKEN=app.config['TELEGRAM_BOT_TOKEN']
TELEGRAM_BOTAPI_CLIENT = TelegramBotAPIClient(TELEGRAM_BOT_KEY, TELEGRAM_BOT_TOKEN)
LASTFM_CLIENT = LastFMClient(app.config['LASTFM_API_KEY'], app.config['LASTFM_SECRET'])

@app.route("/")
def bot_query():
    token = get_token(request)
    if token == TELEGRAM_BOT_TOKEN:
        applogger.info("Received a query from bot\n{}\n{}".format(request.content, request.args))
        print request.content

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

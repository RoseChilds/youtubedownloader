from flask import Flask, request, session, redirect, send_from_directory, send_file
from waitress import serve
from werkzeug.datastructures import ImmutableMultiDict
import requests
import random
import smtplib, ssl
import string
import re
import base64
import json
from datetime import timedelta
import requests
import youtube_dl
import sys
if (sys.version_info>=(3, 0, 0,)):
    from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
else:
    from urlparse import urlparse, parse_qs, urlunparse
    from urllib import urlencode

def withcommas(number):
    return ("{:,}".format(int(number)))

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase+"0123456789"+"""£$%^&*"""
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__, static_url_path='', static_folder='')
app.secret_key = "CHANGE_THIS"

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=2)

@app.route("/403")
def err403():
    return open("403.html", "r").read()

@app.route("/getvideo", methods=["post"])
def getvideo():
    if request.method != "POST":
        return ""
    mp4={"720":[398, 236], "480":[397, 135, 134], "360":[18, 396, 134], "240":[133, 242, 395], "144":[394, 144]}
    youtubeurl = request.form.to_dict().get("videourl")
    print(youtubeurl)
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            youtubeurl,
            download=False
        )
    thing=0
    j={}
    for i in result['formats']:
        if int(i['format_id']) in mp4['720']:
            j=i
            break
    url=j['url']
    return {"videourl": url, "videoname":result["title"]}

@app.route("/")
def index():
    return open("index.html", "r").read()

app.config['SERVER_NAME'] = "0.0.0.0:8012"
app.config['SESSION_COOKIE_DOMAIN'] = "youtube.solithcy.xyz"
if __name__ == "__main__":
    serve(app,port=8012, host="0.0.0.0", threads=50)

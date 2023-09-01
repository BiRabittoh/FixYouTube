from fixyoutube import app
from fixyoutube.db import get_video_from_cache, get_info, clear_cache
import fixyoutube.constants as c
from flask import request, redirect, abort, render_template, Response
from requests import get
import re

def main_handler(request, video_id):
    user_agent = request.headers.get("User-Agent", "")
    result = re.findall(c.UA_REGEX, user_agent, flags=re.I)
    if len(result) == 0:
        return redirect(c.BASE_URL + video_id)

    info = get_info(video_id)
    if info is None:
        return abort(400)
    
    return render_template("base.html", info=info, base_url=c.BASE_URL)

@app.route("/")
def index_route():
    return render_template("index.html", repo_url=c.REPO_URL)

@app.route("/clear")
def clear_route():
    clear_cache()
    return { "done": True }

@app.route("/watch")
def watch_route():
    try:
        video_id = request.args["v"]
        if video_id == "":
            raise KeyError
    except KeyError:
        return redirect("/")
    return main_handler(request, video_id)

@app.route('/<video_id>')
def main_route(video_id):
    return main_handler(request, video_id)

@app.route('/proxy/<video_id>')
def proxy(video_id):
    result = get_video_from_cache(video_id)

    try:
        if result.url == "":
            raise AttributeError
    except AttributeError:
        return abort(400)
    
    return Response(get(result.url).content, headers=c.PROXY_HEADERS)

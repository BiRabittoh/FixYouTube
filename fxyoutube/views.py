from fxyoutube import app
from fxyoutube.db import get_video, get_info, clear_cache
import fxyoutube.constants as c

from flask import request, redirect, abort, render_template, Response
from requests import get
import re

def main_handler(request, video_id):
    if video_id == "":
        return abort(400)
    user_agent = request.headers.get("User-Agent", "")
    result = re.findall(c.UA_REGEX, user_agent, flags=re.I)

    if len(result) == 0:
        return redirect(c.BASE_URL + video_id)

    info = get_info(video_id)
    if info is None:
        return abort(400)
    
    return render_template("base.html", info=info, base_url=c.BASE_URL)

@app.route("/clear")
def clear_route():
    clear_cache()
    return { "done": True }

@app.route("/watch")
def watch_route():
    video = request.args.get('v', '')
    return main_handler(request, video)

@app.route('/', defaults={'video': ''})
@app.route('/<path:video>')
def main_route(video):
    return main_handler(request, video)

@app.route('/proxy/', defaults={'path': ''})
@app.route('/proxy/<path:path>')
def proxy(path):
    result = get_video(path)
    try:
        url = result[0][8]
    except IndexError:
        return abort(400)
    
    result = get(url)
    return Response(result.content, headers={ "Content-Type": "video/mp4" })

from requests import get
from requests.exceptions import JSONDecodeError
import fixyoutube.constants as c
import logging
logger = logging.getLogger(__name__)

def get_url(video: str):
    req_url = c.INVIDIOUS_ENDPOINT.format(instance=c.INVIDIOUS_INSTANCE, video=video)
    logger.debug("GET: " + req_url)
    return req_url

def get_info_from_api(video):
    try:
        res = get(get_url(video))
    except Exception as e:
        logger.warn("GET error: " + str(e))
        c.new_instance()
        return get_info_from_api(video)
    
    try:
        parsed = res.json()
    except JSONDecodeError:
        logger.warn("JSON decode failed for the following video: " + video)
        return None
    
    try:
        format = [ x for x in parsed["formatStreams"] if x["container"] == "mp4" ][-1]
    except KeyError:
        return None
    
    width, height = format["size"].split("x")

    return {
        "videoId": parsed["videoId"],
        "title": parsed["title"],
        "description": parsed["description"],
        "uploader": parsed["author"],
        "duration": parsed["lengthSeconds"],
        "height": height,
        "width": width,
        "url": format["url"]
    }

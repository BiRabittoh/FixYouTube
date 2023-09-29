from requests import get
from requests.exceptions import JSONDecodeError
import fixyoutube.constants as c

def get_url(video: str):
    return c.INVIDIOUS_ENDPOINT.format(instance=c.INVIDIOUS_INSTANCE, video=video)

def get_info_from_api(video):
    try:
        res = get(get_url(video))
    except Exception:
        print("Bad instance.")
        c.new_instance()
        return get_info_from_api(video)
    
    try:
        parsed = res.json()
    except JSONDecodeError:
        print("JSON decode error. Bad instance or video does not exist.")
        return None
    
    try:
        format = [ x for x in parsed["formatStreams"] if x["container"] == "mp4"][-1]
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

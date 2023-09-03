from peewee import Model, CharField, TextField, IntegerField, DateTimeField, DoesNotExist
from playhouse.sqliteq import SqliteQueueDatabase
from requests import get
from requests.exceptions import JSONDecodeError
from datetime import datetime, timedelta
import fixyoutube.constants as c

db = SqliteQueueDatabase(c.DB_URL)

class BaseModel(Model):
    class Meta:
        database = db

class Video(BaseModel):
    videoId = CharField(unique=True)
    title = CharField()
    description = TextField()
    uploader = CharField()
    duration = IntegerField()
    height = IntegerField()
    width = IntegerField()
    url = TextField()
    timestamp = DateTimeField(default=datetime.now)

def cache_video(info):
    try:
        Video.delete().where(Video.videoId == info['videoId']).execute()
    except DoesNotExist:
        pass
    return Video.create(**info)

def get_video_from_cache(video):
    try:
        temp = Video.get(Video.videoId == video)
    except DoesNotExist:
        return None

    delta = datetime.now() - temp.timestamp
    if delta > timedelta(minutes=c.YT_TTL_MINUTES):
        return None
    
    return temp

def get_info(video):
    info = get_video_from_cache(video)

    if info is not None:
        return info
    try:
        res = get(c.INVIDIOUS_ENDPOINT.format(video)).json()
    except JSONDecodeError:
        print("JSON decode error. Bad instance or video does not exist.")
        return None
    
    try:
        format = [ x for x in res["formatStreams"] if x["container"] == "mp4"][-1]
    except KeyError:
        return None
    
    width, height = format["size"].split("x")

    info = {
        "videoId": res["videoId"],
        "title": res["title"],
        "description": res["description"],
        "uploader": res["author"],
        "duration": res["lengthSeconds"],
        "height": height,
        "width": width,
        "url": format["url"]
    }

    return cache_video(info)

def clear_cache():
    Video.delete().execute()

db.connect()
db.create_tables([Video])

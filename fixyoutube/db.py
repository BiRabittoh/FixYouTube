from peewee import Model, CharField, TextField, IntegerField, DateTimeField, DoesNotExist
from playhouse.sqliteq import SqliteQueueDatabase
from datetime import datetime, timedelta
from fixyoutube.yt_info import get_info_ytdl
import fixyoutube.constants as c

db = SqliteQueueDatabase(c.DB_URL)

class BaseModel(Model):
    class Meta:
        database = db

class Video(BaseModel):
    id = CharField(unique=True)
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
        Video.delete().where(Video.id == info["id"]).execute()
    except DoesNotExist:
        pass
    return Video.create(**info)

def get_video_from_cache(video):
    try:
        temp = Video.get(Video.id == video)
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
    
    info = get_info_ytdl(video)
    if info is not None:
        cache_video(info)

    return info

def clear_cache():
    Video.delete().execute()

db.connect()
db.create_tables([Video])

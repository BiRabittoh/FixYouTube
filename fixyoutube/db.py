from peewee import Model, CharField, TextField, IntegerField, DateTimeField, DoesNotExist
from playhouse.sqliteq import SqliteQueueDatabase
from datetime import datetime, timedelta
import fixyoutube.constants as c
from fixyoutube.api import get_info_from_api
import logging
logger = logging.getLogger(__name__)

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
    if info is None:
        return
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
    
    logger.info("Video " + str(video) + " was requested.")
    info = get_video_from_cache(video)

    if info is not None:
        logger.info("Retrieved from cache.")
        return info
    
    info = get_info_from_api(video)

    logger.info("Retrieved from API.")
    return cache_video(info)

def clear_cache():
    Video.delete().execute()

db.connect()
db.create_tables([Video])

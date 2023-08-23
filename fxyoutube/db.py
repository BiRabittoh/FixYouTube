import sqlite3
from contextlib import closing
from datetime import datetime, timedelta
from fxyoutube.yt_info import get_info_ytdl
import fxyoutube.constants as c

create_query = '''
CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    uploader TEXT NOT NULL,
    duration int NOT NULL,
    height TEXT NOT NULL,
    width TEXT NOT NULL,
    url TEXT,
    timestamp DATETIME DEFAULT (datetime('now','localtime'))
);'''

def execute_query(query: str, attributes: list = []):
    with sqlite3.connect(c.DB_URL) as db_connection:
        with closing(db_connection.cursor()) as db_cursor:
            return list(db_cursor.execute(query, attributes))

def get_video_db(video_id):
    return execute_query("SELECT * FROM videos WHERE id = (?);", [ video_id ])

def cache_video(info):
    return execute_query("INSERT OR REPLACE INTO videos (id, title, description, uploader, duration, height, width, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", list(info.values()))

def get_video_from_cache(video):
    result = get_video_db(video)
    try:
        temp = result[0]
        timestamp = datetime.strptime(temp[8], c.TS_FORMAT)
        delta = datetime.now() - timestamp
        if delta > timedelta(minutes=c.YT_TTL_MINUTES):
            raise IndexError
    except IndexError:
        return None
    
    return {
        "id": temp[0],
        "title": temp[1],
        "description": temp[2],
        "uploader": temp[3],
        "duration": temp[4],
        "height": temp[5],
        "width": temp[6],
        "url": temp[7],
    }

def get_info(video):
    info = get_video_from_cache(video)

    if info is not None:
        return info
    
    info = get_info_ytdl(video)
    if info is not None:
        cache_video(info)

    return info

def clear_cache():
    execute_query("DELETE FROM videos;")
    execute_query("VACUUM;")

execute_query(create_query)

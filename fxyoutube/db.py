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
    uploader_id TEXT NOT NULL,
    video_ext TEXT NOT NULL,
    height TEXT NOT NULL,
    width TEXT NOT NULL,
    url TEXT NOT NULL,
    timestamp DATETIME DEFAULT (datetime('now','localtime'))
);'''

def execute_query(query: str, attributes: list = []):
    with sqlite3.connect(c.DB_URL) as db_connection:
        with closing(db_connection.cursor()) as db_cursor:
            return list(db_cursor.execute(query, attributes))

def get_video(video_id):
    return execute_query("SELECT * FROM videos WHERE id = (?);", [ video_id ])

def cache_video(info):
    return execute_query("INSERT OR REPLACE INTO videos (id, title, description, uploader, uploader_id, video_ext, height, width, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", list(info.values()))

def get_info(video):
    result = get_video(video)

    try:
        temp = result[0]
        timestamp = datetime.strptime(temp[9], c.TS_FORMAT)
        delta = datetime.now() - timestamp

        if delta > timedelta(seconds=30):
            raise IndexError
        
        info = {
            "id": temp[0],
            "title": temp[1],
            "description": temp[2],
            "uploader": temp[3],
            "uploader_id": temp[4],
            "video_ext": temp[5],
            "height": temp[6],
            "width": temp[7],
            "url": temp[8],
        }

    except IndexError:
        info = get_info_ytdl(video)
        if info is not None:
            cache_video(info)

    return info

def clear_cache():
    execute_query("DELETE FROM videos;")
    execute_query("VACUUM;")

execute_query(create_query)

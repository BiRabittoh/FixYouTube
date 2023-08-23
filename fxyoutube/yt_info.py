from yt_dlp import YoutubeDL, DownloadError
import fxyoutube.constants as c

ydl_keys = ["id", "title", "description", "uploader", "duration", "height", "width", "url"]

def truncate_lines(input_str: str, max: int = 4):
    return "\n".join(input_str.splitlines()[:max])

def get_info_ytdl(yt_id: str):
    try:
        with YoutubeDL(c.YTDL_OPTS) as ydl:
            info = ydl.extract_info(c.BASE_URL + yt_id, download=False)
            yt_info = { k: info[k] for k in ydl_keys }
    except DownloadError:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(c.BASE_URL + yt_id, download=False)
            yt_info = { k: info[k] for k in ydl_keys[:-3] }
            yt_info["height"] = yt_info["width"] = 0
            yt_info["url"] = ""
            
    yt_info["description"] = truncate_lines(yt_info["description"])
    return yt_info

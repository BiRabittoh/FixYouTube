from yt_dlp import YoutubeDL
import fxyoutube.constants as c
ydl = YoutubeDL()

def handle_format(format):

    if format["resolution"] == "audio only":
        return None # audio-only
    try:
        if format["audio_channels"] is None:
            return None # video-only
    except KeyError:
        return None # video-only

    if format["url"].endswith(".m3u8"):
        return None # HLS stream
    
    try:
        if format["filesize"] > c.MAX_SIZE_BYTES:
            return None # too large
    except TypeError:
        if format["filesize_approx"] > c.MAX_SIZE_BYTES:
            return None

    return format

def get_info_ytdl(yt_id: str):
    info = ydl.extract_info(c.BASE_URL + yt_id, download=False)
    formats = map(handle_format, info["formats"])
    formats = list(filter(lambda x: x is not None, formats))
    try:
        max_format = max(formats, key=lambda x:x["quality"])
    except ValueError:
        return None
    
    return {
        "id": info["id"],
        "title": info["title"],
        "description": info["description"],
        "uploader": info["uploader"],
        "uploader_id": info["uploader_id"],
        "video_ext": max_format["video_ext"],
        "height": max_format["height"],
        "width": max_format["width"],
        "url": max_format["url"],
    }

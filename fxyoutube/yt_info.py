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
            return None # too large

    return format

def truncate_lines(input_str: str, max: int = 5):
    return "\n".join(input_str.splitlines()[:max])

def get_info_ytdl(yt_id: str):
    info = ydl.extract_info(c.BASE_URL + yt_id, download=False)

    yt_info = {
        "id": info["id"],
        "title": info["title"],
        "description": truncate_lines(info["description"]),
        "uploader": info["uploader"],
        "uploader_id": info["uploader_id"],
        "duration": info["duration"],
    }

    formats = map(handle_format, info["formats"])
    formats = filter(lambda x: x is not None, formats)
    try:
        max_format = max(formats, key=lambda x:x["quality"])
    except ValueError:
        yt_info.update({
            "video_ext": None,
            "height": 0,
            "width": 0,
            "url": None
        })

    yt_info.update({
        "video_ext": max_format["video_ext"],
        "height": max_format["height"],
        "width": max_format["width"],
        "url": max_format["url"],
    })
    print(max_format["url"])
    return yt_info

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
    
    if format["video_ext"] != "mp4":
        return None
    
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

    yt_info = { k: truncate_lines(info[k]) for k in ["id", "title", "description", "uploader", "duration"] }
    yt_info.update({ "height": 0, "width": 0, "url": None })

    formats = map(handle_format, info["formats"])
    formats = filter(lambda x: x is not None, formats)
    try:
        max_format = max(formats, key=lambda x:x["quality"])
        yt_info.update({ k: max_format[k] for k in ["height", "width", "url"] })
    except ValueError:
        pass
    finally:
        return yt_info

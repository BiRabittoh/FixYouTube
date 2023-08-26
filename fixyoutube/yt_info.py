from yt_dlp import YoutubeDL, DownloadError
import fixyoutube.constants as c

def truncate_lines(input_str: str, max: int = 4):
    return "\n".join(input_str.splitlines()[:max])

def get_info_ytdl(yt_id: str):
    try:
        with YoutubeDL(c.YTDL_OPTS) as ydl:
            info = ydl.extract_info(c.BASE_URL + yt_id, download=False)
            yt_info = { k: info[k] for k in c.YTDL_KEYS[:-1] }
            yt_info[c.URL_KEY] = info.get(c.URL_KEY, "")
    except DownloadError:
        return None
    
    yt_info["description"] = truncate_lines(yt_info["description"])
    return yt_info

from dotenv import load_dotenv
from os import getenv
from requests import get
load_dotenv()

MAX_SIZE_MB = getenv("MAX_SIZE_MB", "50")
YT_TTL_MINUTES = int(getenv("YT_TTL_MINUTES", 60 * 6))
DB_URL = getenv("DB_URL", "cache.db")
INVIDIOUS_INSTANCE = getenv("INVIDIOUS_INSTANCE", None)
REPO_URL = getenv("REPO_URL", "https://github.com/BiRabittoh/FixYouTube")

if INVIDIOUS_INSTANCE is None:
    instances = get("https://api.invidious.io/instances.json?pretty=1&sort_by=api,type").json()
    INVIDIOUS_INSTANCE = instances[0][0]

UA_REGEX = r"bot|facebook|embed|got|firefox\/92|firefox\/38|curl|wget|go-http|yahoo|generator|whatsapp|preview|link|proxy|vkshare|images|analyzer|index|crawl|spider|python|cfnetwork|node"
BASE_URL = "https://www.youtube.com/watch?v="
PROXY_HEADERS_REQUEST = { "Range": f"bytes=0-{MAX_SIZE_MB}000000" }
PROXY_HEADERS_RESPONSE = { "Content-Type": "video/mp4" }
INVIDIOUS_ENDPOINT = "https://" + INVIDIOUS_INSTANCE + "/api/v1/videos/{}?fields=videoId,title,description,author,lengthSeconds,size,formatStreams"

# test stuff
TELEGRAM_USER_AGENT = "TelegramBot (like TwitterBot)"
GOOD_VIDEO_ID = "crF2AIDlo54"
BAD_VIDEO_ID = GOOD_VIDEO_ID[:-1]

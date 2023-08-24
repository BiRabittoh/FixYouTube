MAX_SIZE_MB = 50
YT_TTL_MINUTES = 60 * 6
DB_URL = "cache.db"

UA_REGEX = r"bot|facebook|embed|got|firefox\/92|firefox\/38|curl|wget|go-http|yahoo|generator|whatsapp|preview|link|proxy|vkshare|images|analyzer|index|crawl|spider|python|cfnetwork|node"
BASE_URL = "https://www.youtube.com/watch?v="
REPO_URL = "https://github.com/BiRabittoh/FixYouTube"
PROXY_HEADERS = { "Content-Type": "video/mp4" }
YTDL_OPTS = { "format": f"best[ext=mp4][filesize<?{ MAX_SIZE_MB }M][filesize_approx<?{ MAX_SIZE_MB }M][protocol^=http][protocol!*=dash] / (bv*+ba/b)" }
YTDL_KEYS = [ "id", "title", "description", "uploader", "duration", "height", "width", "url" ]
URL_KEY = YTDL_KEYS[-1]

from http.server import BaseHTTPRequestHandler
import urllib.parse
import urllib.request

# Dynamic playlist mapping (id -> source URL)
PLAYLISTS = {
    
    "icc": "https://raw.githubusercontent.com/doctor-8trange/nexphi0/refs/heads/main/data/icc.m3u",
"z5": "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/z5.m3u",
"jtv": "https://raw.githubusercontent.com/alex4528y/m3u/refs/heads/main/jtv.m3u",
"aosports": "https://raw.githubusercontent.com/0ashalive/h2o/refs/heads/main/AOsports.m3u",
"axsports": "https://raw.githubusercontent.com/srhady/axsports/refs/heads/main/playlist.m3u",
"ottplus": "https://drive.usercontent.google.com/u/0/uc?id=1SJi5LT5bQ1ZHT5eYQM3VOYuNB6U-mYCB&export=download",
"sonyliv": "https://allplaylist.vercel.app/sony_liv.m3u",
"zongmobiletv": "https://raw.githubusercontent.com/bddeveloperyt/rriptv/refs/heads/main/zongmobiletv.m3u",
"sports2": "https://raw.githubusercontent.com/doms9/iptv/refs/heads/default/M3U8/TV.m3u8",
"yupp": "https://raw.githubusercontent.com/Mehedi-Hasan-404/yupp/refs/heads/main/playlist.m3u",
"sp": "https://raw.githubusercontent.com/raid35/channel-links/refs/heads/main/Canal_SP.m3u",
"kids": "https://drive.usercontent.google.com/u/0/uc?id=1ldtN9AUnmJidxK4SrM3C-xDwsuxw4Nlh&export=download",
"roarzone": "https://raw.githubusercontent.com/sm-monirulislam/RoarZone-Auto-Update-playlist/refs/heads/main/RoarZone.m3u",
"pk": "https://playlists-by-playztv.pages.dev/c-pkk.m3u",
"in": "https://raw.githubusercontent.com/bddeveloperyt/rriptv/refs/heads/main/waves.m3u",
"dish": "https://drive.usercontent.google.com/u/0/uc?id=1v71hpQ0wmJXrrjgrANtPQGtZ4Q6RgdJa&export=download",
"dis": "https://drive.usercontent.google.com/u/0/uc?id=1Qk2wGwj0A3Mw7DB92d8EogTrqmoGpuFu&export=download",
"netflix2": "https://allplaylist.vercel.app/NETFIX_2.json",
    "cartoon": "https://allplaylist.vercel.app/CARTOON_MOVIES.json",
    "tending": "https://allplaylist.vercel.app/TRENDING.json",
    "south": "https://allplaylist.vercel.app/SOUTH_DUBBED.json",
    "hollywood": "https://allplaylist.vercel.app/HOLLYWOOD.json",
    "hindi": "https://allplaylist.vercel.app/NEW_MOVIES.json",
    "hotstarplayer": "https://allplaylist.vercel.app/HOTSTAR.json",
    "aprimeplayer": "https://allplaylist.vercel.app/AMAZON_PRIME.json",
    "sonylivplayer": "https://allplaylist.vercel.app/SONY_LIV.json",
    "zee5player": "https://allplaylist.vercel.app/ZEE5.json",
    "mxplayer": "https://allplaylist.vercel.app/MX_PLAYER.json",
    "vootplayer": "https://allplaylist.vercel.app/VOOT.json",
    "mxplayerhindi": "https://raw.githubusercontent.com/0ashalive/h2o/refs/heads/main/maxplayerall.json",
    "mxplayeren": "https://raw.githubusercontent.com/0ashalive/h2o/refs/heads/main/maxplayerenglish.json",
    "request": "https://allplaylist.vercel.app/request.m3u",
    "etvwin1": "https://drive.usercontent.google.com/u/0/uc?id=10iYNCDX5dwMv5qgZTAr0qUDsEuYaA0ir&export=download",
    "tamilv1": "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u",
    "sunnxt1": "https://raw.githubusercontent.com/alexandermail371/cricfytv/refs/heads/main/sunxt.m3u",
    "dangal1": "https://3ty8.short.gy/udpf_dangalplus.m3u",
    "bdtataplay": "https://drive.usercontent.google.com/u/0/uc?id=1h49qJe5_c8WTwAai622nIK7DhUfByjHI&export=download",
    "beinarlive":"https://raw.githubusercontent.com/IPTVFlixBD/OopsTv/refs/heads/main/bein-mq/playlist.m3u",
    "tntlive":"https://raw.githubusercontent.com/IPTVFlixBD/OopsTv/refs/heads/main/ts3/playlist.m3u",
    "liveevents1":"https://sportzfys.streamit.workers.dev/?url=https://raw.githubusercontent.com/abusaeeidx/BDxTV/refs/heads/main/playlist_s.m3u",
"liveevents2":"https://raw.githubusercontent.com/doms9/iptv/refs/heads/default/M3U8/events.m3u8",
"combolive":"https://raw.githubusercontent.com/Mrbotrx/All-FREE-TV/refs/heads/main/combined_playlist.m3u",
    "tatav2": "http://66.102.126.10:8000/playlist.m3u",
    
}

# Default playlist ID if none is provided in the URL query
DEFAULT_PLAYLIST_ID = "z5"
TELEGRAM_URL = "https://t.me/ashaott"

# Browsers to detect and redirect to Telegram
BROWSER_USER_AGENTS = [
    "mozilla",
    "chrome",
    "safari",
    "edge",
    "opera",
    "firefox",
]

# Media player User-Agent signatures (explicitly includes OkHttp variants)
MEDIA_PLAYER_AGENTS = [
    "okhttp",
    "kodi",
    "iptv",
    "tivimate",
    "exoplayer",
]


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Fetch lowercased User-Agent header from incoming request
        user_agent = (self.headers.get("User-Agent") or "").lower()

        # 1. Player Verification & Browser Redirection Logic
        is_media_player = any(
            player in user_agent for player in MEDIA_PLAYER_AGENTS
        )
        is_browser = any(
            browser in user_agent for browser in BROWSER_USER_AGENTS
        )

        # Redirect standard web browsers (and non-players) to Telegram
        if is_browser and not is_media_player:
            self.send_response(302)
            self.send_header("Location", TELEGRAM_URL)
            self.send_header("Cache-Control", "no-cache, no-store")
            self.end_headers()
            return

        # 2. Extract ?id= parameter from URL query string
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        playlist_id = query_params.get("id", [DEFAULT_PLAYLIST_ID])[0].lower()

        # Return 404 if requested playlist ID is missing from dictionary
        if playlist_id not in PLAYLISTS:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                f"#ERROR: Playlist key '{playlist_id}' not found.".encode("utf-8")
            )
            return

        target_url = PLAYLISTS[playlist_id]

        # 3. Request raw M3U playlist file content
        try:
            req = urllib.request.Request(
                target_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
                },
            )

            with urllib.request.urlopen(req, timeout=15) as response:
                m3u_content = response.read()

            # 4. Output raw playlist data directly to player
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header(
                "Cache-Control", "no-cache, no-store, must-revalidate"
            )
            self.end_headers()
            self.wfile.write(m3u_content)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            err_msg = f"#EXTM3U\n#ERROR: Failed to fetch target playlist: {str(e)}"
            self.wfile.write(err_msg.encode("utf-8"))
            

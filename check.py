# -*- coding: utf-8 -*-
# Site koruma kontrol aracı - dig GEREKMEZ
# Python standart kütüphane + requests

import socket
import sys
import subprocess
import random

try:
    import requests
    import urllib3
    urllib3.disable_warnings()
    REQ_OK = True
except ImportError:
    REQ_OK = False
    print("[!] requests yok: pip3 install requests")

# ======================== RENK ========================
R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; C = '\033[96m'; E = '\033[0m'

# ======================== DNS LOOKUP ========================
def dns_lookup(host):
    try:
        ips = socket.getaddrinfo(host, None)
        return sorted(set(ip[4][0] for ip in ips))
    except Exception as e:
        return []

def get_cname(host):
    """nslookup varsa kullan, yoksa atla"""
    try:
        out = subprocess.check_output(["nslookup", host], timeout=5, stderr=subprocess.DEVNULL).decode()
        lines = out.splitlines()
        for i, line in enumerate(lines):
            if "canonical name" in line.lower() or "aliases" in line.lower():
                return line.strip()
        return None
    except Exception:
        return None

# ======================== HEADER CHECK ========================
def check_headers(url):
    if not REQ_OK:
        return None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15",
        }
        r = requests.head(url, headers=headers, timeout=8, verify=False, allow_redirects=True)
        return dict(r.headers)
    except Exception:
        try:
            r = requests.get(url, headers=headers, timeout=8, verify=False, allow_redirects=True, stream=True)
            return dict(r.headers)
        except Exception as e:
            return {"_error": str(e)}

# ======================== CDN/WAF TESPİT ========================
CDN_SIGNATURES = {
    "cloudflare":      ["server: cloudflare", "cf-ray", "cf-cache-status", "__cfduid", "cf-request-id"],
    "akamai":          ["x-akamai", "akamai-grn", "akamaighost", "x-akamai-transformed"],
    "cloudfront":      ["x-amz-cf-id", "x-amz-cf-pop", "cloudfront", "via: 1.1"],
    "fastly":          ["x-served-by: cache", "x-fastly", "fastly-io", "x-cache: hit from fastly"],
    "sucuri":          ["x-sucuri-id", "x-sucuri-cache", "server: sucuri"],
    "imperva/incapsula": ["x-iinfo", "x-cdn: incapsula", "visid_incap"],
    "aws_waf":         ["x-amzn-requestid", "x-amz-apigw-id", "awselb"],
    "azure":           ["x-azure-ref", "x-msedge-ref", "azurewebsites"],
    "google_cloud":    ["x-cloud-trace-context", "server: gws", "server: google"],
    "nginx":           ["server: nginx"],
    "apache":          ["server: apache"],
    "iis":             ["server: microsoft-iis"],
    "litespeed":       ["server: litespeed"],
    "openresty":       ["server: openresty"],
    "caddy":           ["server: caddy"],
    "gunicorn":        ["server: gunicorn"],
    "werkzeug":        ["server: werkzeug"],
}

def analyze(headers):
    if not headers:
        return [], []
    blob = " ".join(f"{k}: {v}" for k, v in headers.items()).lower()
    
    found_cdn = []
    found_origin = []
    
    for name, sigs in CDN_SIGNATURES.items():
        for sig in sigs:
            if sig.lower() in blob:
                if name in ("nginx", "apache", "iis", "litespeed", "openresty", "caddy", "gunicorn", "werkzeug"):
                    found_origin.append(name)
                else:
                    found_cdn.append(name)
                break
    
    return found_cdn, found_origin

# ======================== KARAR ========================
def decide(headers, cdn, origin):
    print(f"\n{C}=============== KARAR ==============={E}")
    
    if cdn:
        print(f"{R}[X] KORUMALI - CDN/WAF tespit edildi: {', '.join(cdn).upper()}{E}")
        print(f"{R}[X] Bu siteye flood saldırısı ETKİSİZ olur.{E}")
        print(f"{Y}[i] CDN edge'de cache tutar, gerçek sunucuya ulaşmaz.{E}")
        return False
    
    if origin:
        print(f"{G}[+] Origin server: {', '.join(origin).upper()}{E}")
        print(f"{G}[+] CDN/WAF YOK{ E}")
        print(f"{G}[+] Bu site KORUMASIZ - flood DENENEBİLİR{E}")
        return True
    
    print(f"{Y}[?] Net veri yok. Manuel kontrol et:{E}")
    if headers:
        for k, v in list(headers.items())[:10]:
            print(f"    {k}: {v}")
    return None

# ======================== ANA ========================
def main():
    print(f"{C}{'='*55}{E}")
    print(f"{C}  SİTE KORUMA ANALİZ ARACI - dig GEREKMEZ{E}")
    print(f"{C}{'='*55}{E}\n")
    
    url = input("Site URL (örn: https://example.com): ").strip()
    if not url:
        print(f"{R}[!] URL boş{E}"); return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    from urllib.parse import urlparse
    p = urlparse(url)
    host = p.hostname
    
    print(f"\n{C}[*] Hedef: {host}{E}")
    print(f"{C}[*] Analiz başlıyor...{E}\n")
    
    # 1) DNS
    print(f"{C}--- DNS ÇÖZÜMLEME ---{E}")
    ips = dns_lookup(host)
    if not ips:
        print(f"{R}[X] DNS çözümlenemedi{E}")
        return
    for ip in ips:
        print(f"{G}[+] {host} -> {ip}{E}")
    
    # 2) CNAME
    print(f"\n{C}--- CNAME ---{E}")
    cname = get_cname(host)
    if cname:
        print(f"{Y}[i] {cname}{E}")
        blob = cname.lower()
        for cdn in ["cloudflare", "akamai", "fastly", "cloudfront", "sucuri", "incapsula", "azure", "google"]:
            if cdn in blob:
                print(f"{R}[X] CNAME CDN'e işaret ediyor: {cdn.upper()}{E}")
    else:
        print(f"{G}[+] CNAME yok (veya nslookup yok) - düz A kaydı görünüyor{E}")
    
    # 3) HTTP Header
    print(f"\n{C}--- HTTP HEADER ---{E}")
    headers = check_headers(url)
    if headers is None:
        print(f"{R}[!] requests yok, header kontrolü atlanıyor{E}")
        headers = {}
    elif "_error" in headers:
        print(f"{R}[X] HTTP isteği başarısız: {headers['_error']}{E}")
        headers = {}
    else:
        for k, v in list(headers.items())[:15]:
            print(f"  {Y}{k}{E}: {v}")
    
    # 4) Analiz
    cdn, origin = analyze(headers)
    decide(headers, cdn, origin)
    
    # 5) Özet
    print(f"\n{C}=============== ÖZET ==============={E}")
    print(f"Host    : {host}")
    print(f"IP'ler  : {', '.join(ips)}")
    print(f"CDN/WAF : {', '.join(cdn) if cdn else 'YOK'}")
    print(f"Origin  : {', '.join(origin) if origin else 'bilinmiyor'}")
    print(f"{C}===================================={E}\n")

if __name__ == "__main__":
    main()
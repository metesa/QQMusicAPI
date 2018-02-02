# coding=utf-8

import time
import random
import requests

# __all__ = ['guid', 'music_headers', 'text_headers', 'session']


guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
music_headers = {
    "referer": "https://y.qq.com/portal/player.html",
    "cookie": 'pgv_pvi=6725760000; pgv_si=s4324782080; pgv_pvid=%s; qqmusic_fromtag=66' % guid,
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) "
                  "Version/9.0 Mobile/13B143 Safari/601.1 "
}
text_headers = {
    "referer": "https://y.qq.com/portal/player.html",
    "cookie": "skey=@LVJPZmJUX; p",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) "
                  "Version/9.0 Mobile/13B143 Safari/601.1 "
}
session = requests.Session()

import os
import re
import json

import requests
import random
from hashlib import md5

from . import Translator

def get_api_key():
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        data = json.load(f)['baidu']
    return data['APPID'], data['APPKEY']

appid, appkey = get_api_key()

def _make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

class Translator_baidu(Translator):
    def __init__(self, sleep_time = 3):
        self.sleep_time = sleep_time

        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        self.url = endpoint + path

        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def _translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        if source_lang == 'ko':
            source_lang = 'kor'

        text = re.sub('\n', ' ', text)

        salt = random.randint(32768, 65536)
        sign = _make_md5(appid + text + str(salt) + appkey)

        payload = {'appid': appid, 'q': text, 'from': source_lang, 'to': target_lang, 'salt': salt, 'sign': sign}

        r = requests.post(self.url, params=payload, headers=self.headers)
        result = r.json()

        return result["trans_result"][0]["dst"]
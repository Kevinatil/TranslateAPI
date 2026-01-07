import os
import hashlib
import hmac
import json
import re
import time
from datetime import datetime
from http.client import HTTPSConnection

from . import Translator

def get_id_key():
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        data = json.load(f)['TencentCloud']
    return data['SecretId'], data['SecretKey']

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY = get_id_key()

secret_id = TENCENTCLOUD_SECRET_ID
secret_key = TENCENTCLOUD_SECRET_KEY
token = ""

service = "tmt"
host = "tmt.tencentcloudapi.com"
region = "ap-beijing"
version = "2018-03-21"
action = "TextTranslate"
endpoint = "https://tmt.tencentcloudapi.com"
algorithm = "TC3-HMAC-SHA256"
timestamp = int(time.time())
date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

http_request_method = "POST"
canonical_uri = "/"
canonical_querystring = ""
ct = "application/json; charset=utf-8"
canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
signed_headers = "content-type;host;x-tc-action"
credential_scope = date + "/" + service + "/" + "tc3_request"

class Translator_tencent(Translator):
    def __init__(self, sleep_time = 3):
        self.payload = "{{\"SourceText\":\"{text}\",\"Source\":\"{source}\",\"Target\":\"{target}\",\"ProjectId\":0}}"
        self.sleep_time = sleep_time

    def _translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        text = re.sub('\n', ' ', text)
        payload = self.payload.format(text = text, source=source_lang, target=target_lang)
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" +
                            canonical_uri + "\n" +
                            canonical_querystring + "\n" +
                            canonical_headers + "\n" +
                            signed_headers + "\n" +
                            hashed_request_payload)
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (algorithm + "\n" +
                        str(timestamp) + "\n" +
                        credential_scope + "\n" +
                        hashed_canonical_request)
        secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        authorization = (algorithm + " " +
                        "Credential=" + secret_id + "/" + credential_scope + ", " +
                        "SignedHeaders=" + signed_headers + ", " +
                        "Signature=" + signature)
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": host,
            "X-TC-Action": action,
            "X-TC-Timestamp": timestamp,
            "X-TC-Version": version,
            "X-TC-Region": region
        }

        req = HTTPSConnection(host)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = json.loads(req.getresponse().read().decode())
        return resp['Response']['TargetText']


if __name__ == "__main__":
    trans = Translator_tencent()
    print(trans.translate('저녁엔 식사 약속이 있었습니다', source_lang='ko', target_lang='zh'))
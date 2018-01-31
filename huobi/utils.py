"""
based on   : https://github.com/KlausQIU
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import json

import urllib.request, urllib.parse, urllib.error
import datetime
import requests
from urllib.parse import urlparse

# timeout in 5 seconds:
TIMEOUT = 5

# API 请求地址
TRADE_URL = "https://api.huobi.pro"

#各种请求,获取数据方式
def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)

    try:
        response = requests.get(url, postdata, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "User-Agent": "Chrome/39.0.2171.71",
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        response = requests.post(url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(("httpPost failed, detail is:%s" % e))
        return {"status":"fail","msg":e}

def create_sign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(list(pParams.items()), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='utf8')
    secret_key = secret_key.encode(encoding='utf8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature

class Auth:
    def __init__(self, pkey, skey):
        """
        skey:
        """
        self._pkey = pkey
        self._skey = skey

    def get(self, request_path, params):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self._pkey,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_name = host_url = TRADE_URL
        #host_name = urlparse.urlparse(host_url).hostname
        host_name = urlparse(host_url).hostname
        host_name = host_name.lower()

        params['Signature'] = create_sign(params, method, host_name, request_path, self._skey)
        url = host_url + request_path
        return http_get_request(url, params)

    def post(self, request_path, params):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self._pkey,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = TRADE_URL
        #host_name = urlparse.urlparse(host_url).hostname
        host_name = urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = create_sign(params_to_sign, method, host_name, request_path, self._skey)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return http_post_request(url, params)

""" Request from WeChat official server
"""
import json

import requests
from wx_secret import APP_SECRET, APP_ID


class CronJobConfig:
    JOBS = [{
        'id': 'get_access_token',
        'func': 'application.models.wx_backend:get_access_token',
        'trigger': 'interval',  # interval task
        'seconds': 5
    }]


def get_access_token(app_id=APP_ID,
                     secret=APP_SECRET):
    with open('./access_token.txt', 'w', encoding='utf-8') as f:
        _url = ('https://api.weixin.qq.com/cgi-bin/token?'
                'grant_type=client_credential&appid={}&secret={}').format(app_id, secret)
        response = requests.get(_url)
        print(response.json())
        f.write(response.json()['access_token'])


def get_qr_code(scene: str):
    _PAGE = 'pages/fillIn/fillIn'
    with open('./access_token.txt', 'r', encoding='utf-8') as f:
        access_token = f.read()
    _url = ('https://api.weixin.qq.com/wxa/getwxacodeunlimit?'
            'access_token={}').format(access_token)
    data = {
        'scene': scene,
        # 'page': _PAGE
    }
    print(data)
    response = requests.post(_url, json=data)
    print(response.content)
    with open('./pic.png', 'wb') as f:
        f.write(response.content)

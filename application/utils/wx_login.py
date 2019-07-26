import requests
from wx_secret import APP_SECRET, APP_ID, AUTH_URL


def auth_wx_login(js_code,
                  auth_url=AUTH_URL,
                  app_id=APP_ID,
                  secret=APP_SECRET,
                  grant_type='authorization_code'
                  ) -> dict:
    if type(js_code) is not str:
        raise TypeError('TypeError in function auth_wx_login: js_code must be string')
    _url = auth_url.format(app_id, secret, js_code, grant_type)
    response = requests.get(_url)
    return response.json()

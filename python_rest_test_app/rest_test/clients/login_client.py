__author__ = 'alonitzhaki'
import json

import requests
from utils.headers import AdskCommonHeadersManager

from rest_test import app_settings as settings


class LoginClient(object):
    KEY_USERNAME = 'username'
    KEY_PASSWORD = 'password'
    KEY_SESSION_INFO = 'sessionInfo'
    KEY_USER_INFO = 'userInfo'
    KEY_TICKET = 'ticket'
    KEY_AUTH_TYPE = 'authType'
    KEY_USER_ID = 'id'
    KEY_EIDM_USER_ID = 'eidmUserId'

    PARAM_USER_NAME = 'username'
    PARAM_PASSWORD = 'password'

    def login_v2(self, user_name, password, app_id=1):
        url = settings.MAIN_SERVER_URI + '/main/users/login/v2'

        headers = {'Content-type': 'application/json', AdskCommonHeadersManager.ADSK_APP_ID_HEADER: app_id,
                   'x-ads-device-type': settings.DEVICE_TYPE_HEADER}

        body = {}
        body.__setitem__(self.PARAM_USER_NAME, user_name)
        body.__setitem__(self.PARAM_PASSWORD, password)
        try:
            return requests.post(url=url, headers=headers, data=json.dumps(body))
        except Exception as e:
            print('LoginClient.login_v2: body: ' + str(
                body) + '. Exception msg: ' + str(e.message) + '. Exception args: ' + str(e.args) + '\n')
            return None
